import fileinput

# state = states[0]
# states = set(states)

def getCodeBuffer(code):
   code = []
   buffer = ""
   for line in fileinput.input():
      if line != '':
         tmp = str(repr(line))
         tmp = tmp[1:len(tmp)-1]
         tmp = tmp.replace(" ", "\_")
         # tmp = tmp.replace("\\", "\\\\")
         code.append(tmp)
         buffer = ''.join(code)
   return buffer


def getUniformTable(codeBuffer, states, beginState, rules):
   uniformTable = []

   l,r = 0, 0
   currentState = beginState
   currentExpressions = []
