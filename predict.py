

#scikit-learn must be at version <= 0.17

import os
import argparse
import numpy 
import random
import cv2
import time
import matplotlib.pyplot as plt
import pandas as pd

import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
import torchvision

import nibabel

import shutil
import tempfile
import matplotlib.pyplot as plt
import PIL
import torch
import numpy as np
from sklearn.metrics import classification_report

import monai
from monai.apps import download_and_extract
from monai.config import print_config
from monai.data import decollate_batch
from monai.metrics import ROCAUCMetric
from monai.networks.nets import DenseNet121
from monai.transforms import (
    Activations,
    AddChannel,
    AsDiscrete,
    Compose,
    LoadImage,
    CropForeground,
    RandGaussianNoise,
    RandFlip,
    RandRotate,
    RandZoom,
    ScaleIntensity,
    NormalizeIntensity,
    EnsureType,
)
from monai.utils import set_determinism

from monai.data import ImageDataset
from monai.transforms import AddChannel, Compose, RandRotate90, Resize, ScaleIntensity, EnsureType

import SimpleITK as sitk
import re

import logging
import sys

import numpy as np
import torch
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter


#%%
def fix_random_seeds():
	torch.backends.cudnn.deterministic = True
	random.seed(1)
	torch.manual_seed(1)
	torch.cuda.manual_seed(1)
	numpy.random.seed(1)
    
fix_random_seeds()
set_determinism(seed=1)

def seed_worker(worker_id):
    worker_seed = torch.initial_seed() 
    numpy.random.seed(worker_seed)
    random.seed(worker_seed)

g = torch.Generator()
g.manual_seed(1)


#%% Define transforms

test_transforms = Compose([AddChannel(), Resize((200, 200, 1)), NormalizeIntensity(), EnsureType()])
test_transforms.set_random_state(seed=1)


#%% Define resnet18

def resnet18(n_slices = 1, num_classes = 9):
 	
 	net = torchvision.models.resnet18(num_classes = num_classes)
 	net.conv1 = nn.Conv2d(n_slices, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
# 	net.layer3 = nn.Identity() 
# 	net.layer4 = nn.Identity()
 	net.fc = nn.Linear(in_features = 512, out_features = 9, bias = True)
 	return net


#%%
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


#%% Upload model weights

model_1 = resnet18(n_slices = 1, num_classes = 9)
model_1 = model_1.to(device)
model_1.load_state_dict(torch.load('resnet18_best_models/WIN__best-metric__resnet18__Fold_1_epoch_41_2022-12-13.pth')) #, map_location='cuda'
time.sleep(1)
model_1.eval()


#%%

model_2 = resnet18(n_slices = 1, num_classes = 9)
model_2 = model_2.to(device)
model_2.load_state_dict(torch.load('resnet18_best_models/WIN__best-metric__resnet18__Fold_2_epoch_47_2022-12-13.pth')) #, map_location='cuda'
time.sleep(1)
model_2.eval()

#%%

model_3 = resnet18(n_slices = 1, num_classes = 9)
model_3 = model_3.to(device)
model_3.load_state_dict(torch.load('resnet18_best_models/WIN__best-metric__resnet18__Fold_3_epoch_29_2022-12-13.pth')) #, map_location='cuda'
time.sleep(1)
model_3.eval()

#%%

model_4 = resnet18(n_slices = 1, num_classes = 9)
model_4 = model_4.to(device)
model_4.load_state_dict(torch.load('resnet18_best_models/WIN__best-metric__resnet18__Fold_4_epoch_46_2022-12-15.pth')) #, map_location='cuda'
time.sleep(1)
model_4.eval()

#%%
model_5 = resnet18(n_slices = 1, num_classes = 9)
model_5 = model_5.to(device)
model_5.load_state_dict(torch.load('resnet18_best_models/WIN__best-metric__resnet18__Fold_5_epoch_48_2022-12-15.pth')) #, map_location='cuda'
time.sleep(1)
model_5.eval()

#%%

models = [model_1,model_2,model_3,model_4,model_5]

#%%

ensamble_voter = monai.transforms.VoteEnsemble(num_classes=9)


#%%

from preprocessing import process_midslice

def hd_seq_id(input_dir,output_dir):
    
    filenames_all = process_midslice(input_dir, output_dir)
    
    midslice_images = []
    output3d_images = []
    for i in range(len(filenames_all)):
        print(i)
        midslice_images.append(re.sub("\\\\", "/", filenames_all[i][2]))
        output3d_images.append(re.sub("\\\\", "/", filenames_all[i][1]))
        
    # Test ImageDataset
    x_test_fold = np.array(midslice_images)
    test_ds_fold = ImageDataset(image_files=x_test_fold, transform=test_transforms)
    
    dict_labels = {0:'Other', 1:'T1', 2:'T2', 3:'CT1', 4:'FLAIR', 5:'ADC', 6:'SWI', 7:'Low-B-DWI', 8:'High-B-DWI', 9:'UNKNOWN'}
    
    predictions_list = []
    with torch.no_grad():
        
        for i in range(len(test_ds_fold)):
            # break
            try:
                listo = [model_1(test_ds_fold[i].to(device).unsqueeze(0).squeeze(-1)).argmax(),
                         model_2(test_ds_fold[i].to(device).unsqueeze(0).squeeze(-1)).argmax(),
                         model_3(test_ds_fold[i].to(device).unsqueeze(0).squeeze(-1)).argmax(),
                         model_4(test_ds_fold[i].to(device).unsqueeze(0).squeeze(-1)).argmax(),
                         model_5(test_ds_fold[i].to(device).unsqueeze(0).squeeze(-1)).argmax()]
        
                    
                predicted_label = ensamble_voter(listo)
                predictions_list.append(int(predicted_label.cpu()))

                print(int(predicted_label.cpu()))
                
            except:
                predictions_list.append(int(9))
                print("an error occured, check model weights...")
    
    
    for k in range(len(output3d_images)):
        mid_image_nib = nibabel.load(output3d_images[k])
        os.unlink(midslice_images[k])
        
        if rename==1:
            out_newname = re.sub(os.path.basename(output3d_images[k]), dict_labels[predictions_list[k]] +'.nii.gz',output3d_images[k]) 
            try:
                nibabel.save(mid_image_nib, out_newname)
            except:
                print('an error occured at ==>   try: new_image = nibabel.Nifti1Image(img_midslice_new, affine=robust_3d_img.affine)')
        elif rename==0:
            out_newname = re.sub('.nii.gz','_'+dict_labels[predictions_list[k]]+'.nii.gz',output3d_images[k]) 
            try:
                nibabel.save(mid_image_nib, out_newname)
            except:
                print('an error occured at ==>   try: new_image = nibabel.Nifti1Image(img_midslice_new, affine=robust_3d_img.affine)')
        else: 
            print('unknown error')


#%% Define args


if __name__ == "__main__":
    
    import argparse
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-i', '--input', default='', help='input. Should be an input folder containing 4d or 3d NIfTI images, all files ending with .nii.gz. '
                                       'Subfolder structure is irrelevant ', required=False, type=str)
    
    parser.add_argument('-o', '--output', help='output. Should be a folder. If it does not exist, the folder'
                                     ' will be created', required=False, type=str)
    
    parser.add_argument('--overwrite', default=1, type=int, required=False, help="set this to 0 if you don't "
                                                                                          "want to overwrite original image file name. "
                                                                                          "The predicted label will be added to the original "
                                                                                          "image name as a suffix, for example: <original_name>_<predicted_name>.nii.gz")
    
    args = parser.parse_args()
    
    input_dir = args.input
    output_dir = args.output
    
    rename = args.overwrite
    
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(input_dir), os.path.basename(input_dir) + "_OUTPUT")
    
    if os.path.isdir(input_dir):
        input_files = []
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.endswith(".nii.gz"):
                    input_files.append(os.path.join(root, file))

        if len(input_files) == 0:
            raise RuntimeError("input is a folder but no nifti files (.nii.gz) were found in here")

        input_files = [os.path.join(input_dir, i) for i in input_files]
    else:
        "Check input folder..."


    ### Start postprocessing ###

    hd_seq_id(input_dir,output_dir) 
            
    









