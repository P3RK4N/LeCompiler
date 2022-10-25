#izvorni program
#tablica uniformnih znakova
#tablica znakova
   #tablica identifikatora
   #tablica konstanti
   #tablica kljucnih rijeci, operatora i specijalnih znakova

import fileinput

import Parser


def __printDefines():
   for key,define in defines.items():
      print(key, define)
   print()

def __printExpressions(rules): 
   for rule,value in rules.items():
      for expression,args in value.items():
         print(expression)
   print()

def __main__():
   data = []

   for line in fileinput.input():
      tmp = str(line.rstrip("\n"))
      # tmp = tmp[1:len(tmp)-1]
      # tmp = tmp.replace("\\", "\\\\")

      data.append(tmp)


   states, uniforms, rules, rulePriorities = Parser.parseData(data)
   
   # __printExpressions(rules)

   LA = open("analizator\\LA.py", "w")

   LA.write("states = " + str(states) + "\n")
   LA.write("uniforms = " + str(uniforms) + "\n")
   LA.write("rules = " + str(rules) + "\n")
   LA.write("rulePriorities = " + str(rulePriorities) + "\n")
   
   LA.write(
   r"""
import fileinput

import Machine


def getCodeBuffer(prefixes):
   buffer = ""
   code = []
   for line in fileinput.input():
      if line != '':
         tmp = repr(line)
         tmp = tmp[1:len(tmp)-1]
         code.append(tmp)

   buffer = ''.join(code)

   prefixes.discard("n")
   prefixes.discard("t")
   print(prefixes)

   codeBuffer = []
   i = 0
   while i < len(buffer):
      codeBuffer.append(buffer[i])
      if codeBuffer[-1] == '\\':
         i += 1
         codeBuffer[-1] += buffer[i]
      elif codeBuffer[-1] in prefixes:
         codeBuffer[-1] = "\\" + codeBuffer[-1]
      i += 1

   return codeBuffer

def getMachinesFromRules(prefixed = None):
   expressionToMachine = {}
   for state,transitions in rules.items():
      for expression, args in transitions.items():
         expressionToMachine[expression] = Machine.make_eNKA(expression, prefixed)
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
               uniformTable.append([args[i], row, codeBuffer[l:pos-int(previousMachines==None and pos-l > 1 and pos == len(codeBuffer))]]) #TODO : Fix
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


prefixed = set()
expressionToMachine = getMachinesFromRules(prefixed)
codeBuffer = getCodeBuffer(prefixed)

print(codeBuffer)

uniformTable = analyze(codeBuffer, states[0], expressionToMachine)
for uniform in uniformTable:
	print(uniform[0],uniform[1],''.join(uniform[2]))
   """
   )
   LA.write("\n")
   LA.write("codeBuffer = getCodeBuffer()\n")
   LA.write("expressionToMachine = getMachinesFromRules()\n")
   LA.write("uniformTable = analyze(codeBuffer, states[0], expressionToMachine)\n")
   LA.write("for uniform in uniformTable:\n")
   LA.write("\tprint(uniform[0],uniform[1],uniform[2])\n")
   
   LA.close()


if __name__ == "__main__":
   __main__()