#!/usr/bin/python3
# 
# Framework Logging Core-Module
# Adds bufferd output handling and filtering
#
import sys, os
from argparse import ArgumentParser


# Ensure script is embedded and not called directly.
if __name__ == "__main__":
      sys.exit('[FATAL] Quitting. Do not call ' + os.path.basename(__file__) + ' directly.')

# Add Local Shared Lib
importList = [os.path.dirname(os.path.abspath(__file__))]
for location in importList:
  if location not in sys.path:
    sys.path.append(location)
from boilerplate_framework import FrameworkBoilerplate as Boilerplate

class Config(Boilerplate):
  def __init__(self, framework) -> None:
    # Run Boilerplate initialisation
    super().__init__(framework)
    # Prepare reference containers
    # Prepare configurable values
    self.default_value = None
    self.key_seperator = '.'
    self.argumentsetter = '-'
    self.app_name = None
    
    # Prepare data containers
    self.storage = {}
    self.arguments = {}
    # Initialisation
    self.setDefaultConfiguration()
    self.parseDefaultConfiguration()
    self.arguments = self.getRuntimeArguments()
    self.parseRuntimeArguments(self.arguments)
    
    # Development and debugging
    self.debug('Core Module Config loaded')
    #self.debug(self.arguments)

  ##  Access Functions
  ### set
  #   @description stores key and value pais in the configuration storage container.
  #                Keys can be multi-level and are seperated by a .-character.
  #   @arguments key (string)
  #              value (string|list|dict|boolean|integer)
  #              prefix (list)
  #   @returns boolean
  def set(self, key, value=None, prefix=[]):
    # Ensure default value is used
    if value == None:
      value = self.default_value
    # Ensure prefix is a list
    if not type(prefix) is list:
      prefix = [str(prefix)]
    # If the stored value is a dict, it should be recursively processed
    if type(value) is dict:
      for subkey, subvalue in value.items():
        self.set(subkey, subvalue, prefix + [key])
    # Store the (key prefix,) key and value
    else:
      if type(value) == str:
        value = value.strip()
      self.storage[self.key_seperator.join(prefix + [key]).lower()] = value
      return True
  ### get
  #   @description get value for key from configuration storage container
  #   @arguments key (string)
  #              prefix (list)
  #   @returns value (string|list|dict|boolean|integer)
  def get(self, key, prefix=[]):
    # Ensure key is in lowercase
    key = key.lower()
    # First ensure that prefix is a list.
    if type(prefix) is not list:
      prefix = [prefix]
    # if no prefix is supplied, try for an exact match
    if len(prefix) == 0:
      if key in self.storage:
        return self.storage[key]
      else:
        return self.default_value
    else:
      # A prefix is supplied.
      # Check if prefixed key exists
      if self.key_seperator.join(prefix + [key]).lower() in self.storage:
        return self.get(self.key_seperator.join(prefix + [key]))
    return self.default_value
  

  #   Default configuration
  ### Set default configuration
  #   @description Stores some default configuration values in the storage container that are expected
  #                for the core framework to function.
  #   @arguments None
  #   @returns None
  def setDefaultConfiguration(self) -> None:
    self.storage['display_level'] = 5
    
  def parseDefaultConfiguration(self) -> None:
    self.framework.log.setDisplayLevel(self.get('display_level'))



  #   Argument parsing
  ### get_app_name
  #   @description Gets application name from filename
  #   @arguments None
  #   @returns (string)
  def get_app_name(self):
    return sys.argv[0]
  
  ### parse_runtime_arguments
  #   @description Reads runtime arguments and stores these. 
  #                Processes some special arguments but does not require arguments to 
  #                be pre-defined. This allows for the best flexibility.
  #                Argparse requires the arguments to be pre-defined and that is less
  #                flexible.
  #                Stores the arguments in the self.arguments data container
  #   @arguments None
  #   @returns self.
  def getRuntimeArguments(self):
    # Prepare result placeholder
    arguments = { 
      'files': [], 
      }
    # Process arguments
    # Arguments are stored by python in sys.argv. Sys.argv[0] is the current filename and 
    # is not relevant for argument processing. Start with [1:]
    # Loop through each argument.
    # Use count method in stead of a simple for loop. This allows to use the following 
    # argument as value for a set key.
    # Setter arguments mostly look fancy but rarely add functionality. Repeating the same character
    # after a setter character results in the character as key and the number of repeats as value. 
    count = 1
    while count < len(sys.argv):
      argument = sys.argv[count]
      # Detect setter argument (starts with - (character is configured in argumentsetter))
      if argument[:1] == self.argumentsetter or \
         argument[:2] == self.argumentsetter*2:
        # Argument setter is detected
        # Remove argument setter character
        while argument[:1] == self.argumentsetter:
          argument = argument[1:]
        # First, detect repeating character
        if argument == argument[:1]*len(argument):
          # If a repeating character is detected, the character should be stored as key and the 
          # character count should be stored as value.
          arguments[argument[:1]] = len(argument)
          count += 1
          continue
      # Detect if the argument is followed by a value
      # This can be the same for a setter argument or a normal argument
      if argument[-1:] == ':' or \
          argument[-1:] == '=':
        # The following arugment should be seen as value
        argument = argument[:-1]
        # Use count to get the following argument as value. This also skips the following argument
        # for regular processing.
        count += 1
        arguments[argument] = sys.argv[count]
      # Detect if the setter contains a value
      elif ':' in argument:
        argument = argument.split(':')
        arguments[argument[0].lower()] = argument[1]
      elif '=' in argument:
        argument = argument.split('=')
        arguments[argument[0].lower()] = argument[1]
      # Argument could be a file
      elif os.path.isfile(argument):
        arguments['files'].append(argument)
      # Assume the value is True
      else:
        arguments[argument.lower()] = True
      # Increase key count to process next argument
      count += 1
    # Return parsed arguments
    return arguments


  def getArgument(self, argument):
    argument = argument.lower()
    if argument in self.arguments:
      return self.arguments[argument]
    elif argument in self.arguments['files']:
      return self.arguments['files'][argument]
    else:
      return None 

  def parseRuntimeArguments(self, arguments):
    # Use -v*[1-4] to set verbosity. Sets display level between 2 and 5
    # Verbosity level 1 is default and cannot be removed - errors are always displayed. That is why 
    # -v starts with 2. 
    if type(self.getArgument('v')) is int:
      self.framework.log.setDisplayLevel(self.getArgument('v')+1)
    elif self.getArgument('verbose') is True:
      self.framework.log.setDisplayLevel(5)
    elif self.getArgument('verbose') in ['1', '2', '3', '4', '5']:
      self.framework.log.setDisplayLevel(int(self.getArgument('verbose')))
      
    
        
          
    
    