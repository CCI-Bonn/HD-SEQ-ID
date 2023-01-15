# HD-SEQ-ID
HD-SEQ-ID: HD Sequence Identifier for brain MRI


This repository provides an easy to use Python Tool to our recently published "HD-SEQ-ID" automated brain MRI sequence identification tool. 

If you are using HD-SEQ-ID, please cite the following publication: 

Mahmutoglu MA,...


Compared to other previously published brain MRI (cMRI) sequence classification tools, HD-SEQ-ID has some significant advantages:
- HD-SEQ-ID was developed with MRI-data from four large multicentric clinical trials in adult brain tumor patients acquired 
up to 249 institutions  and included a broad range of MR hardware and acquisition parameters, pathologies 
or treatment-induced tissue alterations. We used 80% of data for training and validation and 20% for testing. 

- HD-SEQ-ID was trained with following braim MRI sequence types:  precontrast T1-w (T1), postcontrast T1-w (CT1), T2-w (T2), fluid-attenuated inversion recovery (FLAIR), susceptibility weighted imaging (SWI), apparent diffusion coefficient (ADC), diffusion weighted imaging with low b-values (Low-B-DWI) and high b-vlaues (High-B-DWI).   

- HD-SEQ-ID can identify 8 differents cMRI classes from raw NIfTI files and raneme the file automatically. 

- HD-SEQ-ID outperformed most publicly available brain extraction algorithms (see Mahmutoglu et al. 2023).

- HD-SEQ-ID can differentiate between DWI images according to their low and high b-values. To the best of our knowledge, this is the first Python tool for this task. HD-SEQ-ID can also identify SWI class (apart from T2*-w). 



## Installation Instructions 
Note that you need to have a python3 installation for HD-SEQ-ID to work. HD-SEQ-ID runs on Linux (might work on WSL) with python3. Supported python3 versions are python3.7.3 and above, might work with 3.9 as well. 

In order to run a PC with a GPU with at least 4 GB of VRAM and cuda/pytorch support is required. Running the prediction on CPU is also supported.
 
Please also make sure to install FSL on your Linux operating system or WSL command line. To install FSL please visit their homepage:

<sup>1</sup>https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation



### Manual installation
We generally recommend to create a new virtualenv for every project that is installed so package dependencies don't get mixed.

#### Installing with a virtualenv
We recommend to create a new environment using the `hd-seq-id_environment.yml` file attached to this repository.

```shell
# With .yml file
conda env create --name <ENVNAME> --file=environments.yml  # Creates a new Virtual environment via installing all required packages. <ENVNAME> should be specified by user.
conda env <ENVNAME>  # Activates the environment

git clone .............git  # Clones the Repository
pip install HD-SEQ-ID/  # Install the repository for the current virtualenv
```


## How to use it 

Using HD-SEQ-ID is straightforward. You can use it in any terminal on your linux system or WSL command line. The `hd_seq_id` command was installed 
automatically. We provide CPU as well as GPU support. Running on GPU is a lot faster and should always be preferred. 

- Download the following folder named `resnet18_best_models` inside the `HD-SEQ-ID` folder. If downloading the models one-by-one, make sure that all models are located in `HD-SEQ-ID/resnet18_best_models`.
<sup>2</sup>https://drive.google.com/drive/folders/1reSTwPgMfb7AXC9sfNJHW9b3_uIBS0AY?usp=sharing

- Note that the `hd_seq_id` command should be run inside the `HED-SEQ-ID` folder, check your current working directory before running. 

Here is a minimalistic example of how you can use HD-SEQ-ID. 

```bash
hd_seq_id -i INPUT_FOLDER -o OUTPUT_FOLDER
```

The above command will look for all nifti files (*.nii.gz) in the INPUT_FOLDER and save the renamed NIfTI files under in OUTPUT_FOLDER.

Future versions might include parameters to specifiy whether an automated renaming is wished by user (might output a list of the MRI classes without renaming the original NIfTI files).


### More options:
For more information, please refer to the help functionality:

```bash
hd_seq_id --help
```

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
 
 
