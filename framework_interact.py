#!/usr/bin/python3
# 
# Framework Logging Core-Module
# Adds bufferd output handling and filtering
#
import sys, os

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
      if len(suggestion) > 0:
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
    display_question += ': '
    #
    # Check if question reference is answered in command line arguments
    # If reference is used:
    if reference is not None:
      # Reference should be the key in the command line argument (--key:value)
      if self.framework.config.getArgument(reference):
        answer = self.framework.config.getArgument(reference)
        # Send answer to display as content (as if it were a question that has been answered)
        self.print(display_question + str(answer) + ' (from command line argument)')
        # Return the answer and stop processing
        return answer
    # Answer is not already given.
    # Asking a question requires that content is displayed. Display level should be at least 4
    if self.framework.log.min_log_level < 4:
      self.framework.log.setDisplayLevel(5)
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