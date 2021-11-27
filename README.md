# CMNS Command Line .Framework

The .framework creates a starting point to create maintainable and functioning scripts 
with some basic error handling built in. 

## Key features
- Choose to display Errors, Warnings, Notice and Debugging information
- Layered configuration via command line arguments or configuration files
- Sturdy path-objects
- User-Interaction worked out

## Installation
Install the .framework into a convenient location for you. 
```
$ git clone https://github.com/arnecoomans/.framework (location)
```
For example, to store the framework in a folder called python-apps, use
```
$ mkdir python-apps
$ cd python-apps
$ git clone https://github.com/arnecoomans/.framework .
```
## Updating
With a framework installed, go to the .framework directory and use
```
$ git pull
```
## Requirements
The .framework requires python 3.

The following python modules should be present.
- pyyml ($ pip3 install pyyml)
If this python module is missing, a descriptive error message will be thrown.

## Using in an application
To use the framework in an application, you must make sure the .framework directory is 
loaded into your sys.path. An easy way to ensure that the .framework directory is loaded
is to add the directory to your sys.path during app-script runtime. 
From your python-apps directory, you can use:
```
import os, sys
sys.append(os.path.dirname(os.path.abspath(__file__)) + '/.framework)
```

The python app should load the .framework app.boilerplate
```
from boilerplate_app import AppBoilerplate as Boilerplate
```

The python app should contain a class where the framework is built in to. This class 
should extend the Boilerplate that is imported above.
```
class app(Boilerplate):
  def __init__(self) -> None:
    super().__init__()
```

Combined, this would lead to a default app:
```
#!/usr/bin/python3
import os, sys
sys.append(os.path.dirname(os.path.abspath(__file__)) + '/.framework)
from boilerplate_app import AppBoilerplate as Boilerplate

class app(Boilerplate):
  def __init__(self) -> None:
    super().__init__()
    self.print('Hello World!)

app = app()
```

