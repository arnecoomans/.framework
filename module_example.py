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
from boilerplate_module import ModuleBoilerplate as Boilerplate
from framework_core import Framework

class example(Boilerplate):
  def __init__(self, framework) -> None:
    super().__init__(framework, modulename=__name__[7:])
    self.print('Module \'Example\' loaded')
    

  