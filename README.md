# HD-SEQ-ID

## HD-SEQ-ID: HD Sequence Identifier for brain MRI


This repository provides an easy to use Python Tool to our recently published "HD-SEQ-ID" automated brain MRI sequence identification tool. 

If you are using HD-SEQ-ID, please cite the following publication: 


- Mahmutoglu MA, Preetha CJ, Meredig H, Tonn J-C, Weller M, Wick W, Bendszus M, Brugnara G, Vollmuth P. Deep Learning-based Identification of Brain MRI Sequences Using a Model Trained on Large Multicentric Study Cohorts. Radiology AI, 2023
  https://doi.org/10.1148/ryai.230095




Compared to other previously published brain MRI (cMRI) sequence classification tools, HD-SEQ-ID has some significant advantages:
- HD-SEQ-ID was developed with MRI-data from four large multicentric clinical trials in adult brain tumor patients acquired 
up to 249 institutions  and included a broad range of MR hardware and acquisition parameters, pathologies 
or treatment-induced tissue alterations. We used 80% of data for training and validation and 20% for testing. 

- HD-SEQ-ID was trained with following brain MRI sequence types:  precontrast T1-w (T1), postcontrast T1-w (CT1), T2-w (T2), fluid-attenuated inversion recovery (FLAIR), susceptibility weighted imaging (SWI), apparent diffusion coefficient (ADC), diffusion weighted imaging with low b-values (Low-B-DWI) and high b-vlaues (High-B-DWI), T2* and DSC-related sequence types (T2star-DSCrelated) including different perfusion parameters such as CBV, CBVc, CBF, TTP, K2, MTT, TMAX. TTP. Note that the "T2star-DSCrelated" class cannot differentiate between separate perfusion parameters, they all will be labeled as "T2star-DSCrelated".

- HD-SEQ-ID can identify 9 differents cMRI classes from raw NIfTI files and raneme the file automatically (T1, CT1, T2, FLAIR, SWI, ADC, Low-B-DWI, High-B-DWI, T2*/DSC-related). Sequence types that are not included in the training, e.g. time of flight angiography (TOF) or Scout, are going to be assigned to one of the 9 classes wrongly, we therefore strongly encourage to use our model on tumor protocols, and compare the output predictions prior to further analysis.

- HD-SEQ-ID outperformed most publicly available brain extraction algorithms (see Mahmutoglu et al. 2023).

- HD-SEQ-ID can differentiate between DWI images according to their low and high b-values. To the best of our knowledge, this is the first Python tool for this task. HD-SEQ-ID can also identify SWI class (apart from T2*-w). 



# Installation Instructions 
There are two options to use the HD-SEQ-ID tool. 

## 1) Creating a new python environment

Note that you need to have a python3 installation for HD-SEQ-ID to work. HD-SEQ-ID runs on Linux (might work on WSL) with python3. Supported python3 versions are python3.7.3 and above. 
 
Please also make sure to install FSL on your Linux operating system or WSL command line. To install FSL please visit their homepage:

<sup>1</sup>https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation



### Manual installation
We generally recommend to create a new virtualenv for every project that is installed so that package dependencies don't get mixed.
In case you encounter dependency issues, try to install the versions of the packages in the below mentioned .yml file one-by-one.

#### Installing with a virtualenv
We recommend to create a new environment using the `hd-seq-id_environment.yml` file attached to this repository.

```shell
# With .yml file
git clone https://github.com/NeuroAI-HD/HD-SEQ-ID.git  # Clones the Repository
cd HD-SEQ-ID # Enter the downloaded HD-SEQ-ID folder
conda env create --name <ENVNAME> --file=hd-seq-id_environment.yml  # Creates a new Virtual environment via installing all required packages. <ENVNAME> should be specified by user.
conda activate <ENVNAME>  # Activates the environment

```


# How to use it 

You can use HD-SEQ-ID in any terminal on your linux system or WSL command line. The `hd_seq_id` command was installed 
automatically. We provide CPU as well as GPU support. Running on GPU is a lot faster and should always be preferred. 
Make sure you have empty space on your disk at least as much as the input files you want to rename.


- Download the models from the follwing link:
<sup>2</sup>https://drive.google.com/drive/folders/1reSTwPgMfb7AXC9sfNJHW9b3_uIBS0AY?usp=sharing

Define a `<MODELS_FOLDER>`, where the 5 `.pth` files are downloaded. It will be used as an input argument by running the `hd_seq_id` command.

- Note that the `hd_seq_id` command should be run inside the `HD-SEQ-ID` folder, check your current working directory before running. 

Define an `<INPUT_FOLDER>`, where all NIfTI images are located (4D or 3D). Define an empty `<OUTPUT_FOLDER>`, where the 3D NIfTI files, where the processed and renamed 3D NIfTIs will be located. They will be used as an input argument by running the `hd_seq_id` command.   

- NIfTI file names will remain fully and the output label will be added to the end of the basename. 
 
For example: If a `~/MAINFOLDER/SUBFOLDER/random_NIfTI_name.nii.gz` file is predicted as a FLAIR image, the new name in the output folder will be `~/MAINFOLDER/SUBFOLDER/random_NIfTI_name____FLAIR.nii.gz`. If the `random_NIfTI_name` part should be deleted, it can be done using simple pipelines in various programming languages. The `hd_seq_id` does not delete the initial basename of the NIfTI file, since if multiple NIfTIs will be present in the same subfolder (input folder or output folder, 4D files input files might be splitted into two different 3D files in the output folder), and if multiple NIfTIs receive the same predicted MRI label, it will result by unintentional removing of the first renamed NIfTI file by replacing it with the other NIfTI file, which receives the same label. For example, Ubuntu would delete the first `~/FLAIR.nii.gz` in the same folder, if the second NIfTI should be named as `FLAIR.nii.gz` as well. 


Here is a minimalistic example of how you can use HD-SEQ-ID. 

```bash
python hd_seq_id -i <INPUT_FOLDER> -o <OUTPUT_FOLDER> -m <MODELS_FOLDER>
```

The above command will look for all nifti files (*.nii.gz) in the INPUT_FOLDER and save the renamed NIfTI files in THE OUTPUT_FOLDER with the predicted MRI labels added as a suffix to the NIfTI basename: `*____<predicted-label>.nii.gz` 

Predictions will be exported as a CSV file in the output folder named as `predictions.csv`. We encourage to compare them with the ground truth labels prior to further analysis. 

Future versions might include parameters to specifiy whether an automated renaming is wished by user (might output a list of the MRI classes without renaming the original NIfTI files), a docker version to avoid compatibility issues and a script for quick visual controlling the output predictions.



## 2) Docker file

Download the docker file (~28GB).

```bash
docker pull neuroradhd/hd_seq_id
```

Create a parent folder (for example a folder named as `mount_folder` ) which includes the folders `input`, `output` and `code`. Copy the `run.sh` file into the `code` folder.
Run the following command to mount the parent folder and run the HD-SEQ-ID. 

```bash
docker run -it --name hd-seq-id-container --gpus all --mount type=bind,source="<mount_folder>",target=/mnt/ hd_seq_id:v2  /bin/bash -c "/mnt/code/run.sh"
```
By default, `prediction.csv` file will be created without renaming the input files. You can create renamed output `.nii.gz` files by changing the last line of the code, as in the example below:

```bash
python3 hd_seq_id -i /mnt/input/ -o /mnt/output/ -m models/ -write False  # This will create a prediction.csv file in the output folder without creating renamed NIfTI files.
python3 hd_seq_id -i /mnt/input/ -o /mnt/output/ -m models/ -write True  # This will create a prediction.csv file and  renamed NIfTI files (by adding the predicted MRI sequence name as a suffix [see above]) in the output folder. 
```

If you're using the docker version, you don't need to install the weights manually, they are already in the docker image.


## FAQ

1) **How much GPU memory do I need to run HD-BET?**  
We ran all our experiments on NVIDIA GeForce RTX 3060 and NVIDIA Titan X GPUs with 12 GB memory. For inference you will need less, but since 
inference in implemented by exploiting the fully convolutional nature of CNNs the amount of memory required depends on 
your image. Typical image should run with less than 4 GB of GPU memory consumption.

2) **Will you provide the training code as well?**  
No. The training code is tightly wound around the data which we cannot make public.

3) **What run time can I expect on CPU/GPU?**  
This depends on your MRI image size. Typical run times (preprocessing, postprocessing and renaming included) are just
 a couple of seconds for GPU.
 
 
