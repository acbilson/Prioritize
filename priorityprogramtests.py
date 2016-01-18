import unittest
from prioritize import *

class TestPriorityProgram(unittest.TestCase):

  """ Testing the priority program """

  def setUp(self):
    self.tio = FakeIO()

  def tearDown(self):
    self.tio = None

  def test_priorityprogram_welcome(self):
    program = PriorityProgram(self.tio)
    program.welcome()
    message = self.tio.writeContent
    self.assertEqual(Message.Welcome, message[0])

  def test_priorityprogram_loadpriorities(self):
    program = PriorityProgram(self.tio)
    tasks = [Task('Test1'), Task('Test2'), Task('Test3')]
    program.loadTasks(tasks)
    self.assertTrue(program.priorities != [])

  def test_priorityprogram_isexitcode_exits(self):
    program = PriorityProgram(self.tio)
    hasExited = program.isExitCode('done\n')
    self.assertTrue(hasExited)
 
  def test_priorityprogram_isexitcode_doesnotexit(self):
    program = PriorityProgram(self.tio)
    hasExited = program.isExitCode('continue')
    self.assertFalse(hasExited)
   
  def test_priorityprogram_askforpriorityname_exits(self):
    # arrange
    program = PriorityProgram(self.tio)
    self.tio.callStack = [StackItem(1, Message.EnterPriorityName, 'done\n'),
                          StackItem(2, Message.AskForMore, 'no\n')]
    # act
    program.askForPriorityName()
    #assert
    self.assertEqual(2, self.tio.writeCount)
    self.assertEqual(2, self.tio.readCount)
    self.assertTrue(self.tio.callStack == [])

  def test_priorityprogram_askforpriorityname_oneentry(self):
    # arrange
    program = PriorityProgram(self.tio)
    self.tio.callStack = [StackItem(1, Message.EnterPriorityName, 'TestPriority\n'), \
                          StackItem(2, Message.EnterPriorityName, 'done\n'), \
                          StackItem(3, Message.AskForMore, 'no\n')]
    # act
    program.askForPriorityName()
    # assert
    self.assertEqual('TestPriority\n',program.priorities[0].name)
    self.assertTrue(self.tio.callStack == [])

  def test_priorityprogram_askforimportance_exits(self):
    # arrange
    program = PriorityProgram(self.tio)
    program.priorities.append(Task('TestPriority'))
    self.tio.callStack = [StackItem(1, Message.EnterImportance.replace(Replace.Priority, 'TestPriority'), '3')]
    # act
    program.askForImportance()
    # assert
    self.assertEqual(3, program.priorities[0].importance)

  def test_priorityprogram_askforimportance_outofrange_repeatsquestion(self):
    # arrange
    program = PriorityProgram(self.tio)
    program.priorities.append(Task('TestPriority'))
    self.tio.callStack = [StackItem(1, Message.EnterImportance.replace(Replace.Priority, 'TestPriority'), '6'),
                          StackItem(2, Message.EnterImportance.replace(Replace.Priority, 'TestPriority'), '2')]
    # act
    program.askForImportance()
    # assert
    self.assertTrue(Message.InvalidRange in self.tio.writeContent)
    self.assertEqual(2, program.priorities[0].importance)

  def test_priorityprogram_askforimportance_none_repeatsquestion(self):
    # arrange
    program = PriorityProgram(self.tio)
    program.priorities.append(Task('TestPriority'))
    self.tio.callStack = [StackItem(1, Message.EnterImportance.replace(Replace.Priority, 'TestPriority'), ''),
                          StackItem(2, Message.EnterImportance.replace(Replace.Priority, 'TestPriority'), '2')]
    # act
    program.askForImportance()
    # assert
    self.assertTrue(Message.InvalidInput in self.tio.writeContent)
    self.assertEqual(2, program.priorities[0].importance)

  def test_priorityprogram_askforurgency_exits(self):
    # arrange
    program = PriorityProgram(self.tio)
    program.priorities.append(Task('TestPriority'))
    self.tio.callStack = [StackItem(1, Message.EnterUrgency.replace(Replace.Priority, 'TestPriority'), '5')]
    # act
    program.askForUrgency()
    # assert
    self.assertEqual(5, program.priorities[0].urgency)

  def test_priorityprogram_askforurgency_outofrange_repeatsquestion(self):
    # arrange
    program = PriorityProgram(self.tio)
    program.priorities.append(Task('TestPriority'))
    self.tio.callStack = [StackItem(1, Message.EnterUrgency.replace(Replace.Priority, 'TestPriority'), '6'),
                          StackItem(2, Message.EnterUrgency.replace(Replace.Priority, 'TestPriority'), '2')]
    # act
    program.askForUrgency()
    # assert
    self.assertTrue(Message.InvalidRange in self.tio.writeContent)
    self.assertEqual(2, program.priorities[0].urgency)

  def test_priorityprogram_askforurgency_multiple_iterate(self):
    # arrange
    program = PriorityProgram(self.tio)
    program.priorities.extend([Task('First'),Task('Second'),Task('Third')])
    self.tio.callStack = [StackItem(1, Message.EnterUrgency.replace(Replace.Priority, 'First'), '2'),
                          StackItem(2, Message.EnterUrgency.replace(Replace.Priority, 'Second'), '3'),
                          StackItem(3, Message.EnterUrgency.replace(Replace.Priority, 'Third'), '4')]
    # act
    program.askForUrgency()
    # assert
    self.assertEqual(2, program.priorities[0].urgency)
    self.assertEqual(3, program.priorities[1].urgency)
    self.assertEqual(4, program.priorities[2].urgency)

  def test_priorityprogram_printeisenhowermatrix(self):
    # arrange
    g = Graph(5)
    program = PriorityProgram(self.tio)
    program.priorities.append(Task('Eating', 5, 3, 2))
    program.priorities.append(Task('Sleeping', 3, 2, 4))
    program.priorities.append(Task('Working', 4, 5, 1))
    # act
    program.printEisenhowerMatrix(g)
    # assert
    drawnGraph = ''.join(self.tio.writeContent)
    expectedGraph = ('                      \n'
                     '05                    \n'
                     '                      \n'
                     '04    qq              \n'
                     '                      \n'
                     '03                    \n'
                     '                      \n'
                     '02        hh          \n'
                     '                      \n'
                     '01                ee  \n'
                     '  01  02  03  04  05  \n'
                     '\n'
                     'Eating: hh\n'
                     'Sleeping: qq\n'
                     'Working: ee\n')

    # print(expectedGraph)
    # print(drawnGraph)
    self.assertEqual(expectedGraph, drawnGraph)

  def test_priorityprogram_askforpriorityvalue_onlyone_skip(self):
    # arrange
    program = PriorityProgram(self.tio)
    program.priorities.append(Task('TestPriority', 0, 2, 1))
    # act
    program.askForPriorityValue()
    # assert
    self.assertEqual(Message.CompareSkipped, self.tio.lastWrite)

  def test_priorityprogram_askforpriorityvalue(self):
    # arrange
    program = PriorityProgram(self.tio)
    # begins with no priorities set
    tasks = [Task('Sleeping', 0,2,1),Task('Eating', 0,2,1),Task('Working', 0,2,1)]
    program.priorities.extend(tasks)

    # the messages of each iteration over every priority
    messages = [Message.EnterPriorityValue
                .replace(Replace.PriorityA, 'Sleeping')
                .replace(Replace.PriorityB, 'Eating'),
                Message.EnterPriorityValue
                .replace(Replace.PriorityA, 'Sleeping')
                .replace(Replace.PriorityB, 'Working'),
                Message.EnterPriorityValue
                .replace(Replace.PriorityA, 'Eating')
                .replace(Replace.PriorityB, 'Working')]

    # setting the call stack, with the returned selection
    self.tio.callStack = [StackItem(1, messages[0], 'a'),
                          StackItem(2, messages[1], 'a'),
                          StackItem(3, messages[2], 'b')]
    # act
    program.askForPriorityValue()
    # assert
    # should have selected the first (sleeping) twice, 
    # the second (eating) none, and the third (working) once
    sleepingPriority = next(p for p in program.priorities if p.name == 'Sleeping').priority
    eatingPriority = next(p for p in program.priorities if p.name == 'Eating').priority
    workingPriority = next(p for p in program.priorities if p.name == 'Working').priority
    self.assertEqual(2, sleepingPriority)
    self.assertEqual(0, eatingPriority)
    self.assertEqual(1, workingPriority)

  def test_priorityprogram_printpriorities_inorder(self):
    # arrange
    program = PriorityProgram(self.tio)
    tasks = [Task('Sleeping', 3,2,1),Task('Eating', 1,2,1),Task('Working', 4,2,1)]
    program.priorities.extend(tasks)
    # act
    program.printPriorities()
    # assert
    expected = Message.PrintPriorities + ' Working\t\t4\n Sleeping\t\t3\n Eating\t\t1\n'
    actual = ''.join(self.tio.writeContent)
    self.assertEqual(expected, actual)
