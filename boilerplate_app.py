#!/usr/bin/python3
import sys, os

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
from framework_core import Framework

class AppBoilerplate(Boilerplate):
  def __init__(self) -> None:
    # Loads Framework
    self.framework = Framework()
    # Run Boilerplate initialisation
    super().__init__(self.framework)
  

  def ask(self, question, reference=None, suggestion=None):
    # If the framework interact module is loaded, use it since it.
    if hasattr(self.framework, 'interact'):
      return self.framework.interact.ask(question=question, reference=reference, suggestion=suggestion)
    else:
      # If the framework interact module is not loaded, only display the basic question and pass back the answer
      return input(question)