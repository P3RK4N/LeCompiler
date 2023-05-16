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
       for name in node[DECL]:
         if "|" in node[DECL][name]:
            return False

   return True

def getFuncType(funcName, currentNode):
   while currentNode != None:
      if funcName in currentNode[FUNCS]:
         return currentNode[FUNCS][funcName]
      
def getDeclaredType(currentNode, name):
   while currentNode != None:
      if name in currentNode[SCOPE]:
         return currentNode[SCOPE][name][TYPE], not CONST in currentNode[SCOPE][name][TYPE]
      
      elif name in currentNode[DECL]:
         return currentNode[DECL][name], not "|" in currentNode[DECL][name] and not CONST in currentNode[DECL][name]
      
      elif name in currentNode[FUNCS]:
         return currentNode[FUNCS][name], False

      currentNode = currentNode[PARENT]
   
   return None, None

def findOtherBracket(tree, l, r):
   count = 1
   current = None
   while tree and count > 0:
      current = tree.popleft()[0]
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

def stringify_no_space(s):
   kros,line,name = s.split(" ")
   return kros + "(" + line + "," + name + ")"

def isValidString(s):
   if s[0] != "\"" or s[-1] != "\"":
         return False
   else:   
      for pos in range(1,len(s)-1):
         if s[pos] == "\\" and (pos == len(s)-2 or not s[pos+1] in {'\\', "t", "n", "\"", "\'", "0"}):
            return False
   
   return True

def isValidChar(c):
   if len(c) == 2:
      if c[0] != "\\" or not c[1] in {'\\', "t", "n", "\"", "\'", "0"}:
         return False
   else:
      if c[0] in {'\\', '\''}:
         return False
   
   return True

#0 -> string
#1 -> depth
def getProduction(genTree):
   if not genTree:
      return ""
   
   production = []

   production.append(genTree[0][0])
   production.append("::=")

   depth = genTree[1][1]
   pos = 1

   while pos < len(genTree) and genTree[pos][1] >= depth:
      if depth == genTree[pos][1]:
         s = genTree[pos][0]

         if s[0] == "<" and s[-1] == ">":
            production.append(s)
         else:
            production.append(stringify_no_space(s))
            
      pos += 1

   production = ' '.join(production)

   return production