from collections import defaultdict as dd

__DEBUG__ = False

def __splitExpressionOR(expression):
   '''
   Finds all "OR" parts in expression\n
   IN:
      expression : String
   OUT:
      parts : List
   '''

   parts = []
   begin = 0
   count = 0
   pos = 0
   while pos < len(expression):
      char = expression[pos]

      if char == "\\":
         pos += 1
      elif char == "(":
         count += 1
      elif char == ")":
         count -= 1
      elif char == '|' and not count:
         parts.append(expression[begin:pos])
         begin = pos+1
      
      pos += 1
   parts.append(expression[begin:])
   return parts
   
def __splitExpressionAND(expression):
   '''
   Finds all "AND" parts in expression\n
   IN:
      expression : String
   OUT:
      parts : List
   '''

   pos = 0
   left = 0
   count = 0
   parts = []

   while pos < len(expression):
      char = expression[pos]

      if char == "(":
         count += 1
         if count == 1:
            left = pos
      elif char == ")":
         count -= 1
         if not count:
            parts.append(expression[left:pos+1])
      elif count > 0:
         pass
      elif char == "\\":
         parts.append(expression[pos:pos+2])
         pos += 1
      else:
         parts.append(char)
      
      pos += 1
   
   return parts
 
def make_eNKA(expression, depth = 0):
   partsOR = __splitExpressionOR(expression)

   if __DEBUG__:
      print("    "*depth,"Making:",expression)

   start = dd(list)
   end = dd(list)

   if len(partsOR) > 1:
      for partOR in partsOR:
         subStart, subEnd = make_eNKA(partOR, depth+1)
         start["$"].append(subStart)
         subEnd["$"].append(end)
   else:
      partsAND = __splitExpressionAND(expression)
      partsCache = [(None, start, False)]
      
      for i,partAND in enumerate(partsAND):
         subStart, subEnd = dd(list), dd(list)
         #SUBPART
         if partAND[0] == "(":
            subStart, subEnd = make_eNKA(partAND[1:len(partAND)-1], depth+1)
            partsCache[-1][1]["$"].append(subStart)
            partsCache.append([subStart, subEnd, False])
         
         #REPETITION
         elif partAND == "*":
            partsCache[-1][1]["$"].append(partsCache[-1][0])
            partsCache[-1][2] = True

         #CHARACTER
         else:
            subStart[partAND].append(subEnd)
            partsCache[-1][1]["$"].append(subStart)
            partsCache.append([subStart, subEnd, False])

      partsCache[-1][1]["$"].append(end)
      partsCache.append((end, None, False))

      #TODO: Star for zero repetitions
      for i in range(len(partsCache)-1):
         partCache = partsCache[i]
         if partCache[2]:
            toConnect = i+1
            j = i
            while j >= 0:
               j -= 1
               partsCache[j][1]["$"].append(partsCache[toConnect][0])
               if partsCache[j][2] == False:
                  break
      
   if __DEBUG__:      
      print("    "*depth,"Starts:",list(start.keys()))

   return start, end

def advance_eNKA(currentStates, character):
   nextStates = []
   visitedStates = set()
   DFS = []

   for currentState in currentStates:
      for nextState in currentState[character]:
         if not id(nextState) in visitedStates:
            visitedStates.add(id(nextState))
            nextStates.append(nextState)
            DFS.append(nextState)
   
   while DFS:
      state = DFS.pop()
      for eState in state["$"]:
         if not id(eState) in visitedStates:
            visitedStates.add(id(eState))
            nextStates.append(eState)
            DFS.append(eState)
   
   return nextStates

def get_e(states):
   e = states
   DFS = []
   visited = set()

   for s in states:
      visited.add(id(s))
      DFS.append(s)

   while DFS:
      curr = DFS.pop()
      for nextState in curr["$"]:
         if not id(nextState) in visited:
            visited.add(id(nextState))
            DFS.append(nextState)
            e.append(nextState)
   
   return e

def test_eNKA(machine, text):
   currentStates = [machine[0]]

   currentStates = get_e(currentStates)

   for t in text:
      currentStates = advance_eNKA(currentStates, t)
      if not currentStates:
         return False

   for currentState in currentStates:
      if id(currentState) == id(machine[1]):
         return True
   
   return False
