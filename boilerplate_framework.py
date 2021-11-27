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
  def __init__(self, framework) -> None:
    super().__init__(framework)
    # Store Class name in framework.core_module_names to generate list of loaded modules
    self.framework.core_module_names.append(type(self).__name__)

  