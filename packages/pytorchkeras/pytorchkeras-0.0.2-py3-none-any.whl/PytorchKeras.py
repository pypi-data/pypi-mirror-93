import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

#
from Constants import Constants


class PytorchKeras:
    def __init__(self, model=None):
        self.model = model
        self.optimizer = None
        self.loss = None
        self.metrics = None
        self.loss_weights = None
        self.weighted_metrics = None
        self.run_eagerly = None
        self.steps_per_execution = None
        self.device = None
        self.epochs = None

    def compile(self, optimizer=None, loss=None, metrics=None, loss_weights=None,
                weighted_metrics=None, run_eagerly=None, steps_per_execution=None, device="cpu"):
        """
        It works as same of Keras Model.compile function
        :param optimizer:
        :param loss:
        :param metrics:
        :param loss_weights:
        :param weighted_metrics:
        :param run_eagerly:
        :param steps_per_execution:
        :param device:
        :return:
        """
        self.optimizer = optimizer
        self.loss = loss
        self.metrics = metrics
        self.loss_weights = loss_weights
        self.weighted_metrics = weighted_metrics
        self.run_eagerly = run_eagerly
        self.steps_per_execution = steps_per_execution
        self.device = device

    @staticmethod
    def get_data_loader_from_dataset(dataset, batch_size, shuffle, num_of_worker):
        """
        :param dataset:
        :param batch_size:
        :param shuffle:
        :param num_of_worker:
        :return: new DataLoader from dataset with given configuration
        """
        data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, sampler=None,
                                 batch_sampler=None, num_workers=num_of_worker, collate_fn=None,
                                 pin_memory=False, drop_last=False, timeout=0,
                                 worker_init_fn=None, prefetch_factor=2,
                                 persistent_workers=False)
        return data_loader

    @staticmethod
    def get_num_of_batches(dataloader):
        """

        :param dataloader: Any DataLoader
        :return: total no of batches in dataloader
        """
        return len(dataloader)

    def train_one_epoch(self, train_tqdm):
        """

        :param train_tqdm:
        :return: train_loss_for_current_epoch
        """
        train_loss_for_current_epoch = 0.0
        self.model.train()
        for train_x, train_y in train_tqdm:
            self.optimizer.zero_grad()
            output = self.model(train_x)
            loss = self.loss(output, train_y)
            loss.backward()
            self.optimizer.step()
            train_loss_for_current_epoch += loss.item()
            train_tqdm.set_postfix({"loss": loss.item(), "accuracy": 1})
        return train_loss_for_current_epoch

    def validate_val_epoch(self, val_tqdm):
        """

        :param val_tqdm:
        :return: val_loss_for_current_epoch
        """
        val_loss_for_current_epoch = 0.0
        self.model.eval()
        with torch.no_grad():
            for val_x, val_y in val_tqdm:
                output = self.model(val_x)
                loss = self.loss(output, val_y)
                val_loss_for_current_epoch += loss.item()
                val_tqdm.set_postfix({"val_loss": loss.item(), "val_accuracy": 1})
        return val_loss_for_current_epoch

    def train(self, train_data_loader, val_data_loader):
        """

        :param train_data_loader:
        :param val_data_loader:
        :return: dictionary object containing history of the training
        """
        train_loss_for_all_epochs = []
        val_loss_for_all_epochs = []
        for i in range(self.epochs):
            train_tqdm = tqdm(train_data_loader, desc=f"Epoch {i + 1}/{self.epochs} training   ",
                              ascii=Constants.TQDM_TRAINING_BAR_CHARACTER,
                              # colour='black'
                              unit=Constants.TQDM_UNIT)

            train_loss_for_one_epoch = self.train_one_epoch(train_tqdm) / self.get_num_of_batches(train_data_loader)
            train_loss_for_all_epochs.append(train_loss_for_one_epoch)

            if val_data_loader is not None:
                val_tqdm = tqdm(train_data_loader, desc=f"Epoch {i + 1}/{self.epochs} validating ",
                                ascii=Constants.TQDM_VAL_BAR_CHARACTER,
                                # colour='green',
                                unit=Constants.TQDM_UNIT)
                val_loss_for_one_epoch = self.validate_val_epoch(val_tqdm) / self.get_num_of_batches(val_data_loader)
                val_loss_for_all_epochs.append(val_loss_for_one_epoch)

        history = {"train_loss": train_loss_for_all_epochs,
                   "val_loss": val_loss_for_all_epochs}

        return history

    def fit(self, train_dataset, batch_size=None, epochs=1, verbose=1, callbacks=None, validation_split=0.0,
            validation_dataset=None, shuffle=True,
            class_weight=None, sample_weight=None, initial_epoch=0,
            steps_per_epoch=None, validation_steps=None,
            validation_batch_size=None, validation_freq=1, max_queue_size=10,
            workers=1, use_multiprocessing=False):
        """

        :param train_dataset:
        :param batch_size:
        :param epochs:
        :param verbose:
        :param callbacks:
        :param validation_split:
        :param validation_dataset:
        :param shuffle:
        :param class_weight:
        :param sample_weight:
        :param initial_epoch:
        :param steps_per_epoch:
        :param validation_steps:
        :param validation_batch_size:
        :param validation_freq:
        :param max_queue_size:
        :param workers:
        :param use_multiprocessing:
        :return:  dictionary object containing history of the training
        """
        self.epochs = epochs

        train_data_loader = self.get_data_loader_from_dataset(train_dataset, batch_size, shuffle, workers)
        val_data_loader = None
        if validation_dataset is not None:
            val_data_loader = self.get_data_loader_from_dataset(train_dataset, batch_size, shuffle, workers)

        history = self.train(train_data_loader, val_data_loader)

        return history
