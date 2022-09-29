"""
Code to get list of al files in a directory and its sub directories
"""
import os
import argparse
import numpy as np
from natsort import natsorted
def files(dir_name, filename_extension=".txt"):
    '''
    recursive function to get list of al files in a directory and its sub directories
    '''
    file_list = [] # maintain list of all filenames with paths wrt to main diretory
    file_len_list = [] #maintain length/number of lines of files separately
    subdir_list = [] # maintain a sub directory list to arrange final files acc to dir order
    for file in natsorted(os.listdir(dir_name)): # for all files in dir
        if os.path.isdir(os.path.join(dir_name,file)): # store sub dir name separately
            subdir_list.append(os.path.join(dir_name,file))
        elif file.endswith(filename_extension):
            # check extension and all file to list if matching extension
            file_list.append(os.path.join(dir_name,file))# add full path with filename
            # calculating number of lines per file using enumerate
            #enumerate does not load the entire file to memory so works well for large files
            #better than using readLines()
            with open(os.path.join(dir_name, file), 'r') as file_obj:
                line_count = 0
                for line_count,_ in enumerate(file_obj):
                    continue
            file_obj.close()
            file_len_list.append(line_count+1)
    for subdir in subdir_list: #recursive function for sub directories
        file_list.extend(files((subdir))[0]) #appending file names
        file_len_list.extend(files((subdir))[1]) #appending file lengths
    return file_list, file_len_list
def get_dir_file_details(dir_name, filename_extension=".txt"):
    '''
    function to print details in the required format
    '''
    if os.path.exists(dir_name) is False:
        print("Invalid Directory")
        return
    #get list of files with their respective lengths
    file_list, file_len_list = files(dir_name, filename_extension)
    if len(file_list)==0:
        print("No Files Present in Directory")
        return
    linebreak = ["="]
    #printing files with right aligned length/num lines
    for count, file in enumerate(file_list):
        #width of left alignment is length of largest file name
        print(f"{file:<{len(file_list[-1])}} {file_len_list[count]}")
    #line break is length of largest filename
    print("".join(linebreak*len(file_list[-1])))
    print("".join(linebreak*len(file_list[-1])))
    print_statemet = "Number of files found"
    print(f"{print_statemet:<{30}} {len(file_list)}")
    print_statemet = "Total Number of Line"
    print(f"{print_statemet:<{30}} {np.sum(file_len_list)}")
    print_statemet = "Average lines per file"
    print(f"{print_statemet:<{30}} {np.sum(file_len_list)/len(file_list)}")
def main(dir_name, filename_extension):
    '''
    Defining main function
    '''
    get_dir_file_details(dir_name, filename_extension)
if __name__=="__main__":
    DIR_NAME = "./"
    FILENAME_EXTENSION =".txt"
    parser = argparse.ArgumentParser() # Initialize parser
    # Adding optional argument
    parser.add_argument("-d", "--Directory", help = "File Directory")
    parser.add_argument("-e", "--Extension", help = "File Extension")
    # Read arguments from command line
    args = parser.parse_args()
    if args.Directory:
        DIR_NAME = args.Directory
    if args.Extension:
        FILENAME_EXTENSION = args.Extension
    main(DIR_NAME, FILENAME_EXTENSION)
    
