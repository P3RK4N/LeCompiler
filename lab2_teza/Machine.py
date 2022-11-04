from collections import defaultdict as dd
from collections import deque
import Util

__DEBUG__ = True

DOT = "@"
ARROW = "->"
BEGIN_STATE = "Q0"
EPSILON = "$"
EOF = "@EOF@"

REDUCE = "REDUCE"
ACCEPT = "ACCEPT"
MOVE = "MOVE"
PLACE = "PLACE"

#Initial vars
__nonEndings = None
__startingNonEnding = None
__endings = None
__synEndings = None
__productions = None

#Vars for creating starting endings
__emptyNonEndings = None
__directStarts = None
#Non-ending to all ending starts
__starts = None
#Root productions
__rootProductions = None

#Vars for eNKA
__stateName_to_subStates = None
__stateLHS_to_eState = None
__nonEnding_to_startSet = None
__eNKA_start = None
__stateID_to_subStateName = None
__stateID_to_subState = None

#Vars for DKA
#beggining -> 1
__DKA_stateIndex_to_eNKA_stateID_set = None
__DKA_stateIndex_to_DKA_state = None
__DKA_ID_to_stateIndex = None

#Action and NewState Table
__tableSA = None

#UNDEBUGGED
#Sets emptyNonEndings (with production to EPSILON or production to emptyNonEndings excusively)
def __setEmptyNonEndings():
   global __emptyNonEndings
   __emptyNonEndings = set()

   change = True
   while change:
      change = False
      for nonEnding,rhsProductions in __productions.items():
         if nonEnding in __emptyNonEndings:
            continue
         for rhsProduction in rhsProductions:
            if len(rhsProduction) == 1 and rhsProduction[0] == "$":
               change = True
               __emptyNonEndings.add(nonEnding)
            elif len(__emptyNonEndings) > 0:
               isEmptyNonEnding = True
               for part in rhsProduction:
                  if not part in __emptyNonEndings:
                     isEmptyNonEnding = False
                     break
               if isEmptyNonEnding:
                  __emptyNonEndings.add(nonEnding)
                  change = True
   
   if __DEBUG__:
      print("EMPTY NON ENDINGS:",__emptyNonEndings)
      print()

#UNDEBUGGED
#Recursively gets emptyNonEndings
def __setDirectStarts():
   global __directStarts
   __directStarts = dict()

   for nonEnding,rhsProductions in __productions.items():
      currentDirectStarts = set()
      for rhsProduction in rhsProductions:
         if len(rhsProduction) == 1 and rhsProduction[0] == "$":
            continue
         for productionPart in rhsProduction:
            currentDirectStarts.add(productionPart)
            if not productionPart in __emptyNonEndings:
               break
      __directStarts[nonEnding] = currentDirectStarts

   if __DEBUG__:
      print("DIRECT STARTS:",__directStarts)
      print()

#UNDEBUGGED
#Sets all ending characters with where production starts with them
def __setStarts():
   __setEmptyNonEndings()
   __setDirectStarts()

   global __starts
   __starts = dd(set)

   for nonEnding in __productions:
      currentStarts = set(__directStarts[nonEnding])
      currentStarts.discard(nonEnding)
      DFS = list(currentStarts)
      currentStarts.add(nonEnding)

      while DFS:
         current = DFS.pop()
         if not current in __directStarts:
            continue
         for next in __directStarts[current]:
            if not next in currentStarts:
               currentStarts.add(next)
               DFS.append(next)
      
      __starts[nonEnding] = currentStarts

   for nonEnding in __starts:
      for start in list(__starts[nonEnding]):
         if start in __productions:
            __starts[nonEnding].remove(start)
      
   if __DEBUG__:
      print("STARTS:",__starts)
      print()

#UNDEBUGGED
#Creates dictionary of states[stateName] -> dictionary of subStates[subStateName] -> dictionary substate
#Creates epsilon state that connects to all beginnings of states of that LHS production
def __createStates():
   global __stateName_to_subStates, __stateLHS_to_eState, __stateID_to_subStateName, __stateID_to_subState
   __stateName_to_subStates = dict()
   __stateLHS_to_eState = dict()
   __stateID_to_subStateName = dict()
   __stateID_to_subState = dict()

   for lhsProduction, rhsProductions in __productions.items():
      epsilonState = dd(list)
      if not lhsProduction in __stateLHS_to_eState:
         __stateLHS_to_eState[lhsProduction] = epsilonState
      else:
         epsilonState = __stateLHS_to_eState[lhsProduction]

      for rhsProduction in rhsProductions:
         stateName = lhsProduction + " -> " + ' '.join(rhsProduction)

         if not stateName in __stateName_to_subStates:
            __stateName_to_subStates[stateName] = dict()

         #Pure epsilon production
         if len(rhsProduction) == 1 and rhsProduction[0] == "$":
            subState = [lhsProduction, ARROW] + [DOT]
            subStateName = ' '.join(subState)
            subStateDict = dd(list)
            __stateID_to_subStateName[id(subStateDict)] = subStateName
            __stateID_to_subState[id(subStateDict)] = subStateDict
            __stateName_to_subStates[stateName][subStateName] = subStateDict
            epsilonState[EPSILON].append(subStateDict)
         #Non epsilon production
         else:
            for i in range(len(rhsProduction)+1):
               subState = [lhsProduction, ARROW] + rhsProduction[:i] + [DOT] + rhsProduction[i:]
               subStateName = ' '.join(subState)
               subStateDict = dd(list)
               __stateID_to_subStateName[id(subStateDict)] = subStateName
               __stateID_to_subState[id(subStateDict)] = subStateDict
               __stateName_to_subStates[stateName][subStateName] = subStateDict
               if i == 0:
                  epsilonState[EPSILON].append(subStateDict)

   if __DEBUG__:
      Util.printStates(__stateName_to_subStates,5)
      print()

      print("STATE LHS TO EPSILON STATE:")
      for stateLHS in __stateLHS_to_eState:
         print(stateLHS)
      print()
   
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!UNDEBUGGED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#Connect states
def __connectStates():
   global __nonEnding_to_startSet, __eNKA_start, __rootProductions
   __nonEnding_to_startSet = dd(set)
   __eNKA_start = list()
   __rootProductions = set()

   BFS = deque([__startingNonEnding])
   visited = set(BFS)
   
   while BFS:
      currentNonEnding = BFS.popleft()

      #Add EOF to begin state
      if currentNonEnding == __startingNonEnding:
         if not currentNonEnding in __nonEnding_to_startSet:
            __nonEnding_to_startSet[currentNonEnding] = set()
         __nonEnding_to_startSet[currentNonEnding].add(EOF)

      for rhsList in __productions[currentNonEnding]:
         stateName = currentNonEnding + " -> " + ' '.join(rhsList)

         #ADDS TO ROOT PRODUCTIONS
         if currentNonEnding == __startingNonEnding:
            __rootProductions.add(stateName)

         #ADDS BEGINNINGS TO LIST
         if currentNonEnding == __startingNonEnding:
            subState = [currentNonEnding, ARROW] + [DOT] + rhsList
            subStateName = ' '.join(subState)
            __eNKA_start.append(__stateName_to_subStates[stateName][subStateName])

         #Skip epsilon productions
         if len(rhsList) == 1 and rhsList[0] == "$":
            continue

         for i in range(len(rhsList)):
            subState = [currentNonEnding, ARROW] + rhsList[:i] + [DOT] + rhsList[i:]
            nextSubState = [currentNonEnding, ARROW] + rhsList[:i+1] + [DOT] + rhsList[i+1:]
            subStateName = ' '.join(subState)
            nextSubStateName = ' '.join(nextSubState)
            step = rhsList[i]

            #Connect current iteration of state to next iteration of same state
            __stateName_to_subStates[stateName][subStateName][step].append(__stateName_to_subStates[stateName][nextSubStateName])
            
            #Connect to epsilon of current step if its nonEnding
            if step in __stateLHS_to_eState:
               __stateName_to_subStates[stateName][subStateName][EPSILON].append(__stateLHS_to_eState[step])
            
            #Transfer starts set
            if step in __nonEndings:
               pos = i+1
               while pos < len(rhsList):
                  nextStep = rhsList[pos]
                  if nextStep in __nonEndings:
                     if nextStep in __starts:
                        for ending in __starts[nextStep]:
                           __nonEnding_to_startSet[step].add(ending)
                     if not nextStep in __emptyNonEndings:
                        break
                     else:
                        pos += 1
                  else:
                     __nonEnding_to_startSet[step].add(nextStep)
                     break
                  
               if pos == len(rhsList) and step in __starts:
                  for ending in __nonEnding_to_startSet[currentNonEnding]:
                     __nonEnding_to_startSet[step].add(ending)

            #Add step to DFS if nonEnding
            if step in __productions and not step in visited:
               visited.add(step)
               BFS.append(step)
   
   #Get eNKA starting state
   trueBegin_eNKA = dict()
   trueBegin_eNKA[EPSILON] = list()
   for start in __eNKA_start:
      trueBegin_eNKA[EPSILON].append(start)
   
   __eNKA_start = trueBegin_eNKA

   if __DEBUG__:
      print("CONNECTED STATES!")
      for stateID,state in __stateID_to_subState.items():
         if not len(state):
            continue
         print(__stateID_to_subStateName[stateID], "connected to:")
         print()
         for input,nextStates in state.items():
            for nextState in nextStates:
               if id(nextState) in __stateID_to_subStateName:
                  print(input,"#",__stateID_to_subStateName[id(nextState)])
               else:
                  print("EPSILON")
         print()

      print("NON ENDINGS TO STARTS:")
      for nonEnding,starts in __nonEnding_to_startSet.items():
         print(nonEnding, starts)
      print()

      print("ROOT PRODUCTIONS")
      print(__rootProductions)

      print()
      print()

#UNDEBUGGED
#Gets epsilon environment and removes empty states
def __getEpsilon(states):
   visited = set([id(state) for state in states])
   DFS = list(states)

   while DFS:
      currentState = DFS.pop()
      for nextState in currentState[EPSILON]:
         if not id(nextState) in visited:
            DFS.append(nextState)
            visited.add(id(nextState))
            states.append(nextState)
   
   return [state for state in states if id(state) in __stateID_to_subStateName]

#UNDEBUGGED
#Steps NKA
def __stepNKA(currentStates, input):
   nextStates = []
   visited = set()
   
   for currentState in currentStates:
      if input in currentState:
         for nextState in currentState[input]:
            if not id(nextState) in visited:
               visited.add(id(nextState))
               nextStates.append(nextState)
   return nextStates

#UNDEBUGGED
#Creates DKA from eNKA
def __make_DKA():
   global __DKA_stateIndex_to_eNKA_stateID_set, __DKA_stateIndex_to_DKA_state, __DKA_ID_to_stateIndex
   __DKA_stateIndex_to_eNKA_stateID_set = dict()
   __DKA_stateIndex_to_DKA_state = dict()
   __DKA_ID_to_stateIndex = dict()

   beginStates = __getEpsilon([__eNKA_start])
   beginStatesID_set = set([id(state) for state in beginStates])

   __DKA_stateIndex_to_eNKA_stateID_set[1] = beginStatesID_set
   __DKA_stateIndex_to_DKA_state[1] = dict()
   __DKA_ID_to_stateIndex[id(__DKA_stateIndex_to_DKA_state[1])] = 1
   DFS = [1]

   #Getting all transitions, 2**len(__stateID_to_subStateName) * len(inputs) possible -> VERY HOT PATH (NP complexity)
   inputs = set.union(__nonEndings, __endings)
   while DFS:
      current_DKA_stateID = DFS.pop()
      currentStates = list([__stateID_to_subState[stateID] for stateID in __DKA_stateIndex_to_eNKA_stateID_set[current_DKA_stateID]])

      for input in inputs:
         nextStates = __stepNKA(currentStates, input)
         nextStates = __getEpsilon(nextStates)
         if len(nextStates) == 0:
            continue
         nextStateID_set = set([id(nextState) for nextState in nextStates])
         next_DKA_index = -1
         #HOT PART - finding if dka state already exists
         for DKA_state_index, stateNamesSet in __DKA_stateIndex_to_eNKA_stateID_set.items():
            if stateNamesSet == nextStateID_set:
               next_DKA_index = DKA_state_index
               break
         if next_DKA_index == -1:
            next_DKA_index = len(__DKA_stateIndex_to_eNKA_stateID_set) + 1
            __DKA_stateIndex_to_DKA_state[next_DKA_index] = dict()
            __DKA_ID_to_stateIndex[id(__DKA_stateIndex_to_DKA_state[next_DKA_index])] = next_DKA_index 
            __DKA_stateIndex_to_eNKA_stateID_set[next_DKA_index] = nextStateID_set
            DFS.append(next_DKA_index)

         #Connect dka state to next via input
         __DKA_stateIndex_to_DKA_state[current_DKA_stateID][input] = __DKA_stateIndex_to_DKA_state[next_DKA_index]


   if __DEBUG__:
      print()
      print("MADE DKA!")
      print()

      for dkaState,eNKA_id_set in __DKA_stateIndex_to_eNKA_stateID_set.items():
         print(dkaState)
         print("--------------------")
         for eNKA_stateID in eNKA_id_set:
            print(__stateID_to_subStateName[eNKA_stateID]) 
         print("--------------------")
      
      print()

#UNFINISHED
#Minimize dka
#TODO(P3RK4N): implement if necessary
def __minimizeDKA():
   return

#UNDEBUGGED
#Makes action+newState table
def __makeTable():
   global __tableSA
   __tableSA = dd(lambda : dd(list))

   #CREATE ACCEPT AND REDUCE
   for stateNameDKA, stateID_set_eNKA in __DKA_stateIndex_to_eNKA_stateID_set.items():
      for stateID_eNKA in stateID_set_eNKA:
         stateName_eNKA = __stateID_to_subStateName[stateID_eNKA]

         if stateName_eNKA[-len(DOT):] == DOT:
            lhsProduction = stateName_eNKA.split(" ")[0]
            productionName = stateName_eNKA[:-2]

            #In case of pure epsilon production
            if len(productionName.split(" ")) == 2:
               productionName += " $"

            starts_set = __nonEnding_to_startSet[lhsProduction]
            for input in starts_set:
               if productionName in __rootProductions:
                  __tableSA[stateNameDKA][input].append((ACCEPT, productionName))
               else:
                  __tableSA[stateNameDKA][input].append((REDUCE, productionName))

   #CREATE MOVE AND PLACE
   for stateNameDKA, stateDKA in __DKA_stateIndex_to_DKA_state.items():
      for input, nextState in stateDKA.items():
         nextDKA_index = __DKA_ID_to_stateIndex[id(nextState)]
         if input in __endings:
            __tableSA[stateNameDKA][input].append((MOVE, nextDKA_index))
         else:
            __tableSA[stateNameDKA][input].append((PLACE, nextDKA_index))

   #OTHER IS DISCARD
   if __DEBUG__:
      print("SA TABLE:")
      for currentIndex, transitions in __tableSA.items():
         for input,transition in transitions.items():
            print(currentIndex, "-", input.rjust(5), "-", transition)
      print()
      print()
            
#UNDEBUGGED
def __make_eNKA():
   __setStarts()
   __createStates()
   __connectStates()

#Initialises initial vars
def __initGlobals(nonEndings, startingNonEnding, endings, synEndings, productions):
   global __nonEndings, __startingNonEnding, __endings, __synEndings, __productions
   __nonEndings = nonEndings
   __startingNonEnding = startingNonEnding
   __endings = endings 
   __synEndings = synEndings
   __productions = productions

   if __DEBUG__:
      print("INITIALIZED GLOBALS")

def getTableSA(nonEndings, startingNonEnding, endings, synEndings, productions):
   __initGlobals(nonEndings, startingNonEnding, endings, synEndings, productions)
   __make_eNKA()
   __make_DKA()
   __makeTable()
   return __tableSA, __nonEnding_to_startSet
