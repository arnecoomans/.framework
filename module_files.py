#!/usr/bin/python3
import sys, os
from pathlib import Path, PosixPath

# Ensure script is embedded and not called directly.
if __name__ == "__main__":
      sys.exit('[FATAL] Quitting. Do not call ' + os.path.basename(__file__) + ' directly.')

# Add Local Shared Lib
importList = [os.path.dirname(os.path.abspath(__file__))]
for location in importList:
  if location not in sys.path:
    sys.path.append(location)

# Import framework specifics
from boilerplate_module import ModuleBoilerplate as Boilerplate
from framework_core import Framework

class files(Boilerplate):
  def __init__(self, framework) -> None:
    super().__init__(framework, modulename=__name__[7:])
    pass

  def isPath(self, path=None):
    # Returns the given path is Pathlib.PosixPath.
    # If no path is supplied, get current working directory
    if path is None:
      return Path.cwd()
    elif type(path) is not PosixPath and len(path) == 0:
      return Path.cwd()
    else:
      # Return path as PosixPath
      return path if type(path) is PosixPath else Path(path)
  
  def getMostRecent(self, path=None, filter=None, recursive=False):
    path = self.isPath(path)
    # Normalize filter
    if filter == None or filter == False or len(filter) == 0:
      filter = ''
    elif filter == '*' or filter == '*.*':
      filter = '*'
    elif filter[0:1] != '.':
      filter = '.' + filter
    filter = '*' + filter
    # Allow for recursive searches
    # I don't expect this to be used often, but since it is so little code to maintain,
    # it's easy to keep.
    if recursive == True:
      filter = '**/' + filter
    # Find the most recent file with filter in directory
    return  max(
        list(path.glob(filter)),
        key=os.path.getctime
      )
    