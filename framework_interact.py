#!/usr/bin/python3
# 
# Framework Logging Core-Module
# Adds bufferd output handling and filtering
#
import sys, os
from pathlib import PosixPath, posixpath

# Ensure script is embedded and not called directly.
if __name__ == "__main__":
      sys.exit('[FATAL] Quitting. Do not call ' + os.path.basename(__file__) + ' directly.')

# Add Local Shared Lib
importList = [os.path.dirname(os.path.abspath(__file__))]
for location in importList:
  if location not in sys.path:
    sys.path.append(location)
from boilerplate_framework import FrameworkBoilerplate as Boilerplate

class Interact(Boilerplate):
  def __init__(self, framework) -> None:
    # Run Boilerplate initialisation
    super().__init__(framework)
    # Prepare data containers
    self.questions = {}
    
  def ask(self, question=None, suggestion=None, default=None, reference=None):
    # Verify Question
    if question is None or question is False or len(str(question)) == 0:
      # No question is supplied.
      self.throw_warning('Interact.ask: Interaction is initiated but no question formulated.')
      # Return suggestion if supplied
      return self.get_suggested_answer(None, suggestion) if suggestion is not None else False
    # Question is given
    # Build displayable question
    display_question   = self.get_display_question(question)
    display_suggestion = self.get_display_suggestion(suggestion, default=default)
    display_answer     = self.get_display_answer(self.getArgument(reference))
    # Add ( and ) to suggestion if supplied
    if len(display_suggestion) > 0:
      display_suggestion = ' (' + display_suggestion + ')'
    #
    # Display processed question, building a result
    result = None
    # If accept input is forced using arguments, and an answer is supplied via command line
    # arguments or one or more suggestions are given
    if self.getArgument('force_accept_input') and \
       len(display_suggestion) > 0 or \
       len(display_answer) > 0:
      # If the commandline reference is passed, the answer should be the commandline reference
      if len(display_answer) > 0:
        self.debug('Interact.ask: Getting answer, using commandline reference.')
        result = self.getArgument(reference)
      # Else, use suggestion
      else:
        # When suggestion is a list or a dict, use the first value from suggestion
        if default is not None:
          self.debug('Interact.ask: Getting answer, default value.')
          result = str(default)
        elif type(suggestion) is list:
          self.debug('Interact.ask: Getting answer, using first suggestion.')
          result = suggestion[0]
        elif type(suggestion) is dict:
          self.debug('Interact.ask: Getting answer, using first suggestion.')
          result = list(suggestion.keys())[0]
        else:
          self.debug('Interact.ask: Getting answer, using suggestion.')
          result = suggestion
      # Display the question plus the answer
      self.print(display_question + display_suggestion + ': ' + str(result))
    else:
      # Before sending content to display, make sure the content buffer is flushed
      self.flush()
      # Use input() to get user input
      result = input(display_question + display_suggestion + ': ')
    # Process resulting input, processing special characters such as enter and yes
    result = self.get_processed_user_input(input=result, suggestion=suggestion, default=default)
    # Return processed input
    return result


  def get_display_question(self, question):
    question = question if question[-1:] == '?' else question + '?'
    # Force fist letter to be uppercase
    if not question[:1].isupper():
      question = question[:1].upper() + question[1:]
    return question 


  def get_display_suggestion(self, suggestion=None, underline_default=True, default=None):
    # If a single suggestion is given, return suggestion
    if type(suggestion) is str or \
       type(suggestion) is int or \
         type(suggestion) is bool:
      # If the current value is the default value and colour highlighting is enabled,
      # highlight the default value.
      if self.getArgument('coloured') is True and str(suggestion) == str(default):
        return "\033[92m" + str(suggestion) + "\x1B[0m"
      else:
        return str(suggestion)
    # If single suggestion is posixpath, return the best possible version of this file
    elif type(suggestion) is PosixPath:
      # Check if path is relative to current path
      # @todo use https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.relative_to
      if str(self.getPath()) in str(suggestion):
        return '.' + str(suggestion).replace(str(self.getPath()), '')
      else:
        return str(suggestion)
    #
    # Multiple Suggestions:
    #
    # If suggestion is list, return a joined string of the list
    elif type(suggestion) is list:
      result = []
      # Recursively clean up each entry
      for item in suggestion:
        if len(str(item).strip()) > 0:
          result.append(self.get_display_suggestion(item, default=default).strip())
      # Highlight the default option if this is not yet done
      if self.getArgument('coloured') is True and \
         "\033[92m" + str(default) + "\x1B[0m" not in result:
        result[0] = "\033[92m" + result[0] + "\x1B[0m"
      return ' / '.join(result)
    # If suggestion is dict, return joined string of dict values
    elif type(suggestion) is dict:
      result = []
      # Recursively clean up each entry
      for item in suggestion.values():
        if len(str(item).strip()) > 0:
          result.append(self.get_display_suggestion(item, default=default).strip())
      # Highlight the default option if this is not yet done
      if self.getArgument('coloured') is True and \
         "\033[92m" + str(default) + "\x1B[0m" not in result:
        result[0] = "\033[92m" + result[0] + "\x1B[0m"
      return ' / '.join(result)
    # No value is given, return empty string
    return ''

  def get_display_answer(self, answer=None):
    if answer is not None and answer is not False and len(str(answer)) > 0:
      if self.getArgument('coloured') is True:
        return str(answer) + ' (' + "\033[94m" + 'from command line argument' + "\x1B[0m" + ')'
      else:
        return str(answer) + ' (from command line argument)'
    return ''

  def get_processed_user_input(self, input, suggestion=None, default=None):
    self.debug('Processing ' + str(input))
    # Clean up input and output
    input = str(input).strip()
    result = None
    # Agree with suggestion
    # [enter]. y and yes are seen as in agreement with suggestion
    if len(input) == 0 or \
       str(input).lower() == 'yes' or str(input).lower() == 'y':
      # Use default
      if default is not None:
        self.debug('Interact.process: Accepting default value \'' + str(default) + '\'.' )
        result = str(default)
      # Use suggestion if single suggestion is supplied
      elif type(suggestion) is str or type(suggestion) is int or type(suggestion) is bool:
        self.debug('Interact.process: Accepting suggested value \'' + str(suggestion) + '\'.' )
        result = str(suggestion)
      elif type(suggestion) is list:
        self.debug('Interact.process: Accepting first suggested value \'' + str(suggestion[0]) + '\'.' )
        result = str(suggestion[0])
      elif type(suggestion) is dict:
        self.debug('Interact.process: Accepting first suggested key \'' + str(list(suggestion.keys())[0]) + '\'for value \'' + str(list(suggestion.values())[0]) + '\'.' )
        result = str(list(suggestion.keys())[0])
      elif type(suggestion) is PosixPath:
       self.debug('Interact.process: Accepting suggested file \'' + suggestion.name + '\'.')
       result = suggestion
      elif input.lower() == 'yes' or input.lower() == 'y':
        # Exception case; if YES is not supplied as special value but as expected value, it should be
        # passed back. 
        result = input
      elif len(str(input)) == 0:
        # Enter is pressed but no suggestion or default value is present. 
        self.throw_notice('Interact.process: No answer is given to a question without suggestion or default value. Nothing to return.')
        result = None
      else:
        self.debug('Interact.process: Unhandled approval type for suggestion \'' + str(suggestion) + '\' (' + str(type(suggestion).__name__) + ').')
    # Input is given, check if input is within suggestion options
    # If a list of suggestions is given, the answer should be in list. If it is not, throw 
    # an oud-of-bounds warning.
    elif type(suggestion) is list:
      # Create compare list with options as string, so comparison with input can be made.
      compare_list = []
      for item in suggestion:
        compare_list.append(str(item).strip())
      # Check if answer is in available suggested options
      if input in compare_list:
        result = input
      else:
        self.throw_warning('Interact.process: Input \'' + input + '\' out of bounds for range \'' + ', '.join(compare_list) + '\'.')
        result = None
    # If a dict of suggestions is given, the answer should be a value in the dict.
    # The corresponding dict key should be returned.
    elif type(suggestion) is dict:
      # Create compare list with options as string, so comparison with input can be made.
      compare_list = []
      for item in suggestion.values():
        compare_list.append(str(item).strip())
      # Check if answer is in available suggested values
      if input in compare_list:
        index = compare_list.index(input)
        result = list(suggestion.keys())[index]
      else:
        self.throw_warning('Interact.process: Input \'' + input + '\' out of bounds for range \'' + ', '.join(compare_list) + '\'.')
        result = None
    # Handle booleans
    elif str(input).lower() == 'true':
      result = True
    elif str(input).lower() == 'false':
      result = False
    # By now we've handled about all exeptions and we can assume
    # - a single suggestion is given, so no validation is required
    # - no special value is given, so no translation is required
    else:
      result = str(input)
    return result