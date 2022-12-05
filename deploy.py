import os
import shutil
import zipfile
import pathlib


root_path = r"C:\Users\anubh\deployment_code\deploycode"

codeFolder_path = os.path.join(root_path,"Code")
config_env_path = os.path.join(root_path,"Config_Environment")
deployment_package_path = os.path.join(root_path,"Deployment_Package")

#if deployment-package path doesn't exist then it will create one
if not os.path.exists(deployment_package_path):
    os.mkdir(deployment_package_path)
else:
    shutil.rmtree(deployment_package_path)           
    os.mkdir(deployment_package_path)


#get code folder name from the code folder path
code_folder_path = pathlib.PurePath(codeFolder_path)
code_folder_name = code_folder_path.name

#getting user input
inp = input('Enter input: ')

#to get configuration path according to user input
input_env_path = os.path.join(config_env_path, inp)

#creating user input deployment package path(dev,uat,prd)
input_deploy_path = os.path.join(deployment_package_path,inp)
os.mkdir(input_deploy_path)

#copying files from the user defined(input) folder to the code folder
shutil.copytree(input_env_path, codeFolder_path, dirs_exist_ok=True)


#creating extension folder at root path
extension_folder_path = os.path.join(root_path,"Extension")
os.mkdir(extension_folder_path)


#moving all the code files to the extension folder
source = codeFolder_path
destination = extension_folder_path
allfiles = os.listdir(source)
for file in allfiles:
    src_path = os.path.join(source, file)
    dst_path = os.path.join(destination, file)
    shutil.move(src_path, dst_path)


#moving extension folder inside code folder
source = extension_folder_path
destination = codeFolder_path
shutil.move(source, destination)

#renaming the extension folder with the code folder name
os.chdir(codeFolder_path)
os.rename("Extension", code_folder_name)

#getting the path of the renamed code folder
New_codeFolder_Path = os.path.join(codeFolder_path, code_folder_name)

#path where zip file will be created
input_deploy_path = os.path.join(deployment_package_path, inp)

#function used to create the zip file from code folder to user defined deployment package folder
def zip_directory(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, mode='w') as zipf:
        len_dir_path = len(folder_path)
        for dir,subfolder, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(dir, file)
                zipf.write(file_path, file_path[len_dir_path:]) 
zip_directory(codeFolder_path, os.path.join(input_deploy_path,'ManualExtensionPublishPackage.zip'))
zip_directory(New_codeFolder_Path, os.path.join(input_deploy_path,'StoreExtensionPublishPackage.zip'))


#moving files from new created code(renamed from extension folder) folder at base code folder
source = New_codeFolder_Path
destination = codeFolder_path
allfiles = os.listdir(source)
for f in allfiles:
    src_path = os.path.join(source, f)
    dst_path = os.path.join(destination, f)
    shutil.move(src_path, dst_path)

#deleting the new created code folder
os.rmdir(New_codeFolder_Path)