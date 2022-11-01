def parseData(data):
   nonEndings = set()
   startingNonEnding = None
   endings = set()
   synEndings = set()
   productions = dict()

   pos = 0
   while pos < len(data):
      line = data[pos]

      if len(line) > 1 and line[:2] == "%V":
         nonEndings = line[3:].split(" ")
         startingNonEnding = nonEndings[0]
         nonEndings = set(nonEndings)

      elif len(line) > 1 and line[:2] == "%T":
         endings = set(line[3:].split(" "))

      elif len(line) > 3 and line[:4] == "%Syn":
         synEndings = set(line[5:].split(" "))

      else:
         if not line in productions:
            productions[line] = []
         
         pos += 1
         while pos < len(data) and data[pos][0] == " ":
            productions[line].append(data[pos][1:].split(" "))
            pos += 1
         
         continue
      
      pos += 1
   
   return nonEndings, startingNonEnding, endings, synEndings, productions