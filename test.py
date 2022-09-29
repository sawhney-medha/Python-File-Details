import unittest
import sys
import os
import io
import shutil
import random
from source import main
class TestFileCountDetails(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        '''
        Initializing class variables for storing output and printing
        '''
        super(TestFileCountDetails, self).__init__(*args, **kwargs)
        self.output_obj = None
        self.linebreak_test_type = ["*"]
        self.linebreak_output = ["-"]
        self.output_file = "./test_output.txt"
        output = open(self.output_file,'w')
        output.close()
        
    def redirect_output_store(self):
        '''
        Redirecting console output to store in another variable
        '''
        self.output_obj = io.StringIO()                  
        sys.stdout = self.output_obj 
        
    def redirect_output_normal(self):
        '''
        Redirecting output back to console to print
        '''
        sys.stdout = sys.__stdout__ 
        
    def print_test_output(self, test_name):
        '''
        Function to print test output
        '''
        self.print("".join(self.linebreak_test_type*50))
        self.print (test_name)
        self.print("".join(self.linebreak_output*50))
        self.print(self.output_obj.getvalue())
        self.print("".join(self.linebreak_test_type*50))
        
    def print(self, text):
        output_file = open(self.output_file, 'a')
        print(text)
        output_file.write(text + "\n")
        output_file.close()
    def get_file_size(self,file_name):
        with open(file_name, 'r') as file_obj:
            line_count = 0
            for line_count,_ in enumerate(file_obj):
                continue
            file_obj.close()
            return line_count+1
        
    def test_invalid_dir(self):
        '''
        Testing for a non existing directory
        '''
        #testing non existent directory        
        self.redirect_output_store() 
        test_dir = "./x/"
        main.get_dir_file_details(test_dir)                                   
        self.redirect_output_normal() 
        self.print_test_output("Testing Non-Existing Directory:")
        assert self.output_obj.getvalue().strip() == 'Invalid Directory'
        
    #test for empty dir
    def test_empty_dir(self):
        '''
        Testing for a empty directory
        '''
        #testing empty directory
        self.redirect_output_store()
        test_dir = "./empty"
        os.makedirs(test_dir, exist_ok=True)
        main.get_dir_file_details(test_dir)
        self.redirect_output_normal() 
        self.print_test_output("Testing Empty Directory:")
        assert self.output_obj.getvalue().strip() == 'No Files Present in Directory'
        os.removedirs(test_dir)
        
    #test for single empty file
    def test_single_empty_file(self):
        '''
        Testing for a single empty file
        '''
        #testing empty directory
        self.redirect_output_store()
        test_dir = "./single-file-empty"
        os.makedirs(test_dir, exist_ok=True)
        with open(os.path.join(test_dir,'file1.txt'), 'w') as file_object:
            file_object.close()
        main.get_dir_file_details(test_dir)
        self.redirect_output_normal() 
        self.print_test_output("Testing Single Empty File:")
        self.assertIn(os.path.join(test_dir,'file1.txt'), self.output_obj.getvalue().strip())
        #check number of lines = 1 for emptyfile
        #print(self.output_obj.getvalue().split(" ")[1].split("\n")[0].strip())
        assert int(self.output_obj.getvalue().split(" ")[1].split("\n")[0].strip()) == 1
        shutil.rmtree(test_dir)
        
    #test for multiple empty files
    def test_multiple_empty_file(self):
        '''
        Testing for a multiple empty files
        '''
        #testing empty directory
        self.redirect_output_store()
        test_dir = "./multiple-file-empty"
        os.makedirs(test_dir, exist_ok=True)
        rand_file_num = random.randrange(2,10) 
        for i in range(1,rand_file_num):
            with open(os.path.join(test_dir,f'file_{i}.txt'), 'w') as file_object:
                file_object.close()
        main.get_dir_file_details(test_dir)
        self.redirect_output_normal() 
        self.print_test_output("Testing Multiple Empty Files:")
        self.assertIn(os.path.join(test_dir,'file_1.txt'), self.output_obj.getvalue().strip())
        #check number of lines = 1 for emptyfile
        #print(self.output_obj.getvalue().split(" ")[1].split("\n")[0].strip())
        assert int(self.output_obj.getvalue().split(" ")[1].split("\n")[0].strip()) == 1
        last_file_name = os.path.join(test_dir,f'file_{int(rand_file_num)-1}.txt')
        self.assertIn(last_file_name, self.output_obj.getvalue().strip())
        assert int(self.output_obj.getvalue().split(last_file_name)[1].split("\n")[0].strip()) == 1
        shutil.rmtree(test_dir)
        
    #test for multiple small files
    def test_multiple_small_files(self):
        '''
        Testing for a multiple empty files
        '''
        #testing empty directory
        self.redirect_output_store()
        test_dir = "./multiple-file-small"
        os.makedirs(test_dir, exist_ok=True)
        rand_file_num = random.randrange(2,10) 
        for i in range(1,rand_file_num):
            with open(os.path.join(test_dir,f'file_{i}.txt'), 'w') as file_object:
                for line_count in range(random.randrange(1000,5000)):
                    file_object.write(f"test line{line_count}")
                    file_object.write("\n")
                file_object.close()
        main.get_dir_file_details(test_dir)
        self.redirect_output_normal() 
        self.print_test_output("Testing Multiple Small Files:")
        self.assertIn(os.path.join(test_dir,'file_1.txt'), self.output_obj.getvalue().strip())
        #check number of lines = 1 for emptyfile
        #print(self.output_obj.getvalue().split(" ")[1].split("\n")[0].strip())
        file_size = self.get_file_size(os.path.join(test_dir,'file_1.txt'))
        assert int(self.output_obj.getvalue().split(" ")[1].split("\n")[0].strip()) == file_size
        last_file_name = os.path.join(test_dir,f'file_{int(rand_file_num)-1}.txt')
        last_file_size = self.get_file_size(last_file_name)
        self.assertIn(last_file_name, self.output_obj.getvalue().strip())
        assert int(self.output_obj.getvalue().split(last_file_name)[1].split("\n")[0].strip()) == last_file_size
        shutil.rmtree(test_dir)

    #test for multiple large files
    def test_multiple_large_files(self):
        '''
        Testing for a multiple empty files
        '''
        #testing empty directory
        self.redirect_output_store()
        test_dir = "./multiple-large-small"
        os.makedirs(test_dir, exist_ok=True)
        rand_file_num = random.randrange(2,10) 
        for i in range(1,rand_file_num):
            with open(os.path.join(test_dir,f'file_{i}.txt'), 'w') as file_object:
                for line_count in range(random.randrange(10000,50000)):
                    file_object.write(f"test line{line_count}")
                    file_object.write("\n")
                file_object.close()
        main.get_dir_file_details(test_dir)
        self.redirect_output_normal() 
        self.print_test_output("Testing Multiple Large Files:")
        self.assertIn(os.path.join(test_dir,'file_1.txt'), self.output_obj.getvalue().strip())
        #check number of lines = 1 for emptyfile
        #print(self.output_obj.getvalue().split(" ")[1].split("\n")[0].strip())
        file_size = self.get_file_size(os.path.join(test_dir,'file_1.txt'))
        assert int(self.output_obj.getvalue().split(" ")[1].split("\n")[0].strip()) == file_size
        last_file_name = os.path.join(test_dir,f'file_{int(rand_file_num)-1}.txt')
        last_file_size = self.get_file_size(last_file_name)
        self.assertIn(last_file_name, self.output_obj.getvalue().strip())
        assert int(self.output_obj.getvalue().split(last_file_name)[1].split("\n")[0].strip()) == last_file_size
        shutil.rmtree(test_dir)
        
    #test for multiple very large files
    def test_multiple_very_large_files(self):
        '''
        Testing for a multiple empty files
        '''
        #testing empty directory
        self.redirect_output_store()
        test_dir = "./multiple-very-large-small"
        os.makedirs(test_dir, exist_ok=True)
        rand_file_num = random.randrange(2,10) 
        for i in range(1,rand_file_num):
            with open(os.path.join(test_dir,f'file_{i}.txt'), 'w') as file_object:
                for line_count in range(random.randrange(1000000,5000000)):
                    file_object.write(f"test line{line_count}")
                    file_object.write("\n")
                file_object.close()
        main.get_dir_file_details(test_dir)
        self.redirect_output_normal() 
        self.print_test_output("Testing Multiple Very Large Files:")
        extension=".txt"
        filename = os.path.join(test_dir,f'file_1{extension}')
        self.assertIn(filename, self.output_obj.getvalue().strip())
        #check number of lines = 1 for emptyfile
        #print(self.output_obj.getvalue().split(" ")[1].split("\n")[0].strip())
        file_size = self.get_file_size(os.path.join(test_dir,'file_1.txt'))
        assert int(self.output_obj.getvalue().split(filename)[1].split("\n")[0].strip()) == file_size
        last_file_name = os.path.join(test_dir,f'file_{int(rand_file_num)-1}.txt')
        last_file_size = self.get_file_size(last_file_name)
        self.assertIn(last_file_name, self.output_obj.getvalue().strip())
        assert int(self.output_obj.getvalue().split(last_file_name)[1].split("\n")[0].strip()) == last_file_size
        shutil.rmtree(test_dir)
        
    #test for multiple small python files
    def test_multiple_small_python_files(self):
        '''
        Testing for a multiple small python files
        '''
        #testing empty directory
        self.redirect_output_store()
        test_dir = "./multiple-file-small-python"
        os.makedirs(test_dir, exist_ok=True)
        rand_file_num = random.randrange(2,20) 
        extension = ".py"
        for i in range(1,rand_file_num):
            with open(os.path.join(test_dir,f'file_{i}{extension}'), 'w') as file_object:
                for line_count in range(random.randrange(1000,5000)):
                    file_object.write(f"test line{line_count}")
                    file_object.write("\n")
                file_object.close()
        main.get_dir_file_details(test_dir, filename_extension=extension)
        self.redirect_output_normal() 
        self.print_test_output("Testing Multiple Small Python Files:")
        filename = os.path.join(test_dir,f'file_1{extension}')
        self.assertIn(filename, self.output_obj.getvalue().strip())
        #check number of lines = 1 for emptyfile
        #print(self.output_obj.getvalue().split(" ")[1].split("\n")[0].strip())
        file_size = self.get_file_size(os.path.join(test_dir,f'file_1{extension}'))
        assert int(self.output_obj.getvalue().split(filename)[1].split("\n")[0].strip()) == file_size
        last_file_name = os.path.join(test_dir,f'file_{int(rand_file_num)-1}{extension}')
        last_file_size = self.get_file_size(last_file_name)
        self.assertIn(last_file_name, self.output_obj.getvalue().strip())
        assert int(self.output_obj.getvalue().split(last_file_name)[1].split("\n")[0].strip()) == last_file_size
        shutil.rmtree(test_dir)
        
    #test for multiple small excel files
    def test_multiple_small_excel_files(self):
        '''
        Testing for a multiple small excel files
        '''
        #testing empty directory
        self.redirect_output_store()
        test_dir = "./multiple-file-small-excel"
        os.makedirs(test_dir, exist_ok=True)
        rand_file_num = random.randrange(2,30) 
        extension = ".xlsx"
        for i in range(1,rand_file_num):
            with open(os.path.join(test_dir,f'file_{i}{extension}'), 'w') as file_object:
                for line_count in range(random.randrange(1000,5000)):
                    file_object.write(f"test line{line_count}")
                    file_object.write("\n")
                file_object.close()
        main.get_dir_file_details(test_dir, filename_extension=extension)
        self.redirect_output_normal() 
        self.print_test_output("Testing Multiple Small Excel Files:")
        filename = os.path.join(test_dir,f'file_1{extension}')
        self.assertIn(filename, self.output_obj.getvalue().strip())
        #check number of lines = 1 for emptyfile
        #print(self.output_obj.getvalue().split(" ")[1].split("\n")[0].strip())
        file_size = self.get_file_size(os.path.join(test_dir,f'file_1{extension}'))
        assert int(self.output_obj.getvalue().split(filename)[1].split("\n")[0].strip()) == file_size
        last_file_name = os.path.join(test_dir,f'file_{int(rand_file_num)-1}{extension}')
        last_file_size = self.get_file_size(last_file_name)
        self.assertIn(last_file_name, self.output_obj.getvalue().strip())
        assert int(self.output_obj.getvalue().split(last_file_name)[1].split("\n")[0].strip()) == last_file_size
        shutil.rmtree(test_dir)
        
    #test for multiple small doc files
    def test_multiple_small_doc_files(self):
        '''
        Testing for a multiple small doc files
        '''
        #testing empty directory
        self.redirect_output_store()
        test_dir = "./multiple-file-small-doc"
        os.makedirs(test_dir, exist_ok=True)
        rand_file_num = random.randrange(2,30) 
        extension = ".docx"
        for i in range(1,rand_file_num):
            with open(os.path.join(test_dir,f'file_{i}{extension}'), 'w') as file_object:
                for line_count in range(random.randrange(1000,5000)):
                    file_object.write(f"test line{line_count}")
                    file_object.write("\n")
                file_object.close()
        main.get_dir_file_details(test_dir, filename_extension=extension)
        self.redirect_output_normal() 
        self.print_test_output("Testing Multiple Small Doc Files:")
        #self.print("output chekerrrr:")
        filename = os.path.join(test_dir,f'file_1{extension}')
        #self.print()
        self.assertIn(filename, self.output_obj.getvalue().strip())
        #check number of lines = 1 for emptyfile
        
        file_size = self.get_file_size(filename)
        assert int(self.output_obj.getvalue().split(filename)[1].split("\n")[0].strip()) == file_size
        last_file_name = os.path.join(test_dir,f'file_{int(rand_file_num)-1}{extension}')
        last_file_size = self.get_file_size(last_file_name)
        self.assertIn(last_file_name, self.output_obj.getvalue().strip())
        assert int(self.output_obj.getvalue().split(last_file_name)[1].split("\n")[0].strip()) == last_file_size
        shutil.rmtree(test_dir)


    #test for multiple empty files
    def test_non_existing_extension(self):
        '''
        Testing for a multiple empty files
        '''
        #testing empty directory
        self.redirect_output_store()
        test_dir = "./multiple-file-empty"
        os.makedirs(test_dir, exist_ok=True)
        rand_file_num = random.randrange(2,10) 
        for i in range(1,rand_file_num):
            with open(os.path.join(test_dir,'file_{i}.txt'), 'w') as file_object:
                file_object.close()
        main.get_dir_file_details(test_dir, filename_extension=".py")
        self.redirect_output_normal() 
        self.print_test_output("Testing Empty Directory:")
        assert self.output_obj.getvalue().strip() == 'No Files Present in Directory'
        shutil.rmtree(test_dir)

    def create_dirs(self, test_dir, count=4):
        '''
        Function to create multiple level directories using recursion
        '''
        os.makedirs(test_dir, exist_ok=True)
        rand_file_num = random.randrange(2,7)
        count = count+1
        for i in range(1,rand_file_num):
            random_number_dir = random.randint(19,820)
            if random_number_dir%2==0 and count<10:
                count = count+1
                self.create_dirs(os.path.join(test_dir, str(random_number_dir)), count)
            if count>10:
                return
            with open(os.path.join(test_dir,f'file_{i}.txt'), 'w') as file_object:
                if i%2 == 0:
                    for line_count in range(random.randrange(1000,5000)):
                        file_object.write(f"test line{line_count}")
                        file_object.write("\n")
                file_object.close()
    #multiple level directories
    def test_multiple_level_directories(self):
        '''
        Testing for a multiple level directories
        '''
        #testing multiple directory levels
        self.redirect_output_store()
        test_dir = "./multiple-level-directory"
        self.create_dirs(test_dir, count=0)
        main.get_dir_file_details(test_dir, filename_extension=".py")
        self.redirect_output_normal() 
        self.print_test_output("Testing Multiple Level Directory:")
        file_name = self.output_obj.getvalue().strip().split(" ")[0]
        file_size = self.get_file_size(file_name)
        assert int(self.output_obj.getvalue().split(file_name)[1].split("\n")[0].strip()) == file_size
        shutil.rmtree(test_dir)

    
unittest.main(verbosity=-1)