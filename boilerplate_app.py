#!/usr/bin/python3
#
# Boilerplate: App
# Part of the cmns.framework
# Holds shortcuts available to any app
# @author     Arne Coomans
# @version    0.0.1
# @url        https://github.com/arnecoomans/.framework/
# 

# Import system python modules
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
from framework_core import Framework
from boilerplate_common import CommonBoilerplate as Boilerplate

class AppBoilerplate(Boilerplate):
  def __init__(self) -> None:
    # Loads .framework
    self.framework = Framework()
    # Run Boilerplate initialisation
    super().__init__(self.framework)

  #   Shortcuts available to apps
  ## Core functions
  def run(self):
    return self.framework.run()
    
  ##  Module management shortcuts
  ### loadModule
  #   @arguments     module [string] (module-name)
  #   @returns       module-object
  #   @description   Loads a module via the .framework.loadModule dynamic module loader
  def loadModule(self, module):
    return self.framework.loadModule(module)
  ### getModule
  #   @arguments     module (module-name)
  #   @returns       module-object
  #   @description   Returns a loaded module via the .framework.loadModule dynamic module loader
  def module(self, module):
    return self.framework.getModule(module)
  
  ##  Interaction shortcuts
  ### ask
  #   @arguments     question [string], reference [string], suggestion [string|bool|int]
  #   @returns       answer [string]
  #   @description   Presents the user with a question.
  #                  Presents suggestion if supplied, that is accepted with ease
  #                  If the question is answered via command-line arguments, the answer is used.
  def ask(self, question, reference=None, suggestion=None):
    # If the framework interact module is loaded, use it since it.
    if hasattr(self.framework, 'interact'):
      return self.framework.interact.ask(question=question, reference=reference, suggestion=suggestion)
    else:
      # If the framework interact module is not loaded, only display the basic question and pass back the answer
      return input(question)