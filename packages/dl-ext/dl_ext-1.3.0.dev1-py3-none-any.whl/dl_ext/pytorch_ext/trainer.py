import logging
import math
import os
import sys
import time
from dataclasses import dataclass, field
from matplotlib import axes, figure
from tensorboardX import SummaryWriter
from termcolor import colored
from torch.nn import DataParallel
from torch.nn.parallel import DistributedDataParallel
from torch.optim import Adam
from torch.optim.lr_scheduler import _LRScheduler
from torch.optim.optimizer import Optimizer
from torch.utils.data import DataLoader, DistributedSampler
from tqdm import tqdm
from .sampler import OrderedDistributedSampler
from .dist import *
from .optim import *
from ..average_meter import AverageMeter
import matplotlib.pyplot as plt
import numpy as np
from .utils import *


@dataclass
class BaseTrainer:
    model: nn.Module
    train_dl: DataLoader
    valid_dl: DataLoader
    num_epochs: int
    loss_function: callable
    optimizer: Optimizer = None
    scheduler: _LRScheduler = None
    output_dir: str = 'models'
    max_lr: float = 1e-2
    weight_decay: float = 0.01
    save_every: bool = False
    metric_functions: dict = field(default_factory=dict)

    def __post_init__(self):
        os.makedirs(self.output_dir, exist_ok=True)
        self.begin_epoch = 0
        self.state = TrainerState.BASE
        self.layer_groups = [nn.Sequential(*flatten_model(self.model))]
        if self.optimizer is None:
            self.optimizer = self.create_default_optimizer()
        if self.scheduler is None:
            self.scheduler = ConstantScheduler(self.optimizer)
            # self.scheduler = OneCycleScheduler(self.optimizer, self.max_lr,
            #                                    total_steps=len(self.train_dl) * self.num_epochs)
        if is_main_process():
            self.tb_writer = SummaryWriter(self.output_dir, flush_secs=20)
        self.global_steps = 0
        self.best_val_loss = 100000
        self.logger = self._setup_logger()

    def create_default_optimizer(self):
        split_params = split_no_wd_params(self.layer_groups)
        optimizer = Adam([{'params': p, 'lr': self.max_lr,
                           'betas': (0.9, 0.99),
                           # 'weight_decay': self.weight_decay
                           } for p in split_params])
        return optimizer

    def train(self, epoch):
        loss_meter = AverageMeter()
        metric_ams = {}
        for metric in self.metric_functions.keys():
            metric_ams[metric] = AverageMeter()
        self.model.train()
        bar = tqdm(self.train_dl, leave=False) if is_main_process() else self.train_dl
        begin = time.time()
        for batch in bar:
            self.optimizer.zero_grad()
            x, y = batch_gpu(batch)
            output = self.model(x)
            loss = self.loss_function(output, y)
            loss = loss.mean()
            loss.backward()
            for pg1, pg2 in zip(self.optimizer.param_groups[::2], self.optimizer.param_groups[1::2]):
                for p in pg1['params']: p.data.mul_(1 - self.weight_decay * self.max_lr)
                for p in pg2['params']: p.data.mul_(1 - self.weight_decay * self.max_lr)
            self.optimizer.step()
            if isinstance(self.scheduler, OneCycleScheduler):
                self.scheduler.step()
            # record and plot loss and metrics
            reduced_loss = reduce_loss(loss)
            metrics = {}
            for metric, f in self.metric_functions.items():
                s = f(output, y).mean()
                reduced_s = reduce_loss(s)
                metrics[metric] = reduced_s
            if is_main_process():
                loss_meter.update(reduced_loss.item())
                lr = self.optimizer.param_groups[0]['lr']
                self.tb_writer.add_scalar('train/loss', reduced_loss.item(), self.global_steps)
                self.tb_writer.add_scalar('train/lr', lr, self.global_steps)
                bar_vals = {'epoch': epoch, 'phase': 'train', 'loss': loss_meter.avg, 'lr': lr}
                for k, v in metrics.items():
                    metric_ams[k].update(v.item())
                    self.tb_writer.add_scalar(f'train/{k}', v.item(), self.global_steps)
                    bar_vals[k] = metric_ams[k].avg
                bar.set_postfix(bar_vals)
            self.global_steps += 1
        torch.cuda.synchronize()
        epoch_time = format_time(time.time() - begin)
        if is_main_process():
            metric_msgs = ['epoch %d, train, loss %.4f, time %s' % (
                epoch, loss_meter.avg, epoch_time)]
            for metric, v in metric_ams.items():
                metric_msgs.append('%s %.4f' % (metric, v.avg))
            s = ', '.join(metric_msgs)
            self.logger.info(s)
        if not isinstance(self.scheduler, OneCycleScheduler):
            self.scheduler.step()

    @torch.no_grad()
    def val(self, epoch):
        loss_meter = AverageMeter()
        metric_ams = {}
        for metric in self.metric_functions.keys():
            metric_ams[metric] = AverageMeter()
        self.model.eval()
        bar = tqdm(self.valid_dl, leave=False) if is_main_process() else self.valid_dl
        begin = time.time()
        for batch in bar:
            x, y = batch_gpu(batch)
            output = self.model(x)
            loss = self.loss_function(output, y)
            loss = loss.mean()
            reduced_loss = reduce_loss(loss)
            metrics = {}
            for metric, f in self.metric_functions.items():
                s = f(output, y).mean()
                reduced_s = reduce_loss(s)
                metrics[metric] = reduced_s
            if is_main_process():
                loss_meter.update(reduced_loss.item())
                bar_vals = {'epoch': epoch, 'phase': 'val', 'loss': loss_meter.avg}
                for k, v in metrics.items():
                    metric_ams[k].update(v.item())
                    self.tb_writer.add_scalar(f'val/{k}', v.item(), epoch)
                    bar_vals[k] = metric_ams[k].avg
                bar.set_postfix(bar_vals)
        torch.cuda.synchronize()
        epoch_time = format_time(time.time() - begin)
        if is_main_process():
            metric_msgs = ['epoch %d, val, loss %.4f, time %s' % (
                epoch, loss_meter.avg, epoch_time)]
            for metric, v in metric_ams.items():
                metric_msgs.append('%s %.4f' % (metric, v.avg))
            s = ', '.join(metric_msgs)
            self.logger.info(s)
            self.tb_writer.add_scalar('val/loss', loss_meter.avg, epoch)
            for metric, s in metric_ams.items():
                self.tb_writer.add_scalar(f'val/{metric}', s.avg, epoch)
            return loss_meter.avg

    def fit(self):
        os.makedirs(self.output_dir, exist_ok=True)
        num_epochs = self.num_epochs
        begin = time.time()
        for epoch in range(self.begin_epoch, num_epochs):
            self.train(epoch)
            synchronize()
            val_loss = self.val(epoch)
            synchronize()
            if is_main_process():
                if self.save_every:
                    self.save(epoch)
                elif val_loss < self.best_val_loss:
                    self.logger.info(
                        colored('Better model found at epoch %d with val_loss %.4f.' % (epoch, val_loss), 'red'))
                    self.best_val_loss = val_loss
                    self.save(epoch)
            synchronize()
        if is_main_process():
            self.logger.info('Training finished. Total time %s' % (format_time(time.time() - begin)))

    @torch.no_grad()
    def get_preds(self, dataset='valid', with_target=False):
        if get_world_size() > 1:
            return self.get_preds_dist(dataset, with_target)
        self.model.eval()
        assert dataset in ['train', 'valid']
        if dataset == 'train':
            ordered_train_dl = DataLoader(self.train_dl.dataset, self.train_dl.batch_size, shuffle=False,
                                          sampler=None, num_workers=self.train_dl.num_workers,
                                          collate_fn=self.train_dl.collate_fn, pin_memory=self.train_dl.pin_memory,
                                          timeout=self.train_dl.timeout, worker_init_fn=self.train_dl.worker_init_fn)
            bar = tqdm(ordered_train_dl)
        else:
            ordered_valid_dl = DataLoader(self.valid_dl.dataset, self.valid_dl.batch_size, shuffle=False,
                                          sampler=None, num_workers=self.valid_dl.num_workers,
                                          collate_fn=self.valid_dl.collate_fn, pin_memory=self.valid_dl.pin_memory,
                                          timeout=self.valid_dl.timeout, worker_init_fn=self.valid_dl.worker_init_fn)
            bar = tqdm(ordered_valid_dl)
        outputs = []
        targets = []
        for batch in bar:
            x, y = batch_gpu(batch)
            output = self.model(x)
            output = to_cpu(output)
            outputs.append(output)
            if with_target:
                targets.append(to_cpu(y))
        outputs = torch.cat(outputs)
        if with_target:
            targets = torch.cat(targets)
            return outputs, targets
        else:
            return outputs

    @torch.no_grad()
    def get_preds_dist(self, dataset='valid', with_target=False):
        self.model.eval()
        if dataset == 'train':
            train_sampler = OrderedDistributedSampler(self.train_dl.dataset, get_world_size(), rank=get_rank())
            ordered_dist_train_dl = DataLoader(self.train_dl.dataset, self.train_dl.batch_size, shuffle=False,
                                               sampler=train_sampler, num_workers=self.train_dl.num_workers,
                                               collate_fn=self.train_dl.collate_fn, pin_memory=self.train_dl.pin_memory,
                                               timeout=self.train_dl.timeout,
                                               worker_init_fn=self.train_dl.worker_init_fn)
            bar = tqdm(ordered_dist_train_dl) if is_main_process() else ordered_dist_train_dl
        else:
            valid_sampler = OrderedDistributedSampler(self.valid_dl.dataset, get_world_size(), rank=get_rank())
            ordered_dist_valid_dl = DataLoader(self.valid_dl.dataset, self.valid_dl.batch_size, shuffle=False,
                                               sampler=valid_sampler, num_workers=self.valid_dl.num_workers,
                                               collate_fn=self.valid_dl.collate_fn, pin_memory=self.valid_dl.pin_memory,
                                               timeout=self.valid_dl.timeout,
                                               worker_init_fn=self.valid_dl.worker_init_fn)
            bar = tqdm(ordered_dist_valid_dl) if is_main_process() else ordered_dist_valid_dl
        outputs = []
        targets = []
        for batch in bar:
            x, y = batch_gpu(batch)
            output = self.model(x)
            output = to_cpu(output)
            outputs.append(output)
            if with_target:
                targets.append(to_cpu(y))
        outputs = torch.cat(outputs)
        all_outputs = all_gather(outputs)
        if with_target:
            targets = torch.cat(targets)
            all_targets = all_gather(targets)
        if not is_main_process():
            return
        all_outputs = torch.cat(all_outputs, dim=0).cpu()[:len(self.valid_dl.dataset)]
        if with_target:
            all_targets = torch.cat(all_targets, dim=0).cpu()[:len(self.valid_dl.dataset)]
            return all_outputs, all_targets
        else:
            return all_outputs

    def to_base(self):
        if self.state == TrainerState.BASE:
            return
        elif self.state == TrainerState.PARALLEL:
            self.model = self.model.module
            if isinstance(self.scheduler, OneCycleScheduler):
                world_size = get_world_size()
                self.scheduler.total_steps *= world_size
                self.scheduler.step_size_up *= world_size
                self.scheduler.step_size_down *= world_size
        else:
            self.model = self.model.module
            self.train_dl = self.old_train_dl
            self.valid_dl = self.old_valid_dl
            if isinstance(self.scheduler, OneCycleScheduler):
                world_size = get_world_size()
                self.scheduler.total_steps *= world_size
                self.scheduler.step_size_up *= world_size
                self.scheduler.step_size_down *= world_size

    def to_parallel(self):
        assert self.state == TrainerState.BASE
        devices = os.environ['CUDA_VISIBLE_DEVICES']
        print('visible devices', devices)
        self.model = DataParallel(self.model)
        if isinstance(self.scheduler, OneCycleScheduler):
            world_size = get_world_size()
            self.scheduler.total_steps //= world_size
            self.scheduler.step_size_up //= world_size
            self.scheduler.step_size_down //= world_size

    def to_distributed(self):
        assert dist.is_available() and dist.is_initialized()
        local_rank = dist.get_rank()
        self.model = DistributedDataParallel(self.model, [local_rank],
                                             output_device=local_rank,
                                             broadcast_buffers=False)
        self.old_train_dl = self.train_dl
        train_sampler = DistributedSampler(self.train_dl.dataset, shuffle=True)
        new_train_dl = DataLoader(self.train_dl.dataset, self.train_dl.batch_size, shuffle=False,
                                  sampler=train_sampler, num_workers=self.train_dl.num_workers,
                                  collate_fn=self.train_dl.collate_fn, pin_memory=self.train_dl.pin_memory,
                                  timeout=self.train_dl.timeout, worker_init_fn=self.train_dl.worker_init_fn)
        self.train_dl = new_train_dl
        self.old_valid_dl = self.valid_dl
        valid_sampler = DistributedSampler(self.valid_dl.dataset, shuffle=False)
        new_valid_dl = DataLoader(self.valid_dl.dataset, self.valid_dl.batch_size, shuffle=False,
                                  sampler=valid_sampler, num_workers=self.valid_dl.num_workers,
                                  collate_fn=self.valid_dl.collate_fn, pin_memory=self.valid_dl.pin_memory,
                                  timeout=self.valid_dl.timeout, worker_init_fn=self.valid_dl.worker_init_fn)
        self.valid_dl = new_valid_dl
        if isinstance(self.scheduler, OneCycleScheduler):
            world_size = get_world_size()
            self.scheduler.total_steps /= world_size
            self.scheduler.step_size_up /= world_size
            self.scheduler.step_size_down /= world_size

    def find_lr(self, start_lr: float = 1e-7, end_lr: float = 10,
                num_it: int = 100, stop_div: bool = True,
                skip_start: int = 10, skip_end: int = 5, suggestion: bool = False):
        assert self.state == TrainerState.BASE
        # assert len(self.train_dl) >= num_it
        self.old_scheduler = self.scheduler
        self.scheduler = LRFinder(self.optimizer, start_lr, end_lr, num_it, stop_div)
        loss_meter = AverageMeter()
        self.model.train()

        it = 0
        lrs, smooth_losses = [], []
        for epoch in range(round(math.ceil(num_it / len(self.train_dl)))):
            bar = tqdm(self.train_dl, leave=False)
            for batch in bar:
                if it > num_it: break
                self.optimizer.zero_grad()
                x, y = batch_gpu(batch)
                output = self.model(x)
                loss = self.loss_function(output, y)
                loss = loss.mean()
                loss.backward()
                self.optimizer.step()
                self.scheduler.step()
                # record and plot loss and metrics
                loss_meter.update(loss.item())
                lr = self.optimizer.param_groups[0]['lr']
                lrs.append(lr)
                smooth_losses.append(loss_meter.avg)
                bar_vals = {'it': it, 'phase': 'train', 'loss': loss_meter.avg, 'lr': lr}
                bar.set_postfix(bar_vals)
                it += 1
        lrs = split_list(lrs, skip_start, skip_end)
        losses = split_list(smooth_losses, skip_start, skip_end)
        fig, ax = plt.subplots(1, 1)
        ax.plot(lrs, losses)
        ax.set_ylabel("Loss")
        ax.set_xlabel("Learning Rate")
        ax.set_xscale('log')
        ax.xaxis.set_major_formatter(plt.FormatStrFormatter('%.0e'))
        if suggestion:
            try:
                mg = (np.gradient(np.array(losses))).argmin()
            except:
                print("Failed to compute the gradients, there might not be enough points.")
                return
            print(f"Min numerical gradient: {lrs[mg]:.2E}")
            ax.plot(lrs[mg], losses[mg], markersize=10, marker='o', color='red')
            ml = np.argmin(losses)
            print(f"Min loss divided by 10: {lrs[ml] / 10:.2E}")
        fig: figure.Figure
        ax: axes.Axes
        fig.savefig(os.path.join(self.output_dir, 'lr.jpg'))
        # reset scheduler
        self.scheduler = self.old_scheduler

    def save(self, epoch):
        name = os.path.join(self.output_dir, str(epoch) + '.pth')
        net_sd = self.model.module.state_dict() if hasattr(self.model, 'module') else self.model.state_dict()
        d = {'model': net_sd,
             'optimizer': self.optimizer.state_dict(),
             'scheduler': self.scheduler.state_dict(),
             'epoch': epoch,
             'best_val_loss': self.best_val_loss}
        torch.save(d, name)

    def load(self, name):
        name = os.path.join(self.output_dir, name + '.pth')
        d = torch.load(name, 'cpu')
        net_sd = d['model']
        if hasattr(self.model, 'module'):
            self.model.module.load_state_dict(net_sd)
        else:
            self.model.load_state_dict(net_sd)
        self.optimizer.load_state_dict(d['optimizer'])
        self.scheduler.load_state_dict(d['scheduler'])
        self.begin_epoch = d['epoch']
        self.best_val_loss = d['best_val_loss']

    def _setup_logger(self):
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.DEBUG)
        # don't log results for the non-master process
        if get_rank() > 0:
            return logger
        ch = logging.StreamHandler(stream=sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        fh = logging.FileHandler(os.path.join(self.output_dir, 'log.txt'))
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger

    @property
    def tb_writer(self):
        return self._tb_writer

    @tb_writer.setter
    def tb_writer(self, value):
        self._tb_writer = value
