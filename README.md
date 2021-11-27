# CMNS Command Line .Framework

The .framework creates a starting point to create maintainable and functioning scripts 
with some basic error handling built in. 

## Table of contents
- [Key Features](#key-features)
- [Installation](#installation)
- [Using in an application](#using-in-an-application)
- [Configuration](#configuration)

## Key features
- Choose to display Errors, Warnings, Notice and Debugging information
- Layered configuration via command line arguments or configuration files
- Sturdy path-objects
- User-Interaction worked out

## Installation
Install the .framework into a convenient location for you. 
```
$ git clone https://github.com/cmns-nl/.framework (location)
```
For example, to store the framework in a folder called python-apps, use
```
$ mkdir python-apps
$ cd python-apps
$ git clone https://github.com/cmns-nl/.framework .
```
### Updating
With a framework installed, go to the .framework directory and use
```
$ git pull
```
### Requirements
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

## Configuration
Configuration is passed to the application using command line directives. Some basic
directives are built-in. New directives can be passed to the application during 
the __init__ process of an application.

### Runtime configuration
#### Static configuration
- --config [optional: file-reference] Load static configuration file
#### Verbosity
- --verbose [1-5] Sets display level in buffered output
- --debug Shortcut to --verbose 5
- -v -> -vvvv Increase verbosity from 2 to 5
#### Log to file
- --logfile [optional: file-reference] Also write log buffer to file output
- --logfile-verbose [0-5] Set display level in logfile output
- --logfile-append Set logfile write mode to append in stead of overwrite
#### General available configuration
- --source For use in app or module
- --destination For use in app or module
- --yes|-y Accept suggestions in interaction

### Static configuration
In the .framework/conf directory, static configuration can be placed.
- defaults.yml is always loaded by the application.
- app_{app-name}.yml is loaded when the --config directive is passed.
- custom_{name}.yml is loaded when the --config {name} directive is passed.

