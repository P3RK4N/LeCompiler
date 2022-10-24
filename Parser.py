__DEBUG__ = True

def importData(pathName):
   """
   IN: 
      pathName : String\n\n\n
   
   OUT:  
      regularDefines : Dict, 
      rules : Dict, 
      states : List, 
      uniforms : List
   """

   regularDefines = {}
   rules = {}
   states = []
   uniforms = []

   tmpData = open(pathName)
   data = []
   for row in tmpData:
      tmp = str(row.rstrip("\n").encode('utf-8'))
      tmp = tmp[2:len(tmp)-1]
      data.append(tmp)

   position = 0
   while position < len(data):
      line = data[position]

      #Regular definitions
      if line[0] == "{":
         definition,values = line.split(" ")

         for key in regularDefines:
            if not "eksponent" in line:
               values = values.replace(key, regularDefines[key])
            else:
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

         if state not in rules:
            rules[state] = {}

         rules[state][expression] = args

      position += 1

   return regularDefines, rules, states, uniforms