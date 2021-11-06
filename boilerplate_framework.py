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
from boilerplate_common import CommonBoilerplate as Boilerplate
#from framework_core import Framework

class FrameworkBoilerplate(Boilerplate):
  def __init__(self, framework, frameworkmodulename='') -> None:
    super().__init__(framework)
    self.frameworkmodulename = frameworkmodulename
    
  def log(self, content, level=None):
    if hasattr(self.framework, 'log'):
      return self.framework.log.add(content=content, level=level)
    # For framework messages; only print notice, warning and error messages.
    elif int(level) <= 3:
      if type(content) is list:
        for line in content:
          print(line)
      else:
        print(content)