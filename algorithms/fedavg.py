import copy
import numpy as np

import torch
import torch.nn as nn
import sys
sys.path.append(r"/home/lhh/v0/")
import exchange
import json
import pickle

from utils import Averager
from utils import count_acc
from utils import append_to_logs
from utils import format_logs

from tools import construct_dataloaders
from tools import construct_optimizer
from networks.basic_nets import VGG


class FedAvg():
    def __init__(
        self, csets, gset, model, args
    ):
        self.csets = csets
        self.gset = gset
        self.model = model
        self.args = args

        self.clients = list(csets.keys())

        # construct dataloaders
        self.train_loaders, self.test_loaders, self.glo_test_loader = \
            construct_dataloaders(
                self.clients, self.csets, self.gset, self.args
            )

        self.logs = {
            "ROUNDS": [],
            "LOSSES": [],
            "GLO_TACCS": [],
            "LOCAL_TACCS": [],
        }

    def train(self):
        # Training
        for r in range(1, self.args.max_round + 1):
            n_sam_clients = int(self.args.c_ratio * len(self.clients))
            sam_clients = np.random.choice(
                self.clients, n_sam_clients, replace=False
            )

            local_models = {}

            avg_loss = Averager()
            all_per_accs = []
            
            if(r == 1):
                for client in sam_clients:
                    local_model, per_accs, loss = self.update_local(
                        r=r,
                        model=copy.deepcopy(self.model), #此处每次深拷贝全局模型
                        train_loader=self.train_loaders[client],
                        test_loader=self.test_loaders[client],
                    )

                    local_models[client] = copy.deepcopy(local_model)
                    avg_loss.add(loss)
                    all_per_accs.append(per_accs)
                
            if(r != 1):
                for client in sam_clients:
                    local_model, per_accs, loss = self.update_local(
                        r=r,
                        #model=copy.deepcopy(self.model), #此处每次深拷贝全局模型
                        model=copy.deepcopy(self.get_global_model()),
                        train_loader=self.train_loaders[client],
                        test_loader=self.test_loaders[client],
                    )

                    local_models[client] = copy.deepcopy(local_model)
                    avg_loss.add(loss)
                    all_per_accs.append(per_accs) 

            #打印本地模型字典
            print('本地模型字典如下:')
            print(local_models)

            train_loss = avg_loss.item()
            per_accs = list(np.array(all_per_accs).mean(axis=0))

            #得到全局模型
            global_model = self.update_global(
                r=r,
                global_model=self.model,
                local_models=local_models,
            )

            #打印全局模型
            print('全局模型如下:')
            print(global_model)
            self.upload_global_model(global_model)

            if r % self.args.test_round == 0:
                # global test loader
                glo_test_acc = self.test(
                    model=self.model,
                    loader=self.glo_test_loader,
                )

                # add to log
                self.logs["ROUNDS"].append(r)
                self.logs["LOSSES"].append(train_loss)
                self.logs["GLO_TACCS"].append(glo_test_acc)
                self.logs["LOCAL_TACCS"].extend(per_accs)

                # 打印全局模型是否更新
                print('self.model == global_model:')
                print(self.model == global_model)

                print("[R:{}] [Ls:{}] [TeAc:{}] [PAcBeg:{} PAcAft:{}]".format(
                    r, train_loss, glo_test_acc, per_accs[0], per_accs[-1]
                ))





    def update_local(self, r, model, train_loader, test_loader):
        # lr = min(r / 10.0, 1.0) * self.args.lr
        lr = self.args.lr

        optimizer = construct_optimizer(
            model, lr, self.args
        )

        if self.args.local_steps is not None:
            n_total_bs = self.args.local_steps
        elif self.args.local_epochs is not None:
            n_total_bs = max(
                int(self.args.local_epochs * len(train_loader)), 5
            )
        else:
            raise ValueError(
                "local_steps and local_epochs must not be None together"
            )

        model.train()

        loader_iter = iter(train_loader)

        avg_loss = Averager()
        per_accs = []

        for t in range(n_total_bs + 1):
            if t in [0, n_total_bs]:
                per_acc = self.test(
                    model=model,
                    loader=test_loader,
                )
                per_accs.append(per_acc)

            if t >= n_total_bs:
                break

            model.train()
            try:
                batch_x, batch_y = next(loader_iter)
            except Exception:
                loader_iter = iter(train_loader)
                batch_x, batch_y = next(loader_iter)

            if self.args.cuda:
                batch_x, batch_y = batch_x.cuda(), batch_y.cuda()

            hs, logits = model(batch_x)

            criterion = nn.CrossEntropyLoss()
            loss = criterion(logits, batch_y)

            optimizer.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(
                model.parameters(), self.args.max_grad_norm
            )
            optimizer.step()

            avg_loss.add(loss.item())

        loss = avg_loss.item()
        return model, per_accs, loss

    def update_global(self, r, global_model, local_models):
        mean_state_dict = {}

        for name, param in global_model.state_dict().items():
            vs = []
            for client in local_models.keys():
                vs.append(local_models[client].state_dict()[name])
            vs = torch.stack(vs, dim=0)

            try:
                mean_value = vs.mean(dim=0)
            except Exception:
                # for BN's cnt
                mean_value = (1.0 * vs).mean(dim=0).long()
            mean_state_dict[name] = mean_value

        global_model.load_state_dict(mean_state_dict, strict=False)
        
        return global_model

    def test(self, model, loader):
        model.eval()

        acc_avg = Averager()

        with torch.no_grad():
            for i, (batch_x, batch_y) in enumerate(loader):
                if self.args.cuda:
                    batch_x, batch_y = batch_x.cuda(), batch_y.cuda()
                _, logits = model(batch_x)
                acc = count_acc(logits, batch_y)
                acc_avg.add(acc)

        acc = acc_avg.item()
        return acc

    def save_logs(self, fpath):
        all_logs_str = []
        all_logs_str.append(str(self.args))

        logs_str = format_logs(self.logs)
        all_logs_str.extend(logs_str)

        append_to_logs(fpath, all_logs_str)

    '''def upload_global_model(self, global_model):
        # 调用 to_dict 方法将 VGG 对象转换为字典
        vgg_dict = global_model.to_dict()
        str = json.dumps(vgg_dict, indent=2)
        exchange.save(str)

    def get_global_model(str):
        str = exchange.getPath()
        vgg_dict = json.loads(str)
        model = VGG.from_dict(vgg_dict)
        return model'''
        
    def upload_global_model(self, global_model):
        vgg_str = pickle.dumps(global_model)
        with open('vgg_model.pkl', 'wb') as file:
            file.write(vgg_str)
        exchange.save('vgg_model.pkl')

    def get_global_model(str):
        str = exchange.getpath()
        with open(str, 'rb') as file:
            loaded_vgg_str = file.read()
            model = pickle.loads(loaded_vgg_str)
        return model
        
