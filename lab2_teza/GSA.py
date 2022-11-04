import fileinput
import InputParser
import Machine

#TODO(P3RK4N): Dodaj pocetni nezavrsni znak

def __printProductions(productions):
   for lhsProduction in productions:
      print(lhsProduction)
      for rhsProduction in productions[lhsProduction]:
         print("    ", rhsProduction)

def __printInput(nonEndings, endings, synEndings, productions):
   print(nonEndings)
   print(endings)
   print(synEndings)
   __printProductions(productions)

def __main__():
   data = []

   for line in fileinput.input():
      tmp = str(line.rstrip("\n"))
      data.append(tmp)

   nonEndings, startingNonEnding, endings, synEndings, productions, priorities = InputParser.parseData(data)
   tableSA, nonEnding_to_startSet = Machine.getTableSA(nonEndings, startingNonEnding, endings, synEndings, productions)

   LA = open("analizator/SA.py", "w+")
   LA.write("tableSA = " + str(dict([(key,dict(values)) for key,values in tableSA.items()])) + '\n')
   LA.write("syn = " + str(synEndings) + '\n')
   LA.write("nonEnding_to_startSet = " + str(dict(nonEnding_to_startSet)) + '\n')
   LA.write("priority = " + str(priorities) + '\n')
   LA.write(r"""
   
import fileinput

EOF = "@EOF@"
BEGIN = "@FOE@"
EPSILON = "$"
__DEBUG__ = True

REDUCE = "REDUCE"
ACCEPT = "ACCEPT"
MOVE = "MOVE"
PLACE = "PLACE"

stack = [(BEGIN,-1), (1, 1)]
inputLA = []

for line in fileinput.input():
   inputLA.append(line.rstrip("\n").split(" "))

def parserSA():
   inputLA.append([EOF])

   pos = 0
   while True:
      line = inputLA[min(pos,len(inputLA)-1)]
      inputChar = line[0]
      
      if __DEBUG__:
         print("Line",pos+1)
         print("Input char", inputChar)
         print("Stack", stack)

      #OPORAVAK ????
      if not inputChar in tableSA[stack[-1][0]]:
         inputChar = EOF
         if not inputChar in tableSA[stack[-1][0]] or tableSA[stack[-1][0]][inputChar][0][0] == ACCEPT:
            while pos < len(inputLA)-1 and not inputLA[pos][0] in syn:
               pos += 1
            inputChar = inputLA[pos][0]
            if __DEBUG__:
               print("Error while parsing")
            while len(stack) > 3 and not inputChar in tableSA[stack[-1][0]]:
               stack.pop()
               stack.pop()
            if __DEBUG__:
               print("Stack reduced to:",stack)

      if not inputChar in tableSA[stack[-1][0]]:
         if __DEBUG__:
            print("Error while parsing input")
         return
      
      action_info_list = tableSA[stack[-1][0]][inputChar]
      action, info = None, None

      #Choosing priority
      #Regular
      if len(action_info_list) == 1:
         action,info = action_info_list[0]
      #REDUCE/MOVE
      elif action_info_list[0][0] == MOVE or action_info_list[1][0] == MOVE:
         if action_info_list[0][0] == MOVE:
            action, info = action_info_list[0]
         else:
            action, info = action_info_list[1]
      #REDUCE/ACCEPT (REDUCE/REDUCE)
      elif action_info_list[0][0] == REDUCE and action_info_list[1][0] == REDUCE:
         if __DEBUG__:
            print("##################REDUCE/REDUCE################")
         p = -1000000000
         for action_info in action_info_list:
            if priority[action_info[1]] > p:
               p = priority[action_info[1]]
               action, info = action_info


      if __DEBUG__:
         print("Action and info", action,info)
         print()
      #----------------------------------------------------------
      if action == MOVE:
         stack.append((inputChar, ' '.join(inputLA[pos])))
         stack.append((info, []))
      #----------------------------------------------------------
      elif action == REDUCE:
         lhsProduction, rhsProduction = info.split(" -> ")
         rhsParts = rhsProduction.split(" ")

         subOutput = []
         if not(len(rhsParts) == 1 and rhsParts[0] == EPSILON):
            for rhsPart in rhsParts[::-1]:
               stack.pop()
               if stack[-1][0] == rhsPart:
                  subOutput.append(stack[-1][1])
                  stack.pop()
               else:
                  if __DEBUG__:
                     print("Error while reducing")
                  return
         else:
            subOutput.append("$")
               
         stack.append((lhsProduction, [lhsProduction, subOutput[::-1]]))

         if not stack[-1][0] in tableSA[stack[-2][0]]:
            if __DEBUG__:
               print("REDUCTION DOESNT HAVE TRANSITION")
            return
         
         action, info = tableSA[stack[-2][0]][stack[-1][0]][0]
         
         if action != PLACE:
            if __DEBUG__:
               print("WEIRD")
            return
         
         stack.append((info, []))
         pos -= 1
      #--------------------------------------------------
      elif action == ACCEPT:
         lhsProduction,rhsProductions = info.split(" -> ")
         rhsParts = rhsProductions.split(" ")
         subOutput = []
         # if not(len(rhsParts) == 1 and rhsParts[0] == EPSILON):
         #    for rhsPart in rhsParts[::-1]:
         #       stack.pop()
         #       if stack[-1][0] == rhsPart:
         #          subOutput.append(stack[-1][1])
         #          stack.pop()
         #       else:
         #          if __DEBUG__:
         #             print("Error while Accepting")
         #          return
               
         if __DEBUG__:
            print("Prihvaceno")

         stack.pop()
         return stack[-1][1]
      #-----------------------------------------------------
      pos += 1

def printOutputRec(output, depth = 0):
   if not output:
      return
   for o in output:
      if len(o) == 0:
         pass
      elif isinstance(o, str):
         print(" "*(depth//2) + " "*int(o[0] != "<") + o)
      elif isinstance(o, list):
         printOutputRec(o, depth+1)

if __DEBUG__:
   print("SA TABLE:")
   for currentIndex, transitions in tableSA.items():
      for input,transition in transitions.items():
         print(currentIndex, "-", input.rjust(5), "-", transition)
   print()
   print()

output = parserSA()
# print(output)
printOutputRec(output)
   
   """)
   LA.close()


if __name__ == "__main__":
   __main__()