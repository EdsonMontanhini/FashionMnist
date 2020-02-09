import numpy as np
import torch
from utils.logger import logger

"""
original code from: https://github.com/Bjarten/early-stopping-pytorch/blob/master/pytorchtools.py
modified to save model with custom model name depending on runs
replaced prints with logs 
"""


class EarlyStopping:
    """Early stops the training if validation loss doesn't improve after a given patience."""

    def __init__(self, patience=7, verbose=False, delta=0):
        """
        Args:
            patience (int): How long to wait after last time validation loss improved.
                            Default: 7
            verbose (bool): If True, prints a message for each validation loss improvement.
                            Default: False
            delta (float): Minimum change in the monitored quantity to qualify as an improvement.
                            Default: 0
        """
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.val_loss_min = np.Inf
        self.delta = delta
        self.logger = logger().get_logger(logger_name='Advertima early stoppinglogs')

    def __call__(self, val_loss, model, model_path):

        score = -val_loss

        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(val_loss, model, model_path)
        elif score < self.best_score + self.delta:
            self.counter += 1
            self.logger.info('EarlyStopping counter: {} out of {}'.format(self.counter, self.patience))
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.save_checkpoint(val_loss, model, model_path)
            self.counter = 0

    def save_checkpoint(self, val_loss, model, model_path):
        """Saves model when validation loss decrease."""
        if self.verbose:
           self.logger.info('Validation loss decreased from {:.3f} to {:.3f} ==> update model weights...'.format(self.val_loss_min, val_loss))
        torch.save(model.state_dict(), model_path)
        self.val_loss_min = val_loss
