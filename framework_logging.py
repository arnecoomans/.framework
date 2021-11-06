#!/usr/bin/python3
# 
# Framework Logging Core-Module
# Adds bufferd output handling and filtering
#
import sys, os
from datetime import datetime

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
    # Prepare configurable values
    self.min_log_level = 4
    self.max_buffer_size = 16
    # Prepare data containers
    self.buffer = []
    # Development and debugging
    #self.debug('Core Module Logging loaded')
    
  
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
    # Add normalized content to buffer
    self.buffer.append( { 'content': content,
                          'level': level,
                          'datetime': datetime.now()
                        } )
    if len(self.buffer) > self.max_buffer_size:
      self.flush()
    return True
  
  ### Flush
  #   @description pushes all of the log buffer to the output channel(s) 
  #                if the log level is high enough and clears the pushed lines.
  #   @input None
  #   @output (boolean)
  def flush(self) -> True:
    for row in self.buffer:
      if row['level'] <= self.min_log_level:
        self.send_line_to_display(row)
    self.buffer = []

  ##  Shortcuts
  #   These shortcuts can be used to quickly add a message to the log without worrying about
  #   log levels. 
  def throw_error(self, content):
    self.add(content, 1)
    self.flush()
    sys.exit(str(datetime.now())[:-4] + ' Stopping application because of error.')
  def throw_warning(self, content):
    self.add(content, 2)
  def throw_notice(self, content):
    self.add(content, 3)
  def print(self, content):
    self.add(content, 4)
  def debug(self, content):
    self.add(content, 5)

  ##  Input validation
  ### Normalize level
  #   @description normalizes input level as integer within boundaries
  #   @input level (integer)
  #   @output (ineger) [1:5]
  def normalize_level(self, level):
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
      self.debug('Changed display level from ' + str(self.min_log_level) + ' to ' + str(level) + '.')
      self.min_log_level = level



  ##  Output validation
  def send_line_to_display(self, line):
    # Prepend the first line with characterisation
    pre = ''
    if line['level'] == 1:
      pre = '[! Error] '
    elif line['level'] == 2:
      pre = '[w] '
    elif line['level'] == 3:
      pre = '[n] '
    elif line['level'] == 5:
      pre = str(line['datetime'])[:-4] + ' '
    # Print all lines within the content
    for row in line['content']:
      print(pre + row)
      # Reset the prepend to empty space in the same width as the original content
      # This ensures that multiline messages are prepended only once.
      pre = ' '*len(pre)
    