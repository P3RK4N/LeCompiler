states = ['S_pocetno', 'S_komentar', 'S_jednolinijskiKomentar', 'S_string']
uniforms = {'IDN': 0, 'BROJ': 1, 'ZNAK': 2, 'NIZ_ZNAKOVA': 3, 'KR_BREAK': 4, 'KR_CHAR': 5, 'KR_CONST': 6, 'KR_CONTINUE': 7, 'KR_ELSE': 8, 'KR_FLOAT': 9, 'KR_FOR': 10, 'KR_IF': 11, 'KR_INT': 12, 'KR_RETURN': 13, 'KR_STRUCT': 14, 'KR_VOID': 15, 'KR_WHILE': 16, 'PLUS': 17, 'OP_INC': 18, 'MINUS': 19, 'OP_DEC': 20, 'ASTERISK': 21, 'OP_DIJELI': 22, 'OP_MOD': 23, 'OP_PRIDRUZI': 24, 'OP_LT': 25, 'OP_LTE': 26, 'OP_GT': 27, 'OP_GTE': 28, 'OP_EQ': 29, 'OP_NEQ': 30, 'OP_NEG': 31, 'OP_TILDA': 32, 'OP_I': 33, 'OP_ILI': 34, 'AMPERSAND': 35, 'OP_BIN_ILI': 36, 'OP_BIN_XILI': 37, 'ZAREZ': 38, 'TOCKAZAREZ': 39, 'TOCKA': 40, 'L_ZAGRADA': 41, 'D_ZAGRADA': 42, 'L_UGL_ZAGRADA': 43, 'D_UGL_ZAGRADA': 44, 'L_VIT_ZAGRADA': 45, 'D_VIT_ZAGRADA': 46}
rules = {'S_pocetno': {'\\t|\\_': ['-'], '\\n': ['-', 'NOVI_REDAK'], '//': ['-', 'UDJI_U_STANJE S_jednolinijskiKomentar'], '/\\*': ['-', 'UDJI_U_STANJE S_komentar'], '"': ['-', 'UDJI_U_STANJE S_string', 'VRATI_SE 0'], 'break': ['KR_BREAK'], 'char': ['KR_CHAR'], 'const': ['KR_CONST'], 'continue': ['KR_CONTINUE'], 'else': ['KR_ELSE'], 'float': ['KR_FLOAT'], 'for': ['KR_FOR'], 'if': ['KR_IF'], 'int': ['KR_INT'], 'return': ['KR_RETURN'], 'struct': ['KR_STRUCT'], 'void': ['KR_VOID'], 'while': ['KR_WHILE'], '(_|(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z))(_|(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)|(0|1|2|3|4|5|6|7|8|9))*': ['IDN'], '(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*': ['BROJ'], '0(X|x)((0|1|2|3|4|5|6|7|8|9)|a|b|c|d|e|f|A|B|C|D|E|F)((0|1|2|3|4|5|6|7|8|9)|a|b|c|d|e|f|A|B|C|D|E|F)*': ['BROJ'], '(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*.(0|1|2|3|4|5|6|7|8|9)*($|((e|E)($|+|-)(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*))': ['BROJ'], '(0|1|2|3|4|5|6|7|8|9)*.(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*($|((e|E)($|+|-)(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*))': ['BROJ'], '\'(\\(|\\)|\\{|\\}|\\||\\*|\\\\|\\$|\\_|!|"|#|%|&|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|~)\'': ['ZNAK'], '\'\\\\(\\(|\\)|\\{|\\}|\\||\\*|\\\\|\\$|\\_|!|"|#|%|&|\'|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|~)\'': ['ZNAK'], '++': ['OP_INC'], '--': ['OP_DEC'], '+': ['PLUS'], '-': ['MINUS'], '\\*': ['ASTERISK'], '/': ['OP_DIJELI'], '%': ['OP_MOD'], '=': ['OP_PRIDRUZI'], '<': ['OP_LT'], '<=': ['OP_LTE'], '>': ['OP_GT'], '>=': ['OP_GTE'], '==': ['OP_EQ'], '!=': ['OP_NEQ'], '!': ['OP_NEG'], '~': ['OP_TILDA'], '&&': ['OP_I'], '\\|\\|': ['OP_ILI'], '&': ['AMPERSAND'], '\\|': ['OP_BIN_ILI'], '^': ['OP_BIN_XILI'], ',': ['ZAREZ'], ';': ['TOCKAZAREZ'], '.': ['TOCKA'], '\\(': ['L_ZAGRADA'], '\\)': ['D_ZAGRADA'], '\\{': ['L_VIT_ZAGRADA'], '\\}': ['D_VIT_ZAGRADA'], '[': ['L_UGL_ZAGRADA'], ']': ['D_UGL_ZAGRADA']}, 'S_jednolinijskiKomentar': {'\\n': ['-', 'NOVI_REDAK', 'UDJI_U_STANJE S_pocetno'], '(\\(|\\)|\\{|\\}|\\||\\*|\\\\|\\$|\\t|\\n|\\_|!|"|#|%|&|\'|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|~)': ['-']}, 'S_komentar': {'\\*/': ['-', 'UDJI_U_STANJE S_pocetno'], '\\n': ['-', 'NOVI_REDAK'], '(\\(|\\)|\\{|\\}|\\||\\*|\\\\|\\$|\\t|\\n|\\_|!|"|#|%|&|\'|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|~)': ['-']}, 'S_string': {'"((\\(|\\)|\\{|\\}|\\||\\*|\\\\|\\$|\\t|\\_|!|#|%|&|\'|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|~)|\\\\")*"': ['NIZ_ZNAKOVA', 'UDJI_U_STANJE S_pocetno']}}

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