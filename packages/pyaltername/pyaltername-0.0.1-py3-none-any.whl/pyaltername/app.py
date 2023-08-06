# -*- coding: utf-8 -*-


'''
pyaltername
________________________________________________________
| Author : Michael Amadi (Mgregchi)                       |
| Email : mgregchi@gmail.com                                 |
| Url : https://github.com/Mgregchi/pyaltername/  |
|_______________________________________________________|


'''

try:
        import fnmatch
except ImportError:
        print("Could not import fnamtch. Please install pywildcard if fnmatch is not present.")
        raise

import os


def conversion(filename=None, to=None):
          '''filename : File to be converted.
          to : Format to covert to.

          NOTE : Only Media files are supported.
          Supported :
            Image[ png, jpg, gif]
            Video[Mp4, Mpeg, Avi]
            Audio[Mp3, wav, ogg]
            ______________________
            NOT Yet !!!
          '''
          pass

def extensionAndName(filename):
        base = os.path.basename(filename)
        part = base.find(".")
        if str(part) == "-1": # If '.' not found in filename
                                        # base.find() returns '-1'.
                return base, None, None
        else:
                name_base = base[:part]
                name_ext = base[part+1:]

                return base, name_base, name_ext



class Generic:

   
        def name(self, filename = None, path = None):
                '''filename : Name to give a file.
                Check if filename exists and add increament to new filename
                to avoid conflicts.
                path: Is required to compare files in the (path) directory.
                '''

                new_name = None
                
                if os.path.isfile(filename):
                        if os.path.isdir(path):
                                #base = os.path.basename(path)
                                pass
                        else:
                                raise Exception(path, "     not a valid path")
                
                base, name_base, name_ext = extensionAndName(filename=filename)
                if not name_base:
                        raise Exception("Filename must have an extension")
                name_wildCard = name_base + "*." + name_ext
                files = fnmatch.filter((names for names in os.listdir(path)), name_wildCard)

                numOf_files = len(files)
                numOf_files + 1
              
                for file in files:
                        _base, file_base, file_ext = extensionAndName(filename=file)
                        
                        if file_base == name_base + "%s"%numOf_files:
                                numOf_files = numOf_files + 1
                new_name = name_base + "{}.{}".format(numOf_files, name_ext)
                return new_name


        def extension(self, ext, new = None, path = None):
                '''
                Search through provided path for provided extension.
                Return all files with that extention.
                Return None if none is found.

                If new arg was passed, Rename the extension with the new extension.
                And you'll need to install an additional package(s).
                By changing file format. NOTE : Only Media files are supported.
                Supported :
                Image[ png, jpg, gif]
                Video[Mp4, Mpeg, Avi]
                Audio[Mp3, wav, ogg]
                '''
                pass

        def rename(self, src, dst, path = None,
                     jump_extension = ["exe","py","bat","mp4"], jump_filename = None):
                
                '''Rename  files .
                You can jump or skip some files withouth renaming them (it)
                By specifying using the jump_extension and jump_filename, respectively.

                I.e : jump_extension = ["bat", "exe", "py"]
                        jump_filename  =  ["name01.png, "name02.jpg", 'name03.css"]
                          
                example : rename(src = "newImage.png", )

                NOTE : This isn't conversion!! So don't forget to pass filename and its extension together.
                THE FILENAME OR EXTENSION To SKIP SHOULD BE CORRECTLY ENTERED !!.
                e.g : (src = "new.png") same extension should be maintained
                except you have your reasons. (File may not work properly if extension is changed).

                '''
                jump_ext = None # extension to jump or ignore
                jump_name = None # filename to jump or ignore
                jump = False
                tump =False

                if not os.path.isdir(path):
                        raise Exception("The path isn't vaild :::   ", path)

                if jump_extension:

                        if not type(jump_extension) == list:
                                raise Exception("jump_extension must be a list.\nI.e : jump_extension = ['bat', 'exe'] ")
                        else:
                                jump_ext = jump_extension

                if jump_filename:

                        if not type(jump_filename) == list:
                                raise Exception("jump_filename must be a list.\nI.e : jump_filename = ['name01.txt', 'name02.txt'] ")

                        else:
                                jump_name = jump_filename
                        

                        # Check if file before proceeding
                if os.path.isfile(os.path.join(path, src)):
                        #continue
                        base, name_base, name_ext = extensionAndName(filename=src)

                        # Require abs_path of both files.
                        #if os.path.samefile(os.path.join(path, file), os.path.join(path, "filename.jpeg")):

                        # Name before extension
                        # If name should be skipped, there's no need to check the extension.
                        if "txt" in jump_extension:
                                print("YES")
                        if jump_name and src in jump_name:
                                #continue
                                jump = True
                        if jump_ext and name_ext in jump_ext:
                                #continue
                                tump = True
                        elif jump or tump:
                                pass
                        else:
                                os.rename(os.path.join(path, src), dst)
                


class Find:

        """
        Find specified filename or extension in a given path.
        """

        def file_name(self, name, path):
                """
                Check if file(s) is in path,  with exact or similar name and return True (if exact name)
                or them (if wildcard).
                
                name : name of file to find.
                path : For directory to search for file.
                Match exact filename :
                I.e : file_name(name = "pyaltername.png", path = path)
                Returns : True
                
                To match all filenames with similar name or
                If character(s) is between the filename and extension, use wildcard .
                I.e : file_name(name = "pyaltername*.png", path =path) >> pyaltername001.png
                Returns : List of files matched
                
                Note: extension does not matter.
                The search will include file extension. Use file_extension() instead.
                """
                name_wildCard = name
                if "*" in name_wildCard:                        
                        files = fnmatch.filter((names for names in os.listdir(path)), name_wildCard)
                        return files
                else:
                        if name in os.listdir(path = path):
                                return True


        def file_extension(self, extension, path):
                """
                Find file(s) with provided extension and return list of them.

                extension : extension of file to find.
                path : For directory to search for file.
                """

                #_, b_, name_ext = extensionAndName(filename=file)
                ext_wildCard = "*" + extension.lower()
                files = fnmatch.filter((names for names in os.listdir(path)), ext_wildCard)

                return files
