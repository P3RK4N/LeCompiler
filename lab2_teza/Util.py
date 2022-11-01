def printStates(states, parts = 0):
   print("STATES and SUBSTATES")
   for stateName in states.keys() if not parts else list(states.keys())[:min(parts,len(states))]:
      print()
      print(stateName)
      print()
      for subStateName in states[stateName]:
         print(subStateName)
      print()