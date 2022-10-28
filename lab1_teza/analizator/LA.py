states = ['S_poc', 'S_preskoci']
uniforms = {'A': 0}
rules = {'S_poc': {'a': ['A', 'UDJI_U_STANJE S_preskoci'], '\\n': ['-', 'NOVI_REDAK']}, 'S_preskoci': {'a': ['-', 'UDJI_U_STANJE S_poc'], '\\n': ['-', 'NOVI_REDAK']}}
rulePriorities = {('S_poc', 'a'): 0, ('S_poc', '\\n'): -1, ('S_preskoci', 'a'): -2, ('S_preskoci', '\\n'): -3}

import fileinput

import Machine


def getCodeBuffer():
   buffer = ""
   code = []
   for line in fileinput.input():
      if line != '':
         code.append(line)

   return ''.join(code)

def getMachinesFromRules():
   expressionToMachine = {}
   for state,transitions in rules.items():
      for expression, args in transitions.items():
         expressionToMachine[expression] = Machine.make_eNKA(expression)
   return expressionToMachine

def __getCurrentMachines(state, expressionToMachine):
   currentMachines = {}

   for expression in rules[state]:
      currentMachines[(expression, id(expressionToMachine[expression][1]))] = Machine.getEpsilonEnv([expressionToMachine[expression][0]])

   return currentMachines

def __getPriorityExpression(expressions, state):
   biggestPriority = -1000000000
   priorityExpression = ""
   for expression in expressions:
      tmp = rulePriorities[(state, expression)]
      if tmp > biggestPriority:
         biggestPriority = tmp
         priorityExpression = expression
   return priorityExpression

def analyze(codeBuffer, beginState, expressionToMachine):
   uniformTable = []

   l,row = 0,1
   currentState = beginState

   while l < len(codeBuffer):
      #(expression, id(validState)) => [currentStates...]
      currentMachines = __getCurrentMachines(currentState, expressionToMachine)
      previousMachines = None
      previousMachinesPOS = 0
      pos = l
      args = []

      #Next piece
      while len(currentMachines) > 0 and pos < len(codeBuffer):
         nextMachines = {}
         previousTmp = []

         for machine,currentStates in currentMachines.items():
            nextStates, valid = Machine.step_eNKA(currentStates, codeBuffer[pos], machine[1])
            if valid:
               previousTmp.append(machine[0])
            if len(nextStates) > 0:
               nextMachines[machine] = nextStates
         
         if len(nextMachines) == 0:
            if previousMachines != None:
               priorityExpression = __getPriorityExpression(previousMachines, currentState)
               args = rules[currentState][priorityExpression]
               pos = previousMachinesPOS
               break
            else:
               pos = l + 1
               break          

         else:
            currentMachines = nextMachines
            if len(previousTmp) > 0:
               previousMachines = previousTmp
               previousMachinesPOS = pos + 1

         pos += 1

      if len(args) > 0:
         for i in range(len(args)):
            if "VRATI_SE" in args[i]:
               pos = l + int(args[i].split(" ")[1])


         for i in range(len(args)):
            if args[i] in uniforms:
               word = codeBuffer[l:pos]
               uniformTable.append([args[i], row, word])
            elif "UDJI_U_STANJE" in args[i]:
               currentState = args[i].split(" ")[1]
            elif "NOVI_REDAK" in args[i]:
               row += 1
      l = pos
   
   return uniformTable


expressionToMachine = getMachinesFromRules()
codeBuffer = getCodeBuffer()

uniformTable = analyze(codeBuffer, states[0], expressionToMachine)
for uniform in uniformTable:
	print(uniform[0],uniform[1],uniform[2])
   