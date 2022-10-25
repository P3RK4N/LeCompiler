states = ['S_pocetno', 'S_komentar', 'S_jednolinijskiKomentar', 'S_string']
uniforms = {'IDN': 0, 'BROJ': 1, 'ZNAK': 2, 'NIZ_ZNAKOVA': 3, 'KR_BREAK': 4, 'KR_CHAR': 5, 'KR_CONST': 6, 'KR_CONTINUE': 7, 'KR_ELSE': 8, 'KR_FLOAT': 9, 'KR_FOR': 10, 'KR_IF': 11, 'KR_INT': 12, 'KR_RETURN': 13, 'KR_STRUCT': 14, 'KR_VOID': 15, 'KR_WHILE': 16, 'PLUS': 17, 'OP_INC': 18, 'MINUS': 19, 'OP_DEC': 20, 'ASTERISK': 21, 'OP_DIJELI': 22, 'OP_MOD': 23, 'OP_PRIDRUZI': 24, 'OP_LT': 25, 'OP_LTE': 26, 'OP_GT': 27, 'OP_GTE': 28, 'OP_EQ': 29, 'OP_NEQ': 30, 'OP_NEG': 31, 'OP_TILDA': 32, 'OP_I': 33, 'OP_ILI': 34, 'AMPERSAND': 35, 'OP_BIN_ILI': 36, 'OP_BIN_XILI': 37, 'ZAREZ': 38, 'TOCKAZAREZ': 39, 'TOCKA': 40, 'L_ZAGRADA': 41, 'D_ZAGRADA': 42, 'L_UGL_ZAGRADA': 43, 'D_UGL_ZAGRADA': 44, 'L_VIT_ZAGRADA': 45, 'D_VIT_ZAGRADA': 46}
rules = {'S_pocetno': {'\\t|\\_': ['-'], '\\n': ['-', 'NOVI_REDAK'], '//': ['-', 'UDJI_U_STANJE S_jednolinijskiKomentar'], '/\\*': ['-', 'UDJI_U_STANJE S_komentar'], '"': ['-', 'UDJI_U_STANJE S_string', 'VRATI_SE 0'], 'break': ['KR_BREAK'], 'char': ['KR_CHAR'], 'const': ['KR_CONST'], 'continue': ['KR_CONTINUE'], 'else': ['KR_ELSE'], 'float': ['KR_FLOAT'], 'for': ['KR_FOR'], 'if': ['KR_IF'], 'int': ['KR_INT'], 'return': ['KR_RETURN'], 'struct': ['KR_STRUCT'], 'void': ['KR_VOID'], 'while': ['KR_WHILE'], '(_|(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z))(_|(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)|(0|1|2|3|4|5|6|7|8|9))*': ['IDN'], '(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*': ['BROJ'], '0(X|x)((0|1|2|3|4|5|6|7|8|9)|a|b|c|d|e|f|A|B|C|D|E|F)((0|1|2|3|4|5|6|7|8|9)|a|b|c|d|e|f|A|B|C|D|E|F)*': ['BROJ'], '(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*.(0|1|2|3|4|5|6|7|8|9)*($|((e|E)($|+|-)(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*))': ['BROJ'], '(0|1|2|3|4|5|6|7|8|9)*.(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*($|((e|E)($|+|-)(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*))': ['BROJ'], '\'(\\(|\\)|\\{|\\}|\\||\\*|\\\\|\\$|\\_|!|"|#|%|&|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|~)\'': ['ZNAK'], '\'\\\\(\\(|\\)|\\{|\\}|\\||\\*|\\\\|\\$|\\_|!|"|#|%|&|\'|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|~)\'': ['ZNAK'], '++': ['OP_INC'], '--': ['OP_DEC'], '+': ['PLUS'], '-': ['MINUS'], '\\*': ['ASTERISK'], '/': ['OP_DIJELI'], '%': ['OP_MOD'], '=': ['OP_PRIDRUZI'], '<': ['OP_LT'], '<=': ['OP_LTE'], '>': ['OP_GT'], '>=': ['OP_GTE'], '==': ['OP_EQ'], '!=': ['OP_NEQ'], '!': ['OP_NEG'], '~': ['OP_TILDA'], '&&': ['OP_I'], '\\|\\|': ['OP_ILI'], '&': ['AMPERSAND'], '\\|': ['OP_BIN_ILI'], '^': ['OP_BIN_XILI'], ',': ['ZAREZ'], ';': ['TOCKAZAREZ'], '.': ['TOCKA'], '\\(': ['L_ZAGRADA'], '\\)': ['D_ZAGRADA'], '\\{': ['L_VIT_ZAGRADA'], '\\}': ['D_VIT_ZAGRADA'], '[': ['L_UGL_ZAGRADA'], ']': ['D_UGL_ZAGRADA']}, 'S_jednolinijskiKomentar': {'\\n': ['-', 'NOVI_REDAK', 'UDJI_U_STANJE S_pocetno'], '(\\(|\\)|\\{|\\}|\\||\\*|\\\\|\\$|\\t|\\n|\\_|!|"|#|%|&|\'|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|~)': ['-']}, 'S_komentar': {'\\*/': ['-', 'UDJI_U_STANJE S_pocetno'], '\\n': ['-', 'NOVI_REDAK'], '(\\(|\\)|\\{|\\}|\\||\\*|\\\\|\\$|\\t|\\n|\\_|!|"|#|%|&|\'|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|~)': ['-']}, 'S_string': {'"((\\(|\\)|\\{|\\}|\\||\\*|\\\\|\\$|\\t|\\_|!|#|%|&|\'|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|~)|\\\\")*"': ['NIZ_ZNAKOVA', 'UDJI_U_STANJE S_pocetno']}}
rulePriorities = {('S_pocetno', '\\t|\\_'): 0, ('S_pocetno', '\\n'): -1, ('S_pocetno', '//'): -2, ('S_jednolinijskiKomentar', '\\n'): -3, ('S_jednolinijskiKomentar', '(\\(|\\)|\\{|\\}|\\||\\*|\\\\|\\$|\\t|\\n|\\_|!|"|#|%|&|\'|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|~)'): -4, ('S_pocetno', '/\\*'): -5, ('S_komentar', '\\*/'): -6, ('S_komentar', '\\n'): -7, ('S_komentar', '(\\(|\\)|\\{|\\}|\\||\\*|\\\\|\\$|\\t|\\n|\\_|!|"|#|%|&|\'|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|~)'): -8, ('S_pocetno', '"'): -9, ('S_string', '"((\\(|\\)|\\{|\\}|\\||\\*|\\\\|\\$|\\t|\\_|!|#|%|&|\'|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|~)|\\\\")*"'): -10, ('S_pocetno', 'break'): -11, ('S_pocetno', 'char'): -12, ('S_pocetno', 'const'): -13, ('S_pocetno', 'continue'): -14, ('S_pocetno', 'else'): -15, ('S_pocetno', 'float'): -16, ('S_pocetno', 'for'): -17, ('S_pocetno', 'if'): -18, ('S_pocetno', 'int'): -19, ('S_pocetno', 'return'): -20, ('S_pocetno', 'struct'): -21, ('S_pocetno', 'void'): -22, ('S_pocetno', 'while'): -23, ('S_pocetno', '(_|(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z))(_|(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)|(0|1|2|3|4|5|6|7|8|9))*'): -24, ('S_pocetno', '(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*'): -25, ('S_pocetno', '0(X|x)((0|1|2|3|4|5|6|7|8|9)|a|b|c|d|e|f|A|B|C|D|E|F)((0|1|2|3|4|5|6|7|8|9)|a|b|c|d|e|f|A|B|C|D|E|F)*'): -26, ('S_pocetno', '(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*.(0|1|2|3|4|5|6|7|8|9)*($|((e|E)($|+|-)(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*))'): -27, ('S_pocetno', '(0|1|2|3|4|5|6|7|8|9)*.(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*($|((e|E)($|+|-)(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*))'): -28, ('S_pocetno', '\'(\\(|\\)|\\{|\\}|\\||\\*|\\\\|\\$|\\_|!|"|#|%|&|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|~)\''): -29, ('S_pocetno', '\'\\\\(\\(|\\)|\\{|\\}|\\||\\*|\\\\|\\$|\\_|!|"|#|%|&|\'|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|~)\''): -30, ('S_pocetno', '++'): -31, ('S_pocetno', '--'): -32, ('S_pocetno', '+'): -33, ('S_pocetno', '-'): -34, ('S_pocetno', '\\*'): -35, ('S_pocetno', '/'): -36, ('S_pocetno', '%'): -37, ('S_pocetno', '='): -38, ('S_pocetno', '<'): -39, ('S_pocetno', '<='): -40, ('S_pocetno', '>'): -41, ('S_pocetno', '>='): -42, ('S_pocetno', '=='): -43, ('S_pocetno', '!='): -44, ('S_pocetno', '!'): -45, ('S_pocetno', '~'): -46, ('S_pocetno', '&&'): -47, ('S_pocetno', '\\|\\|'): -48, ('S_pocetno', '&'): -49, ('S_pocetno', '\\|'): -50, ('S_pocetno', '^'): -51, ('S_pocetno', ','): -52, ('S_pocetno', ';'): -53, ('S_pocetno', '.'): -54, ('S_pocetno', '\\('): -55, ('S_pocetno', '\\)'): -56, ('S_pocetno', '\\{'): -57, ('S_pocetno', '\\}'): -58, ('S_pocetno', '['): -59, ('S_pocetno', ']'): -60}

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
   
codeBuffer = getCodeBuffer()
expressionToMachine = getMachinesFromRules()
uniformTable = analyze(codeBuffer, states[0], expressionToMachine)
for uniform in uniformTable:
	print(uniform[0],uniform[1],uniform[2])
