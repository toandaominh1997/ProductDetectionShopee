import os
import numpy as np
import pandas as pd
from PIL import Image
import cv2
import torch
from torch.utils.data import Dataset
import torchvision as tv
from datasets import Augment


class shopeeDataset(Dataset):
    def __init__(self, df, height=320, width=320,phase='train'):
        super(shopeeDataset, self).__init__()
        self.df = df
        self.df = self.df.reset_index()
        self.phase = phase
        self.root_path = {}
        if self.phase =='train' or self.phase=='valid':
            self.root_path['train'] = './datas/train/train'
            self.root_path['test'] = './datas/test/test'
        else:
            self.root_path = './datas/test/test'
        self.transform = Augment(phase=self.phase, height=height, width=height)


    def __len__(self):
        return len(self.df)
    def __getitem__(self, idx):
        file_name = self.df.loc[idx, 'filename']
        if self.phase == 'train' or self.phase == 'valid':
            target = self.df.loc[idx, 'category']
            # flag = self.df.loc[idx, 'path']
            flag = 'train'
            image_path = os.path.join(self.root_path[flag], self.num2str(target, flag), file_name)
        else:
            image_path = os.path.join(self.root_path, file_name)

            # img = cv2.imread(image_path, cv2.IMREAD_COLOR)

        img = Image.open(image_path).convert('RGB')
        (w, h) = img.size
        if self.phase == 'train':
            img = np.asarray(img)
        # img = np.asarray(img)
        if self.phase=='train':
            if w < 60 or h < 60:
                print('Error image small')
                return self[np.random.choice(len(self.df))]
        if self.transform is not None:
            img = self.transform(img)
        if self.phase=='train' or self.phase=='valid':
            target = np.array(target)
            target = torch.from_numpy(target)
            return img, target
        else:
            return img

    @staticmethod
    def num2str(x, flag):
        if flag == 'test':
            return ''
        ans = ''
        if(len(str(x))==1):
            ans = '0'+str(x)
        else:
            ans = str(x)
        return ans
