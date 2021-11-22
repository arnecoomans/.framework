#!/usr/bin/python3
# 
# Framework Configuration Core-Module
# Process configuration within the application
#
import sys, os
from argparse import ArgumentParser, SUPPRESS
from pathlib import Path, PosixPath


# Ensure script is embedded and not called directly.
if __name__ == "__main__":
      sys.exit('[FATAL] Quitting. Do not call ' + os.path.basename(__file__) + ' directly.')

# Add Local Shared Lib
importList = [os.path.dirname(os.path.abspath(__file__))]
for location in importList:
  if location not in sys.path:
    sys.path.append(location)
from boilerplate_framework import FrameworkBoilerplate as Boilerplate
# Non-standard module import
# This module needs to be installed on the host system. If the module is not installed, give
# installation instruction in the error message
try:
  import yaml
except ImportError:
  sys.exit('System module yaml not found. Please run pip3 install pyyaml.')



class Config(Boilerplate):
  def __init__(self, framework) -> None:
    # Run Boilerplate initialisation
    super().__init__(framework)
    # Prepare reference containers
    self.argument_parser = None
    self.allow_overwrite = True
    # Prepare configurable values
    
    # Prepare data containers
    self.arguments = {}
    # Initialisation
    # Prepare argparse instance to receive argument definitions
    self.prepareArgumentParser()
    # Read application default configuration
    self.loadArgConf('defaults')
    self.handleSpecialArguments()
    
  # All configuration is stored as runtime argument. The --config argument can be used
  # to store arguments for re-use. 
  # Commandline supplied arguments override the --config file supplied arguments

  #   Argument Access
  def setArgument(self, key, value, overwrite=False):
    # Key Normalisation
    key = str(key).lower()
    # Value normalisation
    if type(value) == str:
      if value.lower() == 'true':
        value = True
      elif value.lower() == 'false':
        value = False
      elif value.lower() == 'none':
        value = None
    # Check overwrite
    if not overwrite is True:
      if key in self.arguments:
        return False
    self.arguments[key] = value
    return True

  def getArgument(self, key):
    # Key Normalisation
    key = str(key).lower()
    if key in self.arguments:
      return self.arguments[key]
    else:
      return None




  #   Runtime arguments
  #   Runtime arguments are passed to the application behind the execution command.  
  #   Example:
  #   $ application.py --key: value
  #
  ## read command line arguments
  def prepareArgumentParser(self):
    # Use ArgParse to read arguments, since the arguments can only be read during initialisation
    self.argument_parser = ArgumentParser()
    # Prepare system default argument definitions
    self.argument_parser.add_argument('--config', 
                                      help='Load arguments from configuration template.',
                                      nargs='?',    # Allow 0 or more arguments
                                      const=True,   # When no argument is supplied, use const
                                      type=Path     # Ensure type or supplied argument is Path
                                      )
    self.argument_parser.add_argument('--verbose',
                                      help='Set verbosity (1-5)',
                                      action='store',
                                      type=int,
                                      default=None
                                      )
    self.argument_parser.add_argument('-v',
                                      help=SUPPRESS,
                                      action='count',
                                      default=None
                                      )
    
    self.argument_parser.add_argument('--debug',
                                      #help='Debugging shortcut for verbosity',
                                      action='store_true',
                                      default=None,
                                      help=SUPPRESS
                                      )
    self.argument_parser.add_argument('--source', '-s', 
                                      help='Set source file or path',
                                      action='store',
                                      const=None,
                                      type=Path,
                                      )
    self.argument_parser.add_argument('--destination', '-d', 
                                      help='Set destination file or path',
                                      action='store',
                                      const=None,
                                      type=Path,
                                      )
  
  def parseArgumentParser(self):
    arguments = self.argument_parser.parse_args()
    ##  Normalize known arguments
    ### Verbosity should be between 1 and 5
    if arguments.verbose is not None:
      arguments.verbose = 1 if arguments.verbose < 1 else arguments.verbose
      arguments.verbose = 5 if arguments.verbose > 5 else arguments.verbose
    
    for argument in vars(arguments):
      self.setArgument(key=argument, value=getattr(arguments, argument))
    # Process special arguments
    self.handleSpecialArguments()
  
  def handleSpecialArguments(self):
    ### Configuration template file handling
    if self.getArgument('config') is not None:
      if self.getArgument('config') is True:
        # If appname.py --config is used, the config file app_appname.yml should be loaded.
        # Feed app_appname.
        self.loadArgConf(file=Path('app_' + self.framework.getAppName()))
      else:
        # If a configuration template is supplied, the config file custom_template should be
        # used.
        self.loadArgConf(file=self.getArgument('config').with_name('custom_' + self.getArgument('config').name))
        self.setArgument('config', None)
    # Verbosity
    if type(self.getArgument('v')) is int:
      self.framework.log.setDisplayLevel(self.getArgument('v'))
    if type(self.getArgument('verbose')) is int:
      self.framework.log.setDisplayLevel(self.getArgument('verbose'))

  def loadArgConf(self, file=None):
    # Handle file=bool
    if file is True:
      file = Path('app_' + self.framework.getAppName())
    # Ensure File is PosixPath
    file = file if type(file) is PosixPath else Path(file)
    # Fetch basedir
    base = self.framework.getCorePath() / 'conf/'
    file = base / file.with_suffix('.yml')
    # Check if file exists
    if file.exists():
      # Since we we know the file exists, import it.
      self.debug('Reading configuration from \'' + str(file.with_suffix('.yml').name) + '\'.')
      self.readArgConf(file=base / file.with_suffix('.yml'))
    
  def readArgConf(self, file):
    # Ensure File is PosixPath
    file = file if type(file) is PosixPath else Path(file)
    if not file.exists():
      self.throw_error(['Config:readArgConf -- Error when reading file:', str(file)])
    # File exists. Load into argument placeholder
    with open(file) as configuration_file:
      # Read configuration file
      configuration = yaml.full_load(configuration_file)
      # Check if configuration file is not none
      if configuration is not None:
        # Store configuration keys in argument storage
        for key in configuration:
          self.setArgument(key=key, value=configuration[key], overwrite=self.allow_overwrite)
          if key == 'persistance':
            self.allow_overwrite = configuration[key] if type(key) == bool else False