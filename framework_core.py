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
print(sys.path)
from framework_logging   import Logging   as Logging
from framework_config    import Config    as Config
from framework_interact  import Interact  as Interact
from framework_files     import Files     as Files

class Framework:
  def __init__(self) -> None:
    # Prepare Data Containers
    self.modules = {}
    # Load Core Extended Functionality
    self.log      = Logging(self)
    self.config   = Config(self)
    self.interact = Interact(self)
    self.files    = Files(self)

    self.log.debug(['Core is done with loading:', '* core;', '* logging;', '* configuration;', '* interaction.'])
    
    
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
      self.log.debug('Module ' + module + ' already loaded')
      return True
    else:
      # Verify that module exists
      module_path = os.path.dirname(os.path.abspath(__file__)) + '/modules/'
      module_file = 'module_' + module.lower()
      if os.path.isfile(module_path + module_file + '.py'):
        #print('Module ' + module + ' exists, loading')
        imported_module = import_module(module_file)
        module_class = getattr(imported_module, module)
        self.modules[module] = module_class(self)
        return True
      else:
        if hasattr(self, 'log'):
          self.log.throw_error(['An error occured when trying to load module "' + module + '".', 
                                'The module file "module_' + module + '" was not found', 
                                'or the class could not be loaded.'])
  def listModules(self):
    return list(self.modules.keys())
        
      