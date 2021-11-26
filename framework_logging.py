#!/usr/bin/python3
# 
# Framework Logging Core-Module
# Adds bufferd output handling and filtering
#
import sys, os
from datetime import datetime
#import logging # https://docs.python.org/3/library/logging.html

# Ensure script is embedded and not called directly.
if __name__ == "__main__":
      sys.exit('[FATAL] Quitting. Do not call ' + os.path.basename(__file__) + ' directly.')

# Add Local Shared Lib
importList = [os.path.dirname(os.path.abspath(__file__))]
for location in importList:
  if location not in sys.path:
    sys.path.append(location)
from boilerplate_framework import FrameworkBoilerplate as Boilerplate

class Logging(Boilerplate):
  def __init__(self, framework) -> None:
    # Run Boilerplate initialisation
    super().__init__(framework)
    # Prepare reference containers
    self.logfile_target           = None
    self.logfile_suffix           = '.log'
    self.logfile_write_mode       = 'w'    # Supports a for append en w for (over)write
    self.logfile                  = None   # Reference to file in open
    # Prepare configurable values
    self.min_log_level            = 2
    self.min_logfile_level        = 0
    self.max_display_buffer_size  = 16
    # Prepare data containers
    self.buffer                   = []     # For pushing to screen
    self.file_buffer              = []     # For pushing to file
    # Development and debugging

  def __del__(self):
    if self.logfile is not None: 
      # Try to flush buffer
      try:
        self.flush()
      except:
        pass
      # Try to close the write connection to the logfile
      try:
        self.logfile.close()
      except:
        pass

  # Log file initialisation
  def logFileInit(self):
    # Check if logging to file should be enabled.
    if self.getArgument('logfile'):
      # Log file is enabled: Set logfile target
      self.setLogFileTarget(target=self.getArgument('logfile'))
      # Set logfile display level
      if not self.getArgument('logfile_verbose') is None:
        self.setLogFileVerbose(level=self.getArgument('logfile_verbose'))
      # Set logfile write mode
      if self.getArgument('logfile_append') is True:
        self.setLogFileWriteMode('append')
    # If argument is not set, no action is to be taken

  #   Log file functions
  def setLogFileTarget(self, target):
    # If no filename is supplied, assume default format of log file name
    if target == True:
      target = self.getFile(self.getDate() + '-' + self.framework.getAppName())
    else:
      # Log file name is supplied
      target = self.getFile(target, exists=False)
    # Use suffix if supplied, else add locally configured default
    # Store target in local storage
    self.logfile_target = target if len(target.suffixes) > 0 else target.with_suffix(self.logfile_suffix)
    # Log intended file usage.
    self.throw_notice('Log to file: Logging to: \'' + str(self.logfile_target.name) + '\'.')

  def setLogFileVerbose(self, level=None):
    # If an invalid level is supplied, use default log level
    if not type(level) is int:
      level = self.min_logfile_level
    # Use self.normalise_level to normalise level between 1 and 5.
    # However, level 0 should also be supported as shortcut to only show level 2 content and not level 1 errors.
    # So if level is smaller than 0, use 0, else use normalized level
    level = 0 if level <= 0 else self.normalize_level(level)
    if not level == self.min_logfile_level:
      self.debug('Changed logfile display level from \'' + str(self.min_logfile_level) + '\' to \'' + str(level) + '\'.')
      self.min_logfile_level = level
    
  def setLogFileWriteMode(self, mode='w'):
    # Supports 'a' or 'append' as mode to set append mode
    # Defaults to 'w' (over)write mode
    self.logfile_write_mode = 'a' if mode[:1] == 'a' else 'w'
  
  def sendLineToLogFile(self, line):
    if self.logfile_target is not None:
      pre = str(line['datetime'])[:-4] + ' (' + self.getTextualLevel(line['level']) + '): '
      for row in line['content']:
        if line['level'] == 2:
          pre = ''
        self.getLogFile().write(pre + row + "\n")
        pre = ' '*len(pre)

  def getLogFile(self):
    if self.logfile is None:
      self.logfile = open(self.logfile_target, self.logfile_write_mode)
      if self.min_logfile_level >= 3:
        self.logfile.write(str(datetime.now())[:-4] + ': Running app \'' + self.framework.getAppName() + '\' in \'' + str(self.getPath()) + "'\n")
      if self.min_logfile_level == 5:
        self.logfile.write(str(datetime.now())[:-4] + ': $ \'' + ' '.join(sys.argv) + '\'.' + "\n")
    return self.logfile

  def getTextualLevel(self, level):
    if level == 1:
      return ' ERROR '
    elif level == 2:
      return '       '
    elif level == 3:
      return 'WARNING'
    elif level == 4:
      return 'NOTICE '
    else:
      return ' DEBUG '

  ##  Log Buffer
  ### Add
  #   @description adds content to the log buffer, addes log-level and date/time
  #   @arguments content (string|list)
  #              level (integer) [1:5]
  #   @output (boolean)
  def add(self, content='', level=4):
    # Normalize input
    level = self.normalize_level(level)
    content = self.normalize_content(content)
    # Add normalized content to display-buffer
    self.buffer.append( { 'content': content,
                          'level': level,
                          'datetime': datetime.now() # Use datetime and not framework date module 
                                                     # because timing keeps changing.
                        } )
    # Add normalized content to file-buffer
    self.file_buffer.append( { 'content': content,
                               'level': level,
                               'datetime': datetime.now() # Use datetime and not framework date module 
                                                          # because timing keeps changing.
                            } )
    # Flush display buffer if max buffer size is reached
    if len(self.buffer) > self.max_display_buffer_size:
      self.flush()
    return True
  
  ### Flush
  #   @description pushes all of the log buffer to the output channel(s) 
  #                if the log level is high enough and clears the pushed lines.
  #   @input None
  #   @output (boolean)
  def flush(self) -> True:
    for row in self.buffer:
      # Process displaying content to screen
      if row['level'] <= self.min_log_level:
        self.sendLineToDisplay(row)
      # Process writing content to file
      if row['level'] <= self.min_logfile_level:
        self.sendLineToLogFile(row)
      elif self.min_logfile_level == 0 and row['level'] == 2:
        self.sendLineToLogFile(row)
    self.buffer = []

  ##  Shortcuts
  #   These shortcuts can be used to quickly add a message to the log without worrying about
  #   log levels. 
  def throw_error(self, content):
    self.add(content, 1)
    self.flush()
    sys.exit(str(datetime.now())[:-4] + ' Stopping application because of error.')
  def print(self, content):
    self.add(content, 2)
  def throw_warning(self, content):
    self.add(content, 3)
  def throw_notice(self, content):
    self.add(content, 4)
  def debug(self, content):
    self.add(content, 5)

  ##  Input validation
  ### Normalize level
  #   @description normalizes input level as integer within boundaries
  #   @input level (integer)
  #   @output (ineger) [1:5]
  def normalize_level(self, level=5):
    return level if level in range(1,5) else 5

  ### Normalize content
  #   @description normalizes input to a uniform format while allowing flexible input
  #   @input content (string|list|dict|integer|boolean)
  #   @output [list] containing [string(s)]
  def normalize_content(self, content):
    if type(content) is str:
      # A string is supplied. A list is expected. Pack the string in a list
      content = [content]
    elif type(content) is int:
      # An integer is supplied. A list is expected. Pack the string representation of the integer in a list
      content = [str(content)]
    elif type(content) is dict:
      # A dict is supplied. A list is expected. Convert dict to list
      new = []
      for row in content:
        if type(content[row]) is list:
          line = ', '.join(content[row])
        elif type(content[row]) is dict:
          line = []
          for item in content[row]:
            line.append(item + ': ' + str(content[row][item]))
        else:
          line = str(content[row])
        new.append(str(row) + ': ' + str(line))
      content = new
    elif type(content) is list:
      # A list is supplied. A string packed list is expected. Enforce each entry in the list is a string.
      new = []
      for row in content:
        line = row if type(row) is str else str(row)
        new.append(line)
      content = new
    else:
      # If we do not know what to do, enforce a string packed list
      content = [str(content)]
    # Return the processed content
    return content
  
  def setDisplayLevel(self, level):
    if not type(level) is int:
      return False
    elif level < 1:
      level = 1
    elif level >5:
      level = 5
    if not level == self.min_log_level:
      self.debug('Changed display level from \'' + str(self.min_log_level) + '\' to \'' + str(level) + '\'.')
      self.min_log_level = level



  ##  Output validation
  def sendLineToDisplay(self, line):
    # Prepend the first line with characterisation
    pre = pre = str(line['datetime'])[:-4] + ' ' if line['level'] == 5 else ''
    pre += '[' + self.getTextualLevel(line['level']) + '] '
    pre = '' if line['level'] == 2 else pre
    # Print all lines within the content
    for row in line['content']:
      print(pre + row)
      # Reset the prepend to empty space in the same width as the original content
      # This ensures that multiline messages are prepended only once.
      pre = ' '*len(pre)
  
  
    