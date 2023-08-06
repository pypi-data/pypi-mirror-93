import torch
from minetorch.plugin import Plugin
import typing
import copy


class SelfDistillation(Plugin):

    def __init__(
        self,
        top_k: int = 3,
        start_distillation_from: int = 10,
        weights: typing.List = [0.4, 0.3, 0.2, 0.1],
        label_transfer: typing.Callable = None
    ):
        assert start_distillation_from > top_k
        assert len(weights) == top_k + 1
        self.top_k = top_k
        self.start_distillation_from = start_distillation_from
        self.weights = weights
        self.selected_epochs = None
        self.label_transfer = label_transfer
        self.val_losses = []
        self.pseudo_labels = []

    def state_dict(self):
        return {
            'pseudo_labels': self.pseudo_labels,
            'selected_epochs': self.selected_epochs,
            'val_losses': self.val_losses
        }

    def load_state_dict(self, state):
        self.pseudo_labels = state['pseudo_labels']
        self.selected_epochs = state['selected_epochs']
        self.val_losses = state['val_losses']

    def after_init(self):
        self.dataloader = torch.utils.data.DataLoader(
            dataset=self.miner.train_dataloader.dataset,
            batch_size=self.miner.train_dataloader.batch_size,
            num_workers=self.miner.train_dataloader.num_workers,
            pin_memory=self.miner.train_dataloader.pin_memory
        )

    def before_epoch_start(self, epoch: int):
        if epoch < self.start_distillation_from:
            return
        selected_epochs = self._get_selected_epochs()

        if selected_epochs != self.selected_epochs:
            self.selected_epochs = selected_epochs
            self.miner.logger.info(f'update selected epochs to {self.selected_epochs}')
            self._generate_pseudo_label()
        else:
            self.miner.logger.info(f'selected epochs not changed: {self.selected_epochs}')

    def wrapped_dataloader(self):
        pass

    def change_forward(self):

        def forward_fn(miner, data):
            predict = miner.model(data[0].to(miner.devices))
            loss = miner.loss_func(predict, data[1].to(miner.devices))
            return predict, loss

        self.miner.forward_fn = forward_fn

    def after_epoch_end(
        self, train_loss: float, val_loss: float, epoch: int):
        self.val_losses.append((epoch, val_loss))

    def _generate_pseudo_label(self):
        self.pseudo_labels = []
        with torch.no_grad():
            for epoch in self.selected_epochs:
                model = copy.deepcopy(self.miner.model)
                checkpoint = torch.load(self.miner.model_file_path(epoch))
                model.load_state_dict(checkpoint['state_dict'])
                model.eval()
                model.to(self.miner.devices)
                self.pseudo_labels.append(self._inference(model))

    def _inference(self, model):
        predicts = []
        for data in self.dataloader:
            output = model(data[0])
            if self.label_transfer:
                output = self.label_transfer(output)
            predicts += output
        return predicts

    def _get_selected_epochs(self):
        return tuple(map(
            lambda x: x[0],
            sorted(self.val_losses, key=lambda x: x[1], reverse=False)
        ))[:3]


class WrappedDataset(torch.utils.data.DataLoader):

    def __init__(self, pseudo_labels):
        self.pseudo_labels = pseudo_labels

    def __len__(self):
        return len(self.miner.train_dataloader.dataset)

    def __getitem__(self, index):
        return [self.miner.train_dataloader.dataset[index], *self.pseudo_labels[index]]
