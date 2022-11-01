import fileinput
import InputParser
import Machine

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


def __getTableAction():
   return

def __getTableNewState():
   return
         

def __main__():
   data = []

   for line in fileinput.input():
      tmp = str(line.rstrip("\n"))
      data.append(tmp)

   nonEndings, startingNonEnding, endings, synEndings, productions = InputParser.parseData(data)
   _ = Machine.make_eNKA(nonEndings, startingNonEnding, endings, synEndings, productions)

   
   LA = open("analizator/SA.py", "w+")
   LA.close()


if __name__ == "__main__":
   __main__()