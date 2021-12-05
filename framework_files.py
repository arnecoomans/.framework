#!/usr/bin/python3
# 
# Framework Logging Core-Module
# Adds bufferd output handling and filtering
#
import posixpath
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
from boilerplate_framework import FrameworkBoilerplate as Boilerplate

class Files(Boilerplate):
  def __init__(self, framework) -> None:
    # Run Boilerplate initialisation
    super().__init__(framework)
    # Prepare reference containers
    # Prepare configurable values
    # Prepare data containers
    # Initialisation

  # GetPath
  # Returns the given input as path-object
  def getPath(self, path=None):
    if path is None:
      return Path.cwd()
    elif type(path) is not PosixPath and len(path) == 0:
      return Path.cwd()
    else:
      # Return path as PosixPath
      path = path if type(path) is PosixPath else Path(path)
      if path.is_file():
        path = path.parent
      if not path.is_absolute():
        path = Path.cwd() / path
    return path

  def getFile(self, file=None, exists=False):
    if file == None or file == '':
      self.throw_error(['Files.getFile: Error when converting filename to file in path-object in files:getFile(). No filename supplied.'])
    elif type(file) is not PosixPath:
      file = Path(file)
    if not file.is_absolute():
      file = Path.cwd() / file
    if exists == True and not file.is_file():
      self.throw_warning(['Files.getFile: File reference supplied is not a file:', '- ' + str(file)])
      return None
    return file
  

  # getRecentFileIn()
  # Returns suggestion if file exists
  # 
  # 
  def getRecentFileIn(self, path=None,
                            filter=None, recursive=False, method='modified'):
    # Normalize Path
    # If Path is None, False or empty, get default path object
    if path is None or path is False or len(str(path).strip()) == 0:
      path = self.getPath()
    # Force path to be posixPath object
    elif type(path) is not posixpath:
      path = Path(path)
    #
    # If a file is supplied as path:
    if path.is_file():
      # An existing file is supplied.
      # Check if file matches filter
      if filter is not None:
        if path.suffix in filter:
          # An existing file is supplied that is verified
          return self.getFile(path)
        # Filter does not match, proceed with the parent directory of the file as path
        if path.suffix not in filter:
          self.debug('files:getRecentFileIn: ' + path.name + ' does not match filter ' + filter )
          path = self.getPath(path.parent)
    elif path.is_dir():
      pass
    else:
      path = path.parent
    #
    # Proceed with default path, original supplied path or parent path of invalid file
    if path.is_dir():
      path = self.getPath(path)
      self.debug('Files:getRecentFileIn: Getting most recent file in ' + str(path))
      return self.getRecentFileInDirectory(path=path, filter=filter, recursive=recursive, method=method)
    else:
      # This should not occur, that warrants a notice
      self.throw_notice('Files:getRecentFileIn: Unable to find file in ' + path.name + '.')
      return None


  def getRecentFileInDirectory(self, path=None, filter=None, recursive=False, method='modified'):
    # Normalize Path
    path = self.getPath(path)
    # Normalize method
    method = method[:1].lower() if len(method) > 0 else 'm'
    # Normalize filter
    # No filter
    if filter == None or filter == False or len(filter) == 0:
      filter = ''
    # Everything filter
    elif filter == '*' or filter == '*.*':
      filter = '*'
    # Extention without . supplied
    elif filter[0:1] != '.':
      filter = '.' + filter
    filter = '*' + filter
    # Allow for recursive searches
    # I don't expect this to be used often, but since it is so little code to maintain,
    # it's easy to keep.
    if recursive == True:
      filter = '**/' + filter
    # Find the most recent file with filter in directory
    if method == 'c':
      try:
        files = list(path.glob(filter))
        for file in files:
          if not file.is_file():
            files.remove(file)
        return max(
          files,
          key=os.path.getctime # Use getctime for recentlt created, getmtime for recently modified
        )
      except ValueError:
        return None
    else:
      try:
        files = list(path.glob(filter))
        for file in files:
          if not file.is_file():
            files.remove(file)
        return max(
          files,
          key=os.path.getmtime # Use getctime for recentlt created, getmtime for recently modified
        )
      except ValueError:
        return None

  