__DEBUG__ = False


def splitExpressionOR(expression):
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

def parseData(data):
   """
   IN: 
      data : List<String>\n
   
   OUT:  
      states : List<String>, 
      uniforms : Dict<String, Int>,
      rules : Dict<String, Dict<String, List<String>>> 
   """

   regularDefines = {}
   rules = {}
   rulePriorities = {}
   states = []
   uniforms = []

   position = 0
   priority = 0
   while position < len(data):
      line = data[position]

      #Regular definitions
      if line[0] == "{":
         definition,values = line.split(" ")

         for key in regularDefines:
            values = values.replace(key, "(" + regularDefines[key] + ")")

         regularDefines[definition] = values

      #States
      elif line[0:2] == "%X":
         states = line[3:].split(" ")

      #Uniforms
      elif line[0:2] == "%L":
         uniforms = line[3:].split(" ")
      
      #Rules
      else:
         tmpPos = line.find(">",1)
         state = line[1:tmpPos]
         expression = line[tmpPos+1:]

         for key in regularDefines:
            expression = expression.replace(key, "(" + regularDefines[key] + ")")
         
         args = []
         position += 2

         while data[position][0] != "}":
            args.append(data[position])
            position += 1

         if (state, expression) in rulePriorities:
            position += 1
            continue

         if not state in rules:
            rules[state] = {}
         
         rules[state][expression] = args

         rulePriorities[(state,expression)] = priority
         priority -= 1

      position += 1

   uniformsDict = {}

   for i,uniform in enumerate(uniforms):
      uniformsDict[uniform] = i

   return states, uniformsDict, rules, rulePriorities