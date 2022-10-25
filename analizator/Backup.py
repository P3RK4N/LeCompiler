import fileinput
import Machine

def __getCodeBuffer():
   buffer = ""
   code = []
   for line in fileinput.input():
      if line != '':
         tmp = str(repr(line))
         tmp = tmp[1:len(tmp)-1]
         tmp = tmp.replace(" ", "\_")
         # tmp = tmp.replace("\\", "\\\\")
         code.append(tmp)
         buffer = ''.join(code)
   return buffer

def __getMachinesFromRules():
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

def __analyze(codeBuffer, beginState, expressionToMachine):
   uniformTable = []

   l,r,row = 0,0,1
   currentState = beginState

   while l < len(codeBuffer):
      #(expression, id(validState)) => [currentStates...]
      currentMachines = __getCurrentMachines(currentState, expressionToMachine)
      previousMachines = None
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
               break               

         else:
            currentMachines = nextMachines
            if len(previousTmp) > 0:
               previousMachines = previousTmp

         pos += 1

      lChanged = False

      if len(args) > 0:
         for i in range(len(args)):
            if not i and args[i] in uniforms:
               uniformTable.append([args[i], row, codeBuffer[l:pos-int(previousMachines==None and pos-l > 1)]])
            elif "UDJI_U_STANJE" in args[i]:
               currentState = args[i].split(" ")[1]
            elif "VRATI_SE" in args[i]:
               lChanged = True
               l += int(args[i].split(" ")[1])
            elif "NOVI_REDAK" in args[i]:
               row += 1
      
      if not lChanged:
         l = pos
   
   return uniformTable

codeBuffer = __getCodeBuffer()
expressionToMachine = __getMachinesFromRules()

uniformTable = __analyze(codeBuffer, states[0], expressionToMachine)

for uniform in uniformTable:
   print(uniform[0],uniform[1],uniform[2])