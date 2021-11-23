#!/usr/bin/python3
# 
# Framework Date and Time Core-Module
# 
#
import sys, os
from datetime import datetime, date, time

# Ensure script is embedded and not called directly.
if __name__ == "__main__":
      sys.exit('[FATAL] Quitting. Do not call ' + os.path.basename(__file__) + ' directly.')

# Add Local Shared Lib
importList = [os.path.dirname(os.path.abspath(__file__))]
for location in importList:
  if location not in sys.path:
    sys.path.append(location)
from boilerplate_framework import FrameworkBoilerplate as Boilerplate

class Date(Boilerplate):
  def __init__(self, framework) -> None:
    # Run Boilerplate initialisation
    super().__init__(framework)
    # Prepare reference containers
    # Prepare configurable values
    # Prepare data containers
    # Initialisation
    self.now = datetime.now()

  def getDate(self, format='%Y-%m-%d'):
    # Allow format to be a textual shortcut
    if format == 'natural':
      format = '%d-%m-%Y'
    elif format == 'standard':
      format = '%Y-%m-%d'
    elif format == 'monthname':
      format = '%d-%M-%Y'
    return self.now.strftime(format)

  def getTime(self, format='%H:%M:%S'):
    return self.now.strftime(format)

  def getDateTime(self):
    return self.getDate() + ' ' + self.getTime()
  
  
  def getAge(self, origin):
    if not type(origin) is datetime:
      origin = datetime(origin)
    return self.now - origin