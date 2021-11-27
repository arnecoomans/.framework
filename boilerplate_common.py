#!/usr/bin/python3
#
# Boilerplate: Common
# Part of the cmns.framework
# Holds shortcuts available to any app, module or core module
# @author     Arne Coomans
# @version    0.0.1
# @url        https://github.com/cmns-nl/.framework/
# 

# Import system python modules
import sys, os
from pathlib import PosixPath

# Ensure script is embedded and not called directly.
if __name__ == "__main__":
      sys.exit('[FATAL] Quitting. Do not call ' + os.path.basename(__file__) + ' directly.')

# Add Local Shared Lib
importList = [os.path.dirname(os.path.abspath(__file__))]
for location in importList:
  if location not in sys.path:
    sys.path.append(location)

# Import framework specifics

class CommonBoilerplate:
  def __init__(self, framework=None) -> None:
    self.framework = framework

  ##  Logging
  #   Shortcut to functions in framework_logging
  #   Takes information into the content buffer. Uses flush() to send content to output sources.
  #
  ### throw_error()
  #   @arguments     content [string|list]
  #   @description   Sends an error message to content buffer with display level 1.
  #                  Flushes the content buffer
  #                  Halts the application with this error message.
  def throw_error(self, content):
    if hasattr(self.framework, 'log'):
      return self.framework.log.throw_error(content)
    else:
      print('[ ERROR ] ' + str(content))
      sys.exit()
  ### print()
  #   @arguments     content [string|list]
  #   @description   Sends a message to the content buffer with display level 2
  def print(self, content=''):
    if hasattr(self.framework, 'log'):
      return self.framework.log.print(content)
    else:
      print(str(content))
  ### throw_warning()
  #   @arguments     content [string|list]
  #   @description   Sends a message to the content buffer with display level 3
  def throw_warning(self, content):
    if hasattr(self.framework, 'log'):
      return self.framework.log.throw_warning(content)
    else:
      print('[WARNING] ' + str(content))
  ### throw_notice()
  #   @arguments     content [string|list]
  #   @description   Sends a message to the content buffer with display level 4
  def throw_notice(self, content):
    if hasattr(self.framework, 'log'):
      return self.framework.log.throw_notice(content)
    else:
      print('[NOTICE ] ' + str(content))
  ### debug()
  #   @arguments     content [string|list]
  #   @description   Sends a message to the content buffer with display level 5
  def debug(self, content):
    if hasattr(self.framework, 'log'):
      return self.framework.log.debug(content)
    else:
      print('[ DEBUG ] ' + str(content))
  ### flush()
  #   @description   sends the log buffer to its output(s)
  #                  based on the set log level
  def flush(self):
    if hasattr(self.framework, 'log'):
      return self.framework.log.flush()
  

  ##  Configuration
  #   Shortcuts to functions in framework_config
  ### getArgument()
  #   @arguments     key [string]
  #   @description   Retrieves a configured value from configuration class
  #                  Configured values are stored via command line arguments or via config yml files.
  def getArgument(self, key):
    if hasattr(self.framework, 'config'):
      return self.framework.config.getArgument(key=key)
    else:
      self.throw_error('getArgument: Core module Config not found when looking for the value of \'' + str(key) + '\'.')
  
  ##  Files and paths
  #   Shortcuts to functions in framework_files
  #   Common availability to file and directory handling core functionality
  ### getFile()
  #   @arguments     file [string|posixpath], exists [bool]
  #   @returns       posixPath object of file
  #   @description   Returns the posixPath object of the specified file.
  #                  If no absolute path is given, use current working directory as base path.
  def getFile(self, file=None, exists=False):
    return self.framework.files.getFile(file=file, exists=exists)
  ### getPath()
  #   @arguments     path [string|posixpath]
  #   @returns       posixPath object of given path
  #   @description   Returns the path of given input as posixPath object.
  #                  If input is a file, the path of the file is returned
  def getPath(self, path=None):
    return self.framework.files.getPath(path=path)
  ### getRecentFile()
  #   @arguments     path [string|posixpath], filter [string], recursive [bool], method [string]
  #   @returns       posixpath object
  #   @description   Returns the most recently created or modified file in path.
  #                  Use filter to filter files by extention (include .)
  #                  Use recursive to search in path and subdirectories of path
  #                  Method supports created or modified as sorting method
  def getRecentFile(self, path=None, filter=None, recursive=False, method='modified'):
    return self.framework.files.getRecentFile(path=path, filter=filter, recursive=recursive, method=method)
  
  ##  Date and time functions
  #   Shortcut to functions in framework_date
  ### getDate()
  #   @arguments     format [string]
  #   @returns       date in format [string]
  #   @description   Returns date in supplied format. 
  #                  For format options, see https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
  def getDate(self, format='%Y-%m-%d'):
    return self.framework.date.getDate(format=format)
  ### getTime()
  #   @arguments     format [string]
  #   @returns       time in format [string]
  #   @description   Returns time in supplied format. 
  #                  For format options, see https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
  def getTime(self, format='%H:%M:%S'):
    return self.framework.date.getTime(format=format)
  ### getDateTime()
  #   @arguments     format [string]
  #   @returns       date and time in format [string]
  #   @description   Returns date and time in supplied format. 
  #                  For format options, see https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
  def getDateTime(self):
    return self.framework.date.getDateTime()