# Python File Details

## Task

***Write a Python program that takes a directory as a required argument and a filename extension as optional argument that defaults to “.txt”. The program should locate all files with the given extension in the given directory and all its subdirectories to produce a list of all matching files with the numbers of lines within the file. The program should also output the total number of lines and the average number of lines per file.***

#### Sample Output
./file1.txt 10 

./file2.txt 25

./d1/d1fa.txt 5

./d1/d1fb.txt 37

===============

Number of files found: 4

Total number of lines: 77

Average lines per file: 19.25

## Source Code

The source code is in the `source/main.py` file. It contains two functions where the `files` function gets the list of all files present with the given extension and the number of lines in each file. This is a recursive function which gets the list of all contents in a directory and adds them to a list and then repeats the same for all sub-directories in that list. The `get_dir_file_details` function prints out all the information in the expected fashion and also calculates other details such as total number of files and total number of lines. 

The code can be called with `-d` and `-e` arguments for specifying the directory and the extension. These arguments default to the current directory and the `.txt` extension. 

If the directory specified does not exist then the output mentions *Invalid Directory* and if the directory is empty or does not have the files with the expected extension then the output prints the message - *No Files Present in the Directory*.

The output is printe din a sorted fashion. 

## Testing
To run the test code just run the following command in the code directory:
`python test.py`

The output of each of the tests is stored in the file `test_output.txt`

The following types of tests are run:
1. Non exsisting directory
2. Empty directory
3. Non existing file extension or no file with that extension
4. Directory with files with just 1 line
5. Directory with small sized files containing 1000 to 5000 lines
6. Directory with large files having 10,000 to 50,000 lines
7. Directory with very large files having 1,000,000 to 5,000,000 lines
8. Multiple directory levels or a recursive structure
9. Tests with text, docx, xlsx and py files

