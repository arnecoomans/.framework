# App method description
This document contains the methods that can be used within an app.

## Requirements
In order to run, the app should have some perperations
### System modules
> import sys, os
### Import framework 
> sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../.framework/')
> from boilerplate_app import AppBoilerplate as Boilerplate
### Class inheritance
> class app(Boilerplate):
>   def __init__(self) -> None:
>     super().__init__()




## Function: print()
Adds content to the display buffer showed when display level is set to 4 or higher. 
### Arguments:
### Example:
> app.print('Hello world!)
Hello world!
### Notes:
### Maintained in: framework_logging

## Function throw_error()
Throws an error and stops application
### Arguments:
### Example:
> app.throw_error('Cannot proceed')
[! Error] Cannot proceed
2021-11-07 22:39:24.22 Stopping application because of error.
### Maintained in: framework_logging

## Function throw_warning()
Displays a warning when display level is set to 2 or higher (use -v)
### Example:
> app.throw_warning('Something happened')
[w] Something happened
### Maintained in: framework_logging

## Function throw_notice()
Displays a notice when display level is set to 3 or higher (use -vv)
### Example:
> app.throw_notice('Please look at this')
[n] Please look at this



## Function: ask()
Gets user input for a defined question.
### Arguments:
- question (required)
- reference (optional)
- suggestion (optional)
### Returns:
The function returns the answer.
### Example:
> app.ask(question='How you doin\'', reference='tribbiani', suggestion='fine')
How you doin' ('fine'): 
#### Notes:
The reference is used to fetch a key-value from commandline. If a commandline reference is passed, the question is automatically answered.
The reference is also used to store the answer for repeated processing.



