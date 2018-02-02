#-------------------------------------------------------------------------------
# Name:        file loaders
# Purpose:
#
# Author:      adm_bctt490
#
# Created:     01/02/2018
# Copyright:   (c) adm_bctt490 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def file_loader(filepath):
    '''Reads in file and retures data'''
    file_descriptor = open(filepath, "r")
    data = file_descriptor.read()
    file_descriptor.close() # required for nicer clean up. In below example, handle by with
    return data

# better way for the same thing below:
def file_loader_with(filepath):
    '''Reads in file and retures data'''
    with open(filepath, "r") as file_descriptor:
        data = file_descriptor.read()
    return data


def file_load_lines(filepath):
    '''Reads in file and retures data as a list of lines'''
    file_descriptor = open("filepath", "r")
    data = file_descriptor.read()
    # data = file_descriptor.readlines()
    data_lines = data.split("\n")
    file_descriptor.close()
    return data_lines


def yamlFile_loader(filepath):
    '''Reads in file and retures data'''
    yamlfile_descriptor = open("filepath", "r")
    yamldata = yamlfile_descriptor.read()
    yamlfile_descriptor.close()

def yamlFile_loader_with(filepath):
    '''loads file and returns data'''
    with open(filepath, "r") as file_descriptor:
        data = yaml.load(file_descriptor)
    return data


def file_dumper(filepath):
    '''takes data and writes to file'''
    file_descriptor = open("filepath", "w")
    file_descriptor.write(data)
    file_descriptor.close()


if __name__ == '__main__':
    filepath = "test.txt"
    data = file_loader(filepath)
    print(data)




#main()
