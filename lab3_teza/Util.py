PARENT = "PARENT" #Parent Node
KIDS = "KIDS"     #Kid Nodes
SCOPE = "SCOPE"   #Declared vars or functions
TYPE = "TYPE"     #Type of scope identity
NAME = "NAME"     #Name of scope identity (Redundant)
CURRENT_FUNC = "CURRENT_FUNC"     #Current function
FUNCS = "FUNCS"   #Functions defined in this scope
DECL = "DECL"     #Declared, but undefined identities in this scope
LVAL = "LVAL"     #Is identity an lvalue?

INT = "INT"
CONST_INT = "CONST INT"
CONST_INT_ARRAY = "CONST INT ARRAY"
INT_ARRAY = "INT ARRAY"

CHAR = "CHAR"
CHAR_ARRAY = "CHAR ARRAY"
CONST_CHAR = "CONST CHAR"
CONST_CHAR_ARRAY = "CONST CHAR ARRAY"

VOID = "VOID"
ARRAY = "ARRAY"
CONST = "CONST"

def functionExists(funcName, globalNode):
   while globalNode[PARENT]:
        globalNode = globalNode[PARENT]

   toVisit = [globalNode]

   while toVisit:
       currentNode = toVisit.pop()
       toVisit.extend(currentNode[KIDS])
       if funcName in currentNode[FUNCS]:
           return True

   return False

def allDeclared(currentNode):
   while currentNode[PARENT]:
      currentNode = currentNode[PARENT]

   toVisit = [currentNode]

   while toVisit:
       node = toVisit.pop()
       toVisit.extend(node[KIDS])
       if len(node[DECL]) > 0:
           return False

   return True

def getFuncType(funcName, currentNode):
   while currentNode != None:
      if funcName in currentNode[FUNCS]:
         return currentNode[FUNCS][funcName]
      
def getDeclaredType(currentNode, name):
   while currentNode != None:
      if name in currentNode[SCOPE]:
         return currentNode[SCOPE][TYPE], not CONST in currentNode[SCOPE][TYPE]
      
      elif name in currentNode[DECL]:
         return currentNode[DECL][name]
      
      elif name in currentNode[FUNCS]:
         return currentNode[FUNCS][name], False

      currentNode = currentNode[PARENT]
   
   return None, None

def findOtherBracket(tree, l, r):
   count = 1
   current = None
   while tree and count > 0:
      current = tree.popleft()
      if l in current:
         count += 1
      elif r in current:
         count -= 1
   return stringify(current)

def stringify(s):
   kros,line,name = s.split(" ")
   return " " + kros + "(" + line + "," + name + ")"

def stringify1(kros, line, name):
   return " " + kros + "(" + line + "," + name + ")"