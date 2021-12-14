#!/usr/bin/python3
import sys, os
from pathlib import PosixPath
from importlib import import_module



# Ensure script is embedded and not called directly.
if __name__ == "__main__":
      sys.exit('[FATAL] Quitting. Do not call ' + os.path.basename(__file__) + ' directly.')

# Add Local Shared Lib
importList = [os.path.dirname(os.path.abspath(__file__)),
              os.path.dirname(os.path.abspath(__file__)) + '/modules/',]
for location in importList:
  if location not in sys.path:
    sys.path.append(location)

from framework_logging   import Logging   as Logging
from framework_config    import Config    as Config
from framework_interact  import Interact  as Interact
from framework_files     import Files     as Files
from framework_date      import Date      as Date

class Framework:
  def __init__(self) -> None:
    # Prepare Data Containers
    self.modules = {}
    self.core_module_names = []

    # Load Core Extended Functionality
    self.log      = Logging(self)
    self.files    = Files(self)
    self.config   = Config(self)
    self.interact = Interact(self)
    self.date     = Date(self)

    # Prepare configuration Containers
    # Module Path
    # defines the storage location of .framework modules
    self.module_path = self.getCorePath().joinpath('modules/')

  def run(self):
    # Initialisation
    self.config.parseArgumentParser()
    self.log.logFileInit()
    self.log.debug(['Loaded .framework core with following modules: ', ', '.join(self.core_module_names)])
    
  ## Context management
  def getAppName(self):
    # Get app name from sys.argv. Use Pathlib to return stem
    return self.files.getFile(sys.argv[0]).stem
  def getCorePath(self):
    # Get path of core files (where this file is located)
    return self.files.getDir(os.path.dirname(os.path.abspath(__file__)))
  
  ## Module management
  ### getModule
  #   @description returns the loaded instance of a module
  #   @arguments module(string)
  #   @returns (object)|(None)
  def getModule(self, module):
    if self.isModule(module):
      return self.modules[module]
    elif self.loadModule(module):
      return self.modules[module]
    else:
      return None
  
  ### isModule
  #   @description verifies if a module is loaded
  #   @arguments module(string)
  #   @returns (boolean)
  def isModule(self, module):
    result =  True if module in self.modules else False
    return result
  
  ### loadModule
  #   @description loads a module into Framework operation
  #   @arguments module(string)
  #   @returns (boolean)
  def loadModule(self, module):
    # Check if module is already loaded
    if self.isModule(module):
      self.log.debug('Core.Module: Module ' + module + ' already loaded')
      return True
    else:
      # Verify that module exists
      module_file = self.module_path.joinpath('module_' + module.lower()).with_suffix('.py')
      if module_file.is_file():
        imported_module = import_module(module_file.stem)
        self.modules[module] = getattr(imported_module, module)(self)
        return True
      else:
        if hasattr(self, 'log'):
          self.log.throw_error(['Core.Module: An error occured when trying to load module "' + module + '".', 
                                'The module file "' + module_file.name  + '" was not found', 
                                'or the class could not be loaded.'])

  
  def listModules(self):
    return list(self.modules.keys())
        
      