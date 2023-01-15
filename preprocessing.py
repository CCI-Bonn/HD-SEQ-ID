import pandas as pd
import numpy as np
import glob
import os
import re
import nibabel
import scipy.ndimage
import numpy



#%% Create Midslice using LASTVOL, RobustFOV and 'CM'


image_4d_3d_2d_file_names = []
image_files_list = []
image_midslice_list = []


#%%


def process_midslice(INPUTPATH='', OUTPUTPATH=''):
    
    input_images = []
    for root, dirs, files in os.walk(INPUTPATH):
        for file in files:
            if file.endswith(".nii.gz"):
                input_images.append(os.path.join(root, file))
    
    renamed_niftis = []
    for i in range(len(input_images)):
        renamed_niftis.append(re.sub("\\\\","/",input_images[i]))
        
    input_images = renamed_niftis 
    
    
    for i in range(len(input_images)):
        image_files_list.append(input_images[i])
        print(i,"   ",(i/(len(input_images))*100)," % ","     ","\n",input_images[i])
        
        try:
            img = nibabel.load(input_images[i])
            
            if len(img.shape) == 3:
                print(img.shape)
                
                # robustfov
                inputfile = input_images[i]
                last_vol_name = re.sub(".nii.gz","_main.nii.gz",re.sub(INPUTPATH,OUTPUTPATH,inputfile)  )  
                if not (os.path.isdir(os.path.dirname(last_vol_name))):
                    os.makedirs(os.path.dirname(last_vol_name))

                output_torobust = re.sub("_main.nii.gz", "_main-rf00.nii.gz", last_vol_name)
                robust_code = 'robustfov -i ' + inputfile + ' -b 100 -r ' + output_torobust
                os.system(robust_code)
                robust_3d_img_name = output_torobust 

                new_img_name = output_torobust
                
                # new_image
                img_rf100 = nibabel.load(new_img_name)
                print(img_rf100.shape)
                                            
                roi_data = img_rf100.get_fdata()
                CM = scipy.ndimage.measurements.center_of_mass(numpy.array(roi_data))
                round(CM[2])
                
                mid_slice_num = int(round(CM[2]))
                img_midslice = img_rf100.slicer[:,:,mid_slice_num:(mid_slice_num+1)]                
                
                midslice_newname = re.sub("_main-rf00.nii.gz","_CMmidslice_main.nii.gz",new_img_name)     
     
                nibabel.save(img_midslice, midslice_newname) # 2D main volume will be saved
                os.unlink(output_torobust) # delete output_robust
                
                image_midslice_list.append(midslice_newname)

                image_4d_3d_2d_file_names.append([input_images[i],input_images[i],midslice_newname])
                
            elif len(img.shape) > 3:
                
                print(img.shape)
                                                
                # convert 4D to 3D
                img4d = img.get_fdata()
                
                first_vol_img = img4d[..., 0]
                last_vol_img = img4d[..., -1]
                
                # save the last volume as 3d nifti in the OUTPUTPATH
                inputfile = input_images[i]
                
                # find the sequence folder name
                first_foldername =  os.path.basename(os.path.dirname(inputfile)) + '_first' 
                last_foldername =  os.path.basename(os.path.dirname(inputfile)) + '_last'
                
                first_vol_name = re.sub(INPUTPATH,OUTPUTPATH,inputfile)
                first_vol_name2 = re.sub(os.path.basename(os.path.dirname(inputfile)),first_foldername,first_vol_name  )  
                last_vol_name = re.sub(INPUTPATH,OUTPUTPATH,inputfile)
                last_vol_name2 = re.sub(os.path.basename(os.path.dirname(inputfile)),last_foldername,last_vol_name  )  
                if not (os.path.isdir(os.path.dirname(first_vol_name2))):
                    os.makedirs(os.path.dirname(first_vol_name2))
                if not (os.path.isdir(os.path.dirname(last_vol_name2))):
                    os.makedirs(os.path.dirname(last_vol_name2))
                    
                    
                first_vol_img_new = nibabel.Nifti1Image(first_vol_img, affine=img.affine)    
                last_vol_img_new = nibabel.Nifti1Image(last_vol_img, affine=img.affine)
                nibabel.save(first_vol_img_new,first_vol_name2) # 3D first volume will be saved
                nibabel.save(last_vol_img_new,last_vol_name2) # 3D last volume will be saved
        
                ###### robustfov
                first_inputfile_torobust = first_vol_name2
                last_inputfile_torobust = last_vol_name2
                
                first_output_torobust = re.sub("_first.nii.gz", "_first-rf00.nii.gz", first_inputfile_torobust)
                last_output_torobust = re.sub("_last.nii.gz", "_last-rf00.nii.gz", last_inputfile_torobust)

                first_robust_code = 'robustfov -i ' + first_inputfile_torobust + ' -b 100 -r ' + first_output_torobust
                last_robust_code = 'robustfov -i ' + last_inputfile_torobust + ' -b 100 -r ' + last_output_torobust
                
                os.system(first_robust_code)
                os.system(last_robust_code)
                
                first_robust_3d_img_name = first_output_torobust
                last_robust_3d_img_name = last_output_torobust
                
                
                os.unlink(first_inputfile_torobust) # delete the robust 3D lastvolume 
                os.unlink(last_inputfile_torobust) # delete the robust 3D lastvolume
                
                # find center of mass (CM)
                first_robust_3d_img = nibabel.load(first_robust_3d_img_name)
                last_robust_3d_img = nibabel.load(last_robust_3d_img_name)
                
                first_robust_3d_img.get_fdata()
                last_robust_3d_img.get_fdata()
                
                first_CM = scipy.ndimage.measurements.center_of_mass(numpy.array(first_robust_3d_img.get_fdata()))
                round(first_CM[2])
                
                last_CM = scipy.ndimage.measurements.center_of_mass(numpy.array(last_robust_3d_img.get_fdata()))
                round(last_CM[2])
                
                first_mid_slice_num = int(round(first_CM[2]))
                last_mid_slice_num = int(round(last_CM[2]))
                
                first_img_midslice = first_robust_3d_img.slicer[:,:,first_mid_slice_num:(first_mid_slice_num+1)]
                last_img_midslice = last_robust_3d_img.slicer[:,:,last_mid_slice_num:(last_mid_slice_num+1)]

                first_midslice_newname = re.sub('.nii.gz','_CMmidslice.nii.gz',first_robust_3d_img_name) 
                last_midslice_newname = re.sub('.nii.gz','_CMmidslice.nii.gz',last_robust_3d_img_name) 
                                    
                try:
                    first_new_image = nibabel.Nifti1Image(first_img_midslice.get_fdata(), affine=first_robust_3d_img.affine)
                    last_new_image = nibabel.Nifti1Image(last_img_midslice.get_fdata(), affine=last_robust_3d_img.affine)

                except:

                    print('an error occured at ==>   try: new_image = nibabel.Nifti1Image(img_midslice_new, affine=robust_3d_img.affine)')
    
                nibabel.save(first_new_image, first_midslice_newname)
                nibabel.save(last_new_image, last_midslice_newname)
                
                os.unlink(first_robust_3d_img_name) # delete the raw 3D lastvolume 
                os.unlink(last_robust_3d_img_name) # delete the raw 3D lastvolume 
                
                image_midslice_list.append(first_midslice_newname)
                image_midslice_list.append(last_midslice_newname)
                
                image_4d_3d_2d_file_names.append([input_images[i],first_vol_name2,first_midslice_newname])
                image_4d_3d_2d_file_names.append([input_images[i],last_vol_name2,last_midslice_newname]) 
            else:
                print('check image shape or readability...')
                
        except:

            print('an error occurred for the image: ')
            print("     ".join([str(i),input_images[i]]))
    
    
    return image_4d_3d_2d_file_names















