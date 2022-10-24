#izvorni program
#tablica uniformnih znakova
#tablica znakova
   #tablica identifikatora
   #tablica konstanti
   #tablica kljucnih rijeci, operatora i specijalnih znakova

import eNKA
import Parser
import Machine

defines, rules, states, uniforms = Parser.importData("data.txt")

def printDefines():
   for key,define in defines.items():
      print(key, define)
   print()

def printExpressions(): 
   for rule,value in rules.items():
      for expression,args in value.items():
         print(expression)
   print()

def test_eNKA(expression):
   machine = {}
   ends = eNKA.make_eNKA(expression, machine)
   # print(machine)
   print("Done")

def test_eNKA(expression, value):
   machine = {}
   eNKA.make_eNKA(expression, machine)
   print(machine)
   states = dict()
   states[id(machine)] = machine
   for letter in value:
      newStates = {}
      for stateId, prevState in states.items():
         if letter in prevState:
            nextStates = prevState[letter]
            for newState in nextStates:
               if not id(newState) in newStates:
                  newStates[id(newState)] = newState

      states = newStates

   for state in states.values():
      if "Valid" in state:
         return True
      
   return False 

def dfs_eNKA(expression):
   machine = {}
   eNKA.make_eNKA(expression, machine)

   visited = {id(machine)}
   from collections import deque as dq
   stack = dq([(0,machine)])

   while stack:
      depth, current = stack.popleft()
      if isinstance(current,str):
         continue

      for letter, nextStates in current.items():
         print(id(current)," "*6*depth,(" "*(8-len(letter))) + letter, "    Next:", [id(ns) if not isinstance(ns, tuple) else id(ns[0]) for ns in nextStates if not isinstance(nextStates, str)])
         for ns in nextStates:
            if id(ns) not in visited and not isinstance(ns, tuple):
               stack.append((depth+1,ns))
               visited.add(id(ns))
      print()

      
def dfs_machine(machine):
   currentStates = [machine[0]]
   visited = {id(currentStates)}

   while currentStates:
      newStates = []
      for state in currentStates:
         for letter,nextStates in state.items():
            for nextState in nextStates:
               if not id(nextState) in visited: 
                  visited.add(id(nextState))
                  print(id(state), letter, id(nextState))
                  newStates.append(nextState)
            print()
      currentStates = newStates

eNKA = Machine.make_eNKA("(0|1|2|3|4|5|6|7|8|9)*.(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*($|((e|E)($|+|-)(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*))")

print(Machine.test_eNKA(eNKA, ".9e+1"))