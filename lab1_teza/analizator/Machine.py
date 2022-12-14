from collections import defaultdict as dd

__DEBUG__ = False

specials = {
      "\\(" : "(" ,
      "\\)" : ")",
      "\\{" : "{",
      "\\}" : "}",
      "\\|" : "|",
      "\\*" : "*",
      "\\$" : "$",
      "\\_" : " ",
      "\\n" : "\n",
      "\\t" : "\t",
      "\\\\" : "\\"
      }

epsilon = "EPSILON"

def splitExpressionOR(expression):
   '''
   Finds all "OR" parts in expression\n
   IN:
      expression : String
   OUT:
      parts : List
   '''

   parts = set()
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
         parts.add(expression[begin:pos])
         begin = pos+1
      
      pos += 1
   parts.add(expression[begin:])
   return list(parts)
   
def splitExpressionAND(expression):
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

def __make_eNKA(expression):
   partsOR = splitExpressionOR(expression)

   start = dd(list)
   end = dd(list)

   if len(partsOR) > 1:
      for partOR in partsOR:
         subStart, subEnd = __make_eNKA(partOR)
         start[epsilon].append(subStart)
         subEnd[epsilon].append(end)

   #Sequential Expression 
   else:
      partsAND = splitExpressionAND(expression)
      #(subStart, subEnd, repeatable)
      partsCache = [[None, start, False]]

      pos = 0      
      while pos < len(partsAND):
         partAND = partsAND[pos]
         subStart, subEnd = dd(list), dd(list)
         #SUBPART
         if partAND[0] == "(":
            subStart, subEnd = __make_eNKA(partAND[1:len(partAND)-1])
            partsCache[-1][1][epsilon].append(subStart)
            partsCache.append([subStart, subEnd, False])
         
         #REPETITION
         elif partAND == "*":
            partsCache[-1][1][epsilon].append(partsCache[-1][0])
            partsCache[-1][2] = True

         #OPTIONAL
         elif partAND == "$":
            start[epsilon].append(end)

         #CHARACTER
         else:
            if __DEBUG__:
               print(partAND, partAND == "\\", len(partAND))

            if partAND == "\\":
               pos += 1
               partAND += partsAND[pos]

            subStart[partAND if partAND not in specials else specials[partAND]].append(subEnd)
            partsCache[-1][1][epsilon].append(subStart)
            partsCache.append([subStart, subEnd, False])
         
         pos += 1

      partsCache[-1][1][epsilon].append(end)
      partsCache.append([end, None, False])

      for i in range(len(partsCache)-1):
         partCache = partsCache[i]
         if partCache[2]:
            toConnect = i+1
            j = i
            while j >= 0:
               j -= 1
               partsCache[j][1][epsilon].append(partsCache[toConnect][0])
               if partsCache[j][2] == False:
                  break

   return start, end

def step_eNKA(currentStates, character, validID = None):
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
      for eState in state[epsilon]:
         if not id(eState) in visitedStates:
            visitedStates.add(id(eState))
            nextStates.append(eState)
            DFS.append(eState)
   
   valid = False
   if validID in visitedStates:
      valid = True

   return nextStates, valid

def getEpsilonEnv(states):
   e = states
   DFS = []
   visited = set()

   for s in states:
      visited.add(id(s))
      DFS.append(s)

   while DFS:
      curr = DFS.pop()
      for nextState in curr[epsilon]:
         if not id(nextState) in visited:
            visited.add(id(nextState))
            DFS.append(nextState)
            e.append(nextState)
   
   return e

def make_eNKA(expression):
   '''
   Recursively makes eNKA Machine.\n
   IN:\n
      Expression : String\n
   
   OUT:\n
      start_State : Dict\n
      end_State : Dict
   '''
   return __make_eNKA(expression)

def test_eNKA(machine, text):
   '''
   Checks whether text belongs to a Machine's expression.\n
   IN:
      Machine : Dict
      Text : String
   OUT:
      Belongs : Bool
   '''
   currentStates = [machine[0]]

   currentStates = getEpsilonEnv(currentStates)

   for t in text:
      currentStates, _ = step_eNKA(currentStates, t)
      if not currentStates:
         return False

   for currentState in currentStates:
      if id(currentState) == id(machine[1]):
         return True
   
   return False

