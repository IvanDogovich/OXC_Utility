#-------------------------------------------------------------------------------
# Name:        Yampl reader
# Purpose:
#
# Author:      adm_bctt490
#
# Created:     29/01/2018
# Copyright:   (c) adm_bctt490 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

'''
Design Ideas
Import yaml
------
This is a script to test reading a small yml file.  First
step in working on recipe merges

 Requirements:
    Read Picnic list yaml file
    Display file
 Design:
    Data:
        Food:
            Name:
            Ingredients:
    Functions:
        Load Yaml
        display

 Implementation:
    set file
    read file
    dump file


 Testing:

'''


try:
  import yaml
except ImportError:
  sys.exit('Error: PyYAML is not found')

def yaml_loader(filepath):
    '''loads file and returns data'''
    with open(filepath, "r") as file_descriptor:
        data = yaml.safe_load(file_descriptor)
    return data


if __name__ == '__main__':

    picnicListFile = "picnicList.yml"
    #picnicListFile = "C:\temp\PyScripter\picnicList.yml"
    filepath = picnicListFile
    data = yaml_loader(filepath)
    #yaml_loader = yaml.safe_load(open(picnicListFile))
    print(data)


