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

class readcsv(Boilerplate):
  def __init__(self, framework) -> None:
    super().__init__(framework, modulename=__name__[7:])
    # Prepare reference containers
    # Prepare configurable values
    self.supportedSeperatorCharacters = [ '";"', '\';\'', 
                                          '","', '\',\'', 
                                          '"|"', '\'|\'',
                                          "\"\t\"", "'\t'",
                                          ';',
                                          ',',
                                          '|',
                                          "\t",
                                          ]
    # Prepare data containers

  def read(self, source, header=False):
    # Ensure file is PosixPath object
    if type(source) is not PosixPath:
      file = Path(source)
    # Verify that file exists
    if not file.exists():
      self.throw_error(['ReadCSV: Error when trying to read \'' + str(file) + '\'.', 'File does not exist.'])
    elif not file.suffix in ['.csv', '.txt']:
      self.throw_error(['ReadCSV: Error when trying to read \'' + str(file) + '\'.', 'File suffix \'' + file.suffix + '\' is not supported.'])
    # Open file
    self.debug('ReadCSV: Reading ' + str(source))
    with open(source) as f:
      # Convert sourcefile to stored list
      # Use rstrip() to ensure there are no whitespaces in the read line
      file_contents = [line.rstrip() for line in f]
    # The file is now stored in file_contents line by line
    # Check if file length is >0
    if len(file_contents) == 0:
      self.throw_error(['Error while reading file;', str(source) + ' is empty and cannot be read.'])
    # Prepare parsing result container
    result = []
    # Detect seperation character
    seperation_character = self.guessSeperatorCharacter(file_contents[0])
    self.debug('ReadCSV: Detected seperation character: ' + seperation_character)
    # Detect and process header
    if header == True:
      # Fetch first line of file as header and split by seperation character
      building_header = file_contents.pop(0).strip().split(seperation_character)
      header = {}
      index = 0
      # Loop through the fields and normalize
      while index < len(building_header):
        # If the column header has content, use content as header name. Else use index
        header[index] = building_header[index].strip() if len(building_header[index].strip()) > 0 else index
        index += 1
    # Process all lines in the read content
    for line in file_contents:
      # Only process lines that actually have content
      if len(line.replace(seperation_character, '')) > 0:
        # Convert the line into a list based on the previously detected seperation character
        line = line.strip().split(seperation_character)
        # Add keys
        indexed_line = {}
        # Check if header should be used to store key: value
        if header == False:
          # Use column index as key
          for column in line:
            indexed_line = { line.index(column): column}
        else:
          # Find header name for column index
          for column in line:
            if len(column.strip()) > 0:
              # Verivy that the column has a header
              if line.index(column) in header:
                indexed_line[header[line.index(column)]] = column.strip()
              else:
                indexed_line[line.index(column)] = column.strip()
        # Make sure all keys are present in the result
        for key in header:
          if header[key] not in indexed_line:
            indexed_line[header[key]] = ''
        # Store the parsed result
        result.append(indexed_line)
    # Return the parsed result
    return result
    
  def guessSeperatorCharacter(self, line):
    for character in self.supportedSeperatorCharacters:
      if character in line:
        return character
    self.throw_error(['ReadCSV: Error when detecting csv-delimiter. No character detected.', 'Supported characters are: ' + ', '.join(self.supportedSeperatorCharacters)])


  def write(self, target=None, data=[], seperator=','):
    if target == None:
      self.throw_error('Data was sent to output file but no filename was specified')
    self.debug(target)
    self.flush()
    target = self.getFile(target)
    self.debug(target)
    self.flush()
    with open(target, 'w') as f:
      for line in data:
        f.write(seperator.join(line) + "\n")
    f.close() 