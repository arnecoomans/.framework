# App method description
This document contains the methods that can be used within an app.

## Function: print()
Inherited from globally available function


## Function: ask()
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



