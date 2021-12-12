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
    # Prepare reference containers
    # Prepare configurable values
    # Prepare data containers
    self.questions = {}
    # Initialisation

  def ask(self, question, reference=None, suggestion=None):
    # Normalisation
    # Make sure suggestion is a string or None
    if suggestion is not None:
      if len(str(suggestion)) > 0:
        suggestion = str(suggestion)
      else:
        suggestion = None
    # Make sure reference is a string or None
    if reference is not None:
      reference = str(reference)
    # Prepare displayable question
    display_question = '' + str(question)
    if suggestion is not None:
      display_question += ' (\'' + suggestion + '\')'
      if self.getArgument('yes') == True:
        self.print(display_question + ': ' + str(suggestion) + ' (accepted suggestion)' )
        return suggestion
    display_question += ': '
    #
    # Check if question reference is answered in command line arguments
    # If reference is used:
    if reference is not None:
      # Reference should be the key in the command line argument (--key:value)
      if self.framework.config.getArgument(reference):
        answer = self.framework.config.getArgument(reference)
        # Send answer to display as content (as if it were a question that has been answered)
        self.print(display_question + str(answer) + ' (accepted suggestion)')
        # Return the answer and stop processing
        return answer
    # Answer is not already given.
    # Asking a question requires that content is displayed. Display level should be at least 4
    if self.framework.log.min_log_level == 1:
      self.framework.log.setDisplayLevel(2)
      # Make sure there's no content buffer left !!
      self.flush()
    # Display question and request input for answer
    # Make sure content buffer is flushed
    self.flush()
    answer = input(display_question).strip()
    # Process answer
    # If a suggestion is given, certain values (empty, y and yes) should be processed differently
    if suggestion is not None:
      if answer in ['', 'y', 'yes']:
        answer = suggestion
    # If an answer is True or False, convert to boolean
    if answer.lower() == 'true':
      answer = True
    elif answer.lower() == 'false':
      answer = False
    # If answer is (still) empty, return None
    if len(answer) == 0:
      answer = None
    # Store answer
    if reference is not None:
      self.questions['reference'] = {'question': question, 'answer': answer, 'suggestion': suggestion}
    # Return processed answer
    return answer


  def ask2(self, question=None, suggestion=None, reference=None):
    # Verify Question
    if question is None or question is False or len(str(question)) == 0:
      # No question is supplied.
      self.throw_warning('Interact.ask: Interaction is initiated but no question formulated.')
      # Return suggestion if supplied
      return self.get_suggested_answer(None, suggestion) if suggestion is not None else False
    # Question is given
    # Build display question
    display_question   = self.get_display_question(question)
    display_suggestion = self.get_display_suggestion(suggestion)
    display_answer     = self.get_display_answer(self.getArgument(reference))

    if len(display_suggestion) > 0:
      display_suggestion = ' (' + display_suggestion + ')'
    # Display processed question
    self.print(display_question + display_suggestion + ': ' + display_answer)
    


  def get_display_question(self, question):
    question = question if question[-1:] == '?' else question + '?'
    # Force fist letter to be uppercase
    if not question[:1].isupper():
      question = question[:1].upper() + question[1:]
    return question 


  def get_display_suggestion(self, suggestion=None, underline_default=True):
    if type(suggestion) == str:
      return suggestion
    elif type(suggestion) is list:
      result = []
      for item in suggestion:
        result.append(self.get_display_suggestion(item).strip())
      if len(result) > 0 and underline_default is True:
        result[0] = "\033[92m" + result[0] + "\033[0m"
      return ' / '.join(result)
    elif type(suggestion) is dict:
      result = []
      for item in suggestion.values():
        result.append(self.get_display_suggestion(item).strip())
      if len(result) > 0 and self.getArgument('coloured') is True:
        result[0] = "\033[92m" + result[0] + "\x1B[0m"
      return ' / '.join(result)
    elif type(suggestion) is PosixPath:
      if str(self.getPath()) in str(suggestion):
        return '.' + str(suggestion).replace(str(self.getPath()), '')
      else:
        return str(suggestion)
    return ''

  def get_display_answer(self, answer=None):
    if answer is not None and answer is not False and len(str(answer)) > 0:
      if self.getArgument('coloured') is True:
        return str(answer + ' (' + "\033[94m" + 'from command line argument' + "\x1B[0m" + ')')
      else:
        return str(answer + ' (from command line argument)')
    return ''

  
  def get_suggested_answer(self, answer, suggestion=None):
    # If no suggestion is given, return the answer. No further processing is required
    if suggestion is None or suggestion is False or len(str(suggestion)) == 0:
      return answer
    # A suggestion is given

    if type(suggestion) == str:
      suggestion = [suggestion]