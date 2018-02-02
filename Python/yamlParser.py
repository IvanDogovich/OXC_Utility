#-------------------------------------------------------------------------------
# Name:        Yampl Parser
# Purpose:     Parsing the picnic
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
We now have the file opened, read, and printed.
A dictionary of dictionaries

 Requirements:
    Read Picnic list yaml file
    Iterate through items
    Display individually and labled.
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
    Load file
    read items
    print items


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
    filepath = picnicListFile
    data = yaml_loader(filepath)
    print(data)
    print("-" * 20)


    food_items = data.get('Food')
    dict_items = dict(food_items)       #trying to resolveerror:
    # AttributeError: 'list' object has no attribute 'iteritems'
    #looks like a python 3 issue
    # https://stackoverflow.com/questions/30418481/error-dict-object-has-no-attribute-iteritems-when-trying-to-use-networkx
    # instead: explicitly set as dictionary,
    # then use

    print(food_items)
    for item_name, item_value in dict.items(dict_items):
        print(item_name, item_value)
        #currently not iterating



