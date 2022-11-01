from collections import defaultdict as dd
from tkinter import E
import Util

__DEBUG__ = True

DOT = "@"
ARROW = "->"
BEGIN_STATE = "Q0"
EPSILON = "$"
EOF = "@EOF@"

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

#Vars for eNKA
__stateName_to_subStates = None
__stateLHS_to_eState = None
__nonEnding_to_startSet = None
__eNKA_start = None
__stateID_to_subStateName = None

#Vars for DKA
__NKA_stateID_to_eNKA_stateNamesSet = None



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
   global __stateName_to_subStates, __stateLHS_to_eState, __stateID_to_subStateName
   __stateName_to_subStates = dict()
   __stateLHS_to_eState = dict()
   __stateID_to_subStateName = dict()

   for lhsProduction, rhsProductions in __productions.items():
      epsilonState = dict()
      epsilonState[EPSILON] = list()
      __stateLHS_to_eState[lhsProduction] = epsilonState

      for rhsProduction in rhsProductions:
         stateName = lhsProduction + " -> " + ' '.join(rhsProduction)

         if not stateName in __stateName_to_subStates:
            __stateName_to_subStates[stateName] = dict()

         for i in range(len(rhsProduction)+1):
            subState = [lhsProduction, ARROW] + rhsProduction[:i] + [DOT] + rhsProduction[i:]
            subStateName = ' '.join(subState)
            subStateDict = dict()
            __stateID_to_subStateName[id(subStateDict)] = subStateName
            __stateName_to_subStates[stateName][subStateName] = subStateDict
            if i == 0:
               epsilonState[EPSILON].append(subStateDict)

   if __DEBUG__:
      print("SUBSTATES:")
      Util.printStates(__stateName_to_subStates,5)
      print()

      print("STATE LHS TO EPSILON STATE:")
      for stateLHS in __stateLHS_to_eState:
         print(stateLHS)
      print()
   
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!UNDEBUGGED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#Connect states
def __connectStates():
   global __nonEnding_to_startSet, __eNKA_start
   __nonEnding_to_startSet = dd(set)
   __eNKA_start = list()

   DFS = [__startingNonEnding]
   visited = set(DFS)
   
   while DFS:
      currentNonEnding = DFS.pop()

      #Add EOF to begin state
      if currentNonEnding == __startingNonEnding:
         if not currentNonEnding in __nonEnding_to_startSet:
            __nonEnding_to_startSet[currentNonEnding] = set()
         __nonEnding_to_startSet[currentNonEnding].add(EOF)

      for rhsList in __productions[currentNonEnding]:
         stateName = currentNonEnding + " -> " + ' '.join(rhsList)

         if currentNonEnding == __startingNonEnding:
            subState = [currentNonEnding, ARROW] + [DOT] + rhsList
            subStateName = ' '.join(subState)
            __eNKA_start.append(__stateName_to_subStates[stateName][subStateName])

         for i in range(len(rhsList)):
            subState = [currentNonEnding, ARROW] + rhsList[:i] + [DOT] + rhsList[i:]
            nextSubState = [currentNonEnding, ARROW] + rhsList[:i+1] + [DOT] + rhsList[i+1:]
            subStateName = ' '.join(subState)
            nextSubStateName = ' '.join(nextSubState)
            step = rhsList[i]

            #Connect current iteration of state to next iteration of same state
            __stateName_to_subStates[stateName][subStateName][step] = __stateName_to_subStates[stateName][nextSubStateName]
            
            #Connect to epsilon of current step if its nonEnding
            if step in __stateLHS_to_eState:
               __stateName_to_subStates[stateName][subStateName][EPSILON] = __stateLHS_to_eState[step]
            
            #Transfer starts set
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
                  __nonEnding_to_startSet[step].add(nextStep)
                  break

            if pos == len(rhsList):
               for ending in __nonEnding_to_startSet[currentNonEnding]:
                  __nonEnding_to_startSet[step].add(ending)

            #Add to step to DFS if nonEnding
            if step in __productions and not step in visited:
               visited.add(step)
               DFS.append(step)
   
   #Get eNKA starting state
   trueBegin_eNKA = dict()
   trueBegin_eNKA[EPSILON] = list()
   for start in __eNKA_start:
      trueBegin_eNKA[EPSILON].append(start)
   
   __eNKA_start = trueBegin_eNKA

   if __DEBUG__:
      print("CONNECTED STATES!")

#UNFINISHED
#Creates DKA from eNKA
def __make_DKA():
   return

#UNFINISHED
def __make_eNKA():
   __setStarts()
   __createStates()
   __connectStates()

   return

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

def make_eNKA(nonEndings, startingNonEnding, endings, synEndings, productions):
   __initGlobals(nonEndings, startingNonEnding, endings, synEndings, productions)
   return __make_eNKA()