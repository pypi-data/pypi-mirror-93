# pyaltername


Python package to name, rename file(s) without conflict.
Simple and easy way to name, rename,search and manage your files.

## What can it do :

- Rename mutilple files in a go!
- Gives a name to your file before saving - with auto increament to avoide conflicts.
- Return all files with a given filename or extension.
- And moe to come!

## Installations

## You can install with :
```markdown
- pip install pyaltername
- pipwin install pyaltername
```

## Example
- Generate a Name for a file .

```python

from pyaltername import Generic

filename = "Image.png"
path = r"C:/Users"

'''
do your work
data = some_data
'''

generic_name = Generic.name(filename = filename, path = path)

with open(generic_name, "wb") as file:
    file.write(data)
file.close()

```



### Clone and join the move.

Add new feature!
Fix a bug!

### What you can do :

- Submit pull request.
- Clone and make it better.
- Report a bug.
- Provide helpful feedback.


### Support or Contact

Having trouble with the project? Check out the [documentation](https://readthedocs.org/projects/pyaltername/) or [Create an Issue](https://github.com/Mgregchi/pyaltername/issues/) and you’ll get help to sort it out.


### Resources
- [Documentation](https://readthedocs.org/projects/pyaltername/)
- [Github Page](https://mgregchi.github.io/pyaltername/)
- [Issues](https://github.com/Mgregchi/pyaltername/issues/)
- [Wiki](https://github.com/Mgregchi/pyaltername/wiki/)
- [LICENSE](https://github.com/Mgregchi/pyaltername/blob/main/LICENSE)
