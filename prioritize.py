import sys
sys.path.append("C:\\SourceCode\\PersonalRepo\\Python\\LexLib")
from task import *
from iofactory import *
from page import Graph

class Message():

  """ Constant class for messages """

  Welcome = ("-----------------------------------\n"
             " Welcome to Alex's priority machine!\n"
             "-----------------------------------\n\n")
  EnterPriorityName = ("\n--------------------------------------------------------------\n"
                       " Please enter the name of a priority (ex. Sleep): (done to end) ")
  AskForMore = ("\n-----------------------------------------\n"
                " Do you have more priorities to add? (y/n) ")
  EnterImportance = ("\n-----------------------------------------\n"
                     " How important is #PRIORITY# to you: (1-5) ")
  EnterUrgency = ("\n-------------------------------------\n"
                  " How urgent is #PRIORITY# to you: (1-5) ")
  EnterPriorityValue = ("\n-------------------------------------------------------------\n"
                        " Which is a higher priority, #PRIORITYA# or #PRIORITYB#? (a/b) ")
  PrintPriorities = ("\n--------------------------\n"
                     " Your sorted priorities are:\n")


  CompareSkipped = "There is only one priority: priority comparision skipped\n"
  InvalidRange = "Number entered was outside valid range\n"
  InvalidInput = "Value entered was not a valid number\n"

class Replace():

  """ Constant class for replacements """

  Priority = "#PRIORITY#"
  PriorityA = "#PRIORITYA#"
  PriorityB = "#PRIORITYB#"

from page import Page
from point import Point

class PriorityProgram(object):

  """ Main execution of the priority program """
  MaximumNumber = 5
  MinimumNumber = 1
  EXIT = 'exit'

  def __init__(self, consoleIO):
    self.priorities = []
    self.cio = consoleIO

  def welcome(self):
    self.cio.write(Message.Welcome)

  def loadTasks(self, tasks):
    if tasks is list:
      self.priorities.extend(tasks)
    else:
      self.priorities.append(tasks)

  def askForPriorityName(self):
    self._loadPrioritiesFromConsole()
    self.askForMorePriorities()

  def _loadPrioritiesFromConsole(self):
    val = 'continue'
    while self.hasExited(val) != True:
      self.cio.write(Message.EnterPriorityName)
      val = self.cio.read(exitCode=self.EXIT)
      if self.isExitCode(val) != True:
        self.priorities.append(Task(val))

  def askForMorePriorities(self):
    self.cio.write(Message.AskForMore)
    val = self.cio.read(exitCode=self.EXIT)
    if val in ['y\n', 'yes\n', 'y', 'yes']:
      self.askForPriorityName()
    elif val in ['n\n', 'no\n', 'n', 'no']:
      return None
    else: 
      self.askForMorePriorities()

  def askForImportance(self):
    for p in self.priorities:
      validInput = False
      while validInput == False:
        val = self._getValue(Message.EnterImportance, p)
        validInput = self._validateValue(val)
        if validInput == True:
          p.importance = int(val)

  def askForUrgency(self):
    for p in self.priorities:
      validInput = False
      while validInput == False:
        val = self._getValue(Message.EnterUrgency, p)
        validInput = self._validateValue(val)
        if validInput == True:
          p.urgency = int(val)

  def _validateValue(self, val):
    valid = False
    if not val.isdigit():
      self.cio.write(Message.InvalidInput)
    elif self._isInvalidRange(val):
      self.cio.write(Message.InvalidRange)
    else:
      valid = True
    return valid
       
  def _getValue(self, message, priority):
    self.cio.write(message.replace(Replace.Priority, priority.name))
    return self.cio.read(exitCode=self.EXIT)

  def _isInvalidRange(self, num):
    return (int(num) < self.MinimumNumber or int(num) > self.MaximumNumber)

  def printEisenhowerMatrix(self, graph):
    self._setTaskUniqueID()
    self._printMatrix(graph)
    self._printKey()

  def _setTaskUniqueID(self):
    matches = self._getAllPossibleMatches()

    for p in self.priorities:
      for m in matches:
        if p.importance == m.X and p.urgency == m.Y:
          p.uid = str(m.Value)
        
  def _getAllPossibleMatches(self):
    letters = ['aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh', 'ii', \
               'jj', 'kk', 'll', 'mm', 'nn', 'oo', 'pp', 'qq', 'rr', 
               'ss', 'tt', 'uu', 'vv', 'ww', 'xx', 'yy']

    index = 0
    matches = []
    for x in range(1,6):
      for y in range(1,6):
        p = Point(x,y)
        p.Value = letters[index]
        index += 1
        matches.append(p)

    return matches

  def _printMatrix(self, graph):
    self._setGraphPoints(graph)
    graph.Draw(self.cio)

  def _setGraphPoints(self, graph):
    g = graph.GetPage()
    for p in self.priorities:
      xaxis = (int(p.urgency) * 2) - 1
      yaxis = (int(p.importance) * 2) - 1
      # print('\n', p.name, 'x:', xaxis, 'y:', yaxis)
      g[yaxis][xaxis].Value = p.uid

  def _printKey(self):
    self.cio.write('\n')
    for p in self.priorities:
      key = p.name + ': ' + p.uid + '\n'
      self.cio.write(key)
    # self.cio.write('\n')


  def askForPriorityValue(self):

    if len(self.priorities) == 1:
      self.cio.write(Message.CompareSkipped)

    startPriority = 1
    currentPriority = startPriority
    for priorityA in self.priorities:
      for i in range(startPriority, len(self.priorities)):
        priorityB = self.priorities[i]
        self._writeEnterPriority(priorityA, priorityB)
        self._incrementSelectedPriority(priorityA, priorityB)
      
        currentPriority += 1
      startPriority += 1
      currentPriority = startPriority

  def _writeEnterPriority(self, priA, priB):
    self.cio.write(Message.EnterPriorityValue.replace(Replace.PriorityA, priA.name).replace(Replace.PriorityB, priB.name))

  def _incrementSelectedPriority(self, priA, priB):
    val = self.cio.read(exitCode=self.EXIT)
    if val == 'a':
      priA.priority += 1
    elif val == 'b':
      priB.priority += 1

  def printPriorities(self):
    self.priorities.sort(key=lambda p: p.priority, reverse=True)
    self.cio.write(Message.PrintPriorities)
    for p in self.priorities:
      self.cio.write(' ' + p.name + '\t\t' + str(p.priority) + '\n')

  def isExitCode(self, val):
    return self.hasExited(val)

  def hasExited(self, val):
    exitCodes = ['done\n', 'end\n', 'x\n', \
                 'done',   'end',   'x']
    if (val in exitCodes): return True
    return False

if __name__ == "__main__":

  # create program
  cio = ConsoleIO()
  program = PriorityProgram(cio)

  # get any saved priorities and load them into program
  path = "C:\\SourceCode\\PersonalRepo\\Python\\LexLib\\testfiles\\priorities.json"
  jio = JsonIO(path)
  decoder = CustomDecoder()
  savedPriorities = jio.read(decoder.as_task)
  program.loadTasks(savedPriorities)

  # begin standard execution
  program.welcome()
  program.askForPriorityName()
  program.askForImportance()
  program.askForUrgency()
  program.printEisenhowerMatrix(Graph(5))
  program.askForPriorityValue()
  program.printPriorities()

  # remove priority - consider map() function
  # error checking / edge cases / input testing
  # calculate a final priority that's a composite
  #   algorithm of priority and urgency/importance
  # save priorities to file
  # decide whether to re-prioritize the imported tasks
