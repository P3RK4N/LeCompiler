#izvorni program
#tablica uniformnih znakova
#tablica znakova
   #tablica identifikatora
   #tablica konstanti
   #tablica kljucnih rijeci, operatora i specijalnih znakova

import fileinput

import Parser


def __printDefines():
   for key,define in defines.items():
      print(key, define)
   print()

def __printExpressions(rules): 
   for rule,value in rules.items():
      for expression,args in value.items():
         print(expression)
   print()

def __main__():
   data = []

   for line in fileinput.input():
      tmp = str(line.rstrip("\n"))
      # tmp = tmp[1:len(tmp)-1]
      # tmp = tmp.replace("\\", "\\\\")

      data.append(tmp)


   states, uniforms, rules, rulePriorities = Parser.parseData(data)
   
   __printExpressions(rules)

   LA = open("analizator\\LA.py", "w")

   LA.write("states = " + str(states) + "\n")
   LA.write("uniforms = " + str(uniforms) + "\n")
   LA.write("rules = " + str(rules) + "\n")
   LA.write("rulePriorities = " + str(rulePriorities) + "\n")
   
   LA.close()


if __name__ == "__main__":
   __main__()