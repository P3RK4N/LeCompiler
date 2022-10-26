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
            if pos+1 < len(expression) and expression[pos+1] == "*":
               parts.append(expression[left:pos+2])
               pos += 1
            else:
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

def __cacheStates(states):
   cache = set()
   for state in states:
      for nextStates in state.values():
         cache.add(id(nextStates))
   return cache

def __filterDuplicatesID(nums):
   filtered = []
   repeats = set()
   for num in nums:
      if not id(num) in repeats:
         repeats.add(id(num))
         filtered.append(num)
   return filtered

def __filterDuplicateKidsID(root):
   if not isinstance(root, dict):
      return
   
   for letter, kids in root.items():
      cache = set()
      newKids = []
      for kid in kids:
         if id(kid) not in cache:
            cache.add(id(kid))
            newKids.append(kid)
      root[letter] = newKids
         
def make_eNKA(expression, root):
   '''
   Recursively creates e-NKA machine from given expression\n
   IN:
      expression : String
   OUT:
      machineEnds : List
   '''
   return __make_eNKA2(expression, root, True)
   # return __make_eNKA(expression, root, 0)

def __make_eNKA(expression, root = {}, depth = 0, mergeTo = None):
   if not depth and expression[0] != "(":
      expression = "(" + expression + ")"

   if not isinstance(root, list):
      root = [root]

   parts = __splitExpressionOR(expression)
   
   #parallel
   if len(parts) > 1:
      end = {}
      for part in parts:
         __make_eNKA(part, root, depth+1, end)

      if not depth:
         end["Valid"] = "Valid"
      return [end]
   
   #sequential
   else:
      parts = __splitExpressionAND(expression)
      currents = root

      for pos,part in enumerate(parts):
         #SUB_EXPRESSION************************
         if part[0] == "(":
            #Makes sure we dont connect wrong states
            cache = set()
            for current in currents:
               for key, listDict in current.items():
                  for d in listDict:
                     cache.add(id(d))

            ends = __make_eNKA(part[1:len(part)-1-int(part[-1] == "*")], currents, depth+1, mergeTo if pos+1 == len(parts) else None)
            
            if part[-1] == "*":
               for current in currents:
                  for key,listDict in current.items():
                      for end in ends:
                        if not key in end:
                           end[key] = []

                        currList = end[key]
                        for d in listDict:
                           if not id(d) in cache:
                              currList.append(d)
                        
                        if not end[key]:
                           del end[key]
            
            currents = ends

         #SINGLE_CHARACTER*****************************
         else:
            end = dict() if mergeTo == None else mergeTo
            for current in currents:
               if not part in current:
                  current[part] = []
               current[part].extend([end])
            
            currents = [end]
      
      if not depth:
         for current in currents:
            current["Valid"] = "Valid"

      return currents
   

#Returns list of ending states
def __make_eNKA2(expression, root = {}, first = False):
   if not isinstance(root, list):
      root = [root]
   
   partsOR = __splitExpressionOR(expression)

   
   #Sub Parts - converge them into one
   if len(partsOR) > 1:
      if __DEBUG__:
         print("OR parts from", expression)
         for part in partsOR:
            print(part)
         print()

      ending = {}
      parentList = []
      parentCache = set()
      
      for part in partsOR:
         tmpEndings = __make_eNKA2(part, root)

         #Use "PARENT" key to connect to root
         #(parentState, parentLetter)
         for tmpEnding in tmpEndings:
            if "PARENT" in tmpEnding:
               tmpParents = tmpEnding["PARENT"]
               for tmpParent in tmpParents:
                  if not (id(tmpParent[0]), tmpParent[1]) in parentCache:
                     parentCache.add((id(tmpParent[0]),tmpParent[1]))
                     tmpParent[0][tmpParent[1]].append(ending)
                     parentList.append(tmpParent)
                  tmpParent[0][tmpParent[1]] = [tmpKid for tmpKid in tmpParent[0][tmpParent[1]] if id(tmpKid) != id(tmpEnding)]

      ending["PARENT"] = __filterDuplicatesID(parentList)

      if first:
         ending["Valid"] = "Valid"

      return [ending]
   
   #Sequential Parts
   else:
      partsAND = __splitExpressionAND(expression)
      currentStates = root

      if __DEBUG__:
         print("AND parts from",expression)
         for partAND in partsAND:
            print(partAND)
         print()

      for index,partAND in enumerate(partsAND):
         if partAND[0] == "(":
            repeatable = partAND[-1] == "*"
            subPart = partAND[1:len(partAND) - 1 - int(repeatable)]
            subPartEndings = __make_eNKA2(subPart, currentStates)

            if repeatable:
               for currentState in currentStates:
                  for letter,nextStates in currentState.items():
                     for nextState in nextStates:
                        for subPartEnding in subPartEndings:
                           if not letter in subPartEnding:
                              subPartEnding[letter] = []
                           subPartEnding[letter].append(nextState)

            for subPartEnding in subPartEndings:
               __filterDuplicateKidsID(subPartEnding)
            
            if repeatable:
               currentStates.extend(subPartEndings)
            else:
               currentStates = subPartEndings 
         
         else:
            end = {"PARENT":[]}
            repeatedStates = set()
            for currentState in currentStates:
               if not partAND in currentState:
                  currentState[partAND] = []
               end["PARENT"].append((currentState, partAND))
               if not id(currentState) in repeatedStates:
                  currentState[partAND].extend([end])
                  repeatedStates.add(id(currentState))

            currentStates = [end]
      
      if first:
         for currentState in currentStates:
            currentState["Valid"] = "Valid"
            
      return currentStates