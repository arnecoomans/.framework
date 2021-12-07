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
      
      if not path.is_absolute():
        path = Path.cwd() / path
    return path
    
  def getDir(self, path=None):
    if path is None or path is False or len(str(path).strip()) == 0:
      path = self.getPath()
    elif type(path) is not posixpath:
      path = self.getPath(path)
    if path.is_file():
        path = path.parent
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
  
  def getType(self, path):
    if type(path) is not posixpath:
      path = Path(path)
    # Iterate over types
    if path.is_dir():
      return 'dir'
    elif path.is_file():
      return 'file'
    elif path.is_absolute():
      return 'absolute'
    elif path.is_block_device():
      return 'block_device'
    elif path.is_char_device():
      return 'char_device'
    elif path.is_fifo():
      return 'fifo'
    elif path.is_mount():
      return 'mount'
    elif path.is_reserved():
      return 'is_reserved'
    elif path.is_socket():
      return 'socket'
    elif path.is_symlink():
      return 'symlink'
    else:
      self.throw_error('Files.getType: Error when trying to determine file type of \'' + str(path) + '\'.')

  # getRecentFileIn()
  # @description    Retuns the most recent file in a directory.
  #                 If a file is passed as path and the file exists, it is assumed this file is meant
  #                 If a file is passed as path and the file does not exist, the most recent file in
  #                 the parent directory is returned.
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

  # Takes a path and a filename
  # 
  def suggestFilename(self, suggestion=None, path=None, suffix=None, with_date=False, unique=False):
    # Make sure path is posixpath
    if path is None or path is False or len(str(path).strip()) == 0:
      path = self.getPath()
    elif type(path) is not posixpath:
      path = Path(path)
    # If the path has a suffix, assume a file suggestion
    if len(path.suffixes) > 0:
      self.debug('File.suggestFilename: Filename \'' + path.name + '\'detected in path. Moving filename to suggested filename.')
      if suggestion is None:
        suggestion = path.name
      path = path.parent
    # Make sure the path we have now is a full path
    path = self.getPath(path)
    # Make sure suggestion is posixpath, so we can use pathlib logic
    if suggestion is None or len(str(suggestion)) == 0:
      suggestion = Path(self.framework.getAppName())
    elif type(suggestion) is not posixpath:
      suggestion = Path(suggestion)
    # Check if suffix filter needs to be applied
    if suffix is not None:
      report = []
      # If a singlen suffix is supplied, check for single suffix
      if type(suffix) == str and suggestion.suffix != suffix:
        report.append(' '*22 + 'Forcing suffix: Got \'' + suggestion.suffix + '\', expected \'' + suffix + '\'.')
        suggestion = Path(suggestion.stem)
      # If a list of suffixes is supplied, check for multiple suffixes
      elif type(suffix) == list and suggestion.suffixes != suffix:
        report.append(' '*22 + 'Forcing suffix: Got \'' + ''.join(suggestion.suffixes) + '\', expected \'' + ''.join(suffix) + '\'.')
        suggestion = Path(suggestion.stem)
      # If at this time the suggestion does not have a suffix, add it.
      if len(suggestion.suffixes) == 0:
        if len(report) > 0:
          self.debug(['File.suggestFilename: Changing suffix of \'' + suggestion.stem + '\' to \'' + ''.join(suffix) + '\'.'] + report)
        suggestion = suggestion.with_suffix(''.join(suffix))
    # Check to use date
    if with_date is True:
      suggestion = suggestion.with_name(self.getDate() + '-' + suggestion.name)
    #
    # Check if filename should be unique
    if unique is True:
      try_file = path / suggestion
      if try_file.is_file():
        self.debug(['File.suggestFilename: Suggested file \'' + suggestion.name + '\' already exists but should be unique.',
                    ' '*22 + 'Looking for a free followup number for the file.'])
        # See if we can find a file that does not yet exist
        number = 1
        while try_file.with_name(suggestion.stem + '-' + str(number)).with_suffix(''.join(suggestion.suffixes)).is_file():
          number += 1
        suggestion = suggestion.with_name(suggestion.stem + '-' + str(number)).with_suffix(''.join(suggestion.suffixes))
    # Build suggestion path
    suggestion = path / suggestion
    return suggestion
    