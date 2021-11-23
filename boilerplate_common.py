#!/usr/bin/python3
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
#from boilerplate_common import CommonBoilerplate as Boilerplate
#from framework_core import Framework

class CommonBoilerplate:
  def __init__(self, framework=None) -> None:
    self.framework = framework

  # Common availaibility to logging as core functionality
  def log(self, content='', level=None):
    if hasattr(self.framework, 'log'):
      return self.framework.log.add(content=content, level=level)
    if type(content) is list:
      for line in content:
        print(line)
    else:
      print(content)
  def flush(self):
    if hasattr(self.framework, 'log'):
      return self.framework.log.flush()
  # Shortcuts
  def throw_error(self, content):
    if hasattr(self.framework, 'log'):
      return self.framework.log.throw_error(content)
    else:
      print('[! Error] ' + str(content))
      sys.exit()
  def throw_warning(self, content):
    if hasattr(self.framework, 'log'):
      return self.framework.log.throw_warning(content)
    else:
      print('[! Warning] ' + str(content))
  def throw_notice(self, content):
    if hasattr(self.framework, 'log'):
      return self.framework.log.throw_notice(content)
    else:
      print('[! Notice] ' + str(content))
  def print(self, content=''):
    if hasattr(self.framework, 'log'):
      return self.framework.log.print(content)
    else:
      print(str(content))
  def debug(self, content):
    if hasattr(self.framework, 'log'):
      return self.framework.log.debug(content)
    else:
      print('[! Debug] ' + str(content))
  
  # Common availaibility to configuration as core functionality
  def getArgument(self, argument):
    return self.framework.config.getArgument(argument=argument)
  
  # Common availability to file and directory handling core functionality
  def getFile(self, file=None, exists=False):
    return self.framework.files.getFile(file=file, exists=exists)
  def getPath(self, path=None):
    return self.framework.files.getPath(path=path)
  def getRecentFile(self, path, filter=None, recursive=False, method='modified'):
    return self.framework.files.getRecentFile(path=path, filter=filter, recursive=recursive, method=method)
  def pathExists(self, path):
    return self.framework.files.pathExists(path=path)