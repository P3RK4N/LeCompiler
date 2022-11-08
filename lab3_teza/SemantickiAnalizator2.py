import fileinput
from collections import deque, defaultdict as dd
import Util

#DEBUGGING & GLOBALS #######################################################################################
__DEBUG__ = False

PARENT = "PARENT" #Parent Node
KIDS = "KIDS"     #Kid Nodes
SCOPE = "SCOPE"   #Declared vars or functions
TYPE = "TYPE"     #Type of scope identity
NAME = "NAME"     #Name of scope identity (Redundant)
CURRENT_FUNC = "CURRENT_FUNC"     #Current function
FUNCS = "FUNCS"   #Functions defined in this scope
DECL = "DECL"     #Declared, but undefined identities in this scope
LVAL = "LVAL"     #Is identity an lvalue?

INT = "INT"
CONST_INT = "CONST INT"
CONST_INT_ARRAY = "CONST INT ARRAY"
INT_ARRAY = "INT ARRAY"

CHAR = "CHAR"
CHAR_ARRAY = "CHAR ARRAY"
CONST_CHAR = "CONST CHAR"
CONST_CHAR_ARRAY = "CONST CHAR ARRAY"

VOID = "VOID"
ARRAY = "ARRAY"
CONST = "CONST"

castDict = {
   INT : {INT, CONST_INT, CHAR, CONST_CHAR},
   CONST_INT : {INT, CONST_INT, CHAR, CONST_CHAR},

   CHAR : {INT, CONST_INT, CHAR, CONST_CHAR},
   CONST_CHAR : {INT, CONST_INT, CHAR, CONST_CHAR},

   INT_ARRAY : {},
   CONST_INT_ARRAY : {},
   CHAR_ARRAY : {},
   CONST_CHAR_ARRAY : {}
}

equalDict = {
   INT : {INT, CHAR, CONST_INT, CONST_CHAR},
   CHAR : {CHAR, CONST_CHAR}
}

genTreeInput = deque()

funcStack = []
loopStack = []
lastCharArrayLen = 0

#Current scope
#scopeNode[PARENT] = scopeNodeParent if not global else None
#scopeNode[DECL] = dict of declarations
globalScopeNode = {
   PARENT : None,
   KIDS: [],
   FUNCS : dict(),
   DECL : dict(),
   SCOPE : dd(lambda : dict())
}

currentScope = globalScopeNode

def throwError(e = ""):
   # print("ERROR",e)
   print(e)
   exit(0)

########################################################################################
#IZRAZI ################################################################################
########################################################################################

#PRIMARNI IZRAZ# FINISHED
def primarni_izraz(): #Returns type, lval
   #LHS production
   production = genTreeInput.popleft()[0] + " ::="

   if "IDN" in genTreeInput[0][0]:
      kros, line, val = genTreeInput.popleft()[0].split(" ")
      production += Util.stringify1(kros,line,val)

      t, lval = Util.getDeclaredType(currentScope, val)

      if t == None:
         throwError(production)

      return t, lval

   elif "BROJ" in genTreeInput[0][0]:
      kros, line, val = genTreeInput.popleft()[0].split(" ")
      production += Util.stringify1(kros,line,val)
      val = int(val)

      if val < -2**32 or val >= 2**32:
         throwError(production)
      
      return INT, False

   elif "NIZ_ZNAKOVA" in genTreeInput[0][0]:
      kros, line, val = genTreeInput.popleft()[0].split(" ")
      production += Util.stringify1(kros, line, val)

      if val[0] != "\"" or val[-1] != "\"":
         throwError(production)
      else:   
         for pos in range(1,len(val)-1):
            if val[pos] == "\\" and (pos == len(val)-2 or not val[pos+1] in {'\\', "t", "n", "\"", "\'", "0"}):
               throwError(production)

      global lastCharArrayLen
      lastCharArrayLen = len(val) + 1 - len([c for c in val if c == "\\"]) - 2

      return CONST_CHAR_ARRAY, False

   elif "ZNAK" in genTreeInput[0][0]:
      kros, line, val = genTreeInput.popleft()[0].split(" ")
      production += Util.stringify1(kros,line,val)
      val = val[1:-1]

      if len(val) == 2:
         if val[0] != "\\" or not val[1] in {'\\', "t", "n", "\"", "\'", "0"}:
            throwError(production)
      else:
         if val[0] in {'\\', '\''}:
            throwError(production)

      return CHAR, False
   
   elif "L_ZAGRADA" in genTreeInput[0][0]:
      production += Util.stringify(genTreeInput.popleft()[0])
      production += " <izraz>"
      t, lval = izraz()
      production += Util.stringify(genTreeInput.popleft()[0])
      return t, lval

#POSTFIKS IZRAZ# FINISHED - CRITICAL
def postfiks_izraz(): #Returns type, lval
   #LHS production
   production = genTreeInput.popleft()[0] + " ::="
   
   if "<primarni_izraz>" == genTreeInput[0][0]:
      return primarni_izraz()
   
   #Postfix izraz - dodaj u produkciju
   elif "<postfiks_izraz>" == genTreeInput[0][0]:
      production += " <postfiks_izraz>"
      postType, postLval = postfiks_izraz()

      #ARRAY ELEMENT
      #L UGL ZAGRADA - dodaj u produkciju, provjeri jel niz i jel tip izraza int
      if "L_UGL_ZAGRADA" in genTreeInput[0][0]:
         production += Util.stringify(genTreeInput.popleft()[0])

         #IZRAZ - dodaj u produkciju
         production += " <izraz>"

         if not ARRAY in postType:
            production += Util.findOtherBracket(genTreeInput, "L_UGL_ZAGRADA", "D_UGL_ZAGRADA")
            throwError(production)

         izrazType, izrazLval = izraz()

         #D_UGL_ZAGRADA - dodaj u produkciju
         production += genTreeInput.popleft()[0]

         if not izrazType in castDict[INT]:
            throwError(production)
         
         return postType.replace(" ARRAY", ""), not CONST in postType

      #INCREMENTIRANJE
      elif "OP_INC" in genTreeInput[0][0] or "OP_DEC" in genTreeInput[0][0]:
         production += Util.stringify(genTreeInput.popleft()[0])

         if not postType in castDict[INT] or postLval == False:
            throwError(production) 
         
         return INT, False
      
      #FUNCTION CALL
      elif "L_ZAGRADA" in genTreeInput[0][0]:
         production += Util.stringify(genTreeInput.popleft()[0])
         argsType = ""

         #Lista argumenata - dodaj u produkciju, provjeri jel su tipovi isti
         if "<lista_argumenata>" in genTreeInput[0][0]:
            production += " <lista_argumenata>"
            argsType = ",".join(lista_argumenata())

         #D ZAGRADA - dodaj u produkciju
         production += Util.stringify(genTreeInput.popleft()[0])

         #Parametri ne pripadaju ovoj funkciji
         # print(postType, "=", argsType)
         if "|" not in postType or postType.split("|")[1] != argsType:
            throwError(production)

         return postType.split("|")[0], False

#LISTA ARGUMENATA# FINISHED
def lista_argumenata(): #Returns list(types)
   genTreeInput.popleft()[0]

   if "<izraz_pridruzivanja>" == genTreeInput[0][0]:
      return [izraz_pridruzivanja()[0]]

   elif "<lista_argumenata>" == genTreeInput[0][0]:
      types = lista_argumenata()
      #ZAREZ
      genTreeInput.popleft()[0]
      return types + [izraz_pridruzivanja()[0]]

#UNARNI IZRAZ# FINISHED
#UNARNI OPERATOR# FINISHED
def unarni_izraz():
   #LHS production
   production = genTreeInput.popleft()[0] + " ::="

   if "<postfiks_izraz>" == genTreeInput[0][0]:
      return postfiks_izraz()

   #Dodaj u produkciju i provjeri jel tip INT
   elif "OP_INC" in genTreeInput[0][0] or "OP_DEC" in genTreeInput[0][0]:
      #Operator
      production += Util.stringify(genTreeInput.popleft()[0])

      #Unarni izraz
      production += " <unarni_izraz>"
      unarniType, unarniLval = unarni_izraz()

      if unarniLval == False or not unarniType in castDict[INT]:
         throwError(production)

      return INT, False

   elif "<unarni_operator>" == genTreeInput[0][0]:
      production += " <unarni_operator> <cast_izraz>"
      genTreeInput.popleft()[0]
      genTreeInput.popleft()[0]
      castType, castLval = cast_izraz()

      if not castType in castDict[INT]:
         throwError(production)

      return INT, False

#CAST IZRAZ# FINISHED
def cast_izraz(): #Returns type, lval
   #LHS production
   production = genTreeInput.popleft()[0] + " ::="

   if "<unarni_izraz>" == genTreeInput[0][0]:
      return unarni_izraz()

   #Dodaj u produkciju, provjeri da se ovo moze eksplicitno castat
   elif "L_ZAGRADA" in genTreeInput[0][0]:
      #L ZAGRADA - dodaj u produkciju
      production += Util.stringify(genTreeInput.popleft()[0])

      #IME TIPA - dodaj u produkciju
      production += " <ime_tipa>"
      imeType = ime_tipa()

      #D ZAGRADA - dodaj u produkciju
      production += Util.stringify(genTreeInput.popleft()[0])

      #Cast izraz - dodaj u produkciju, provjeri jel moze convertat
      production += " <cast_izraz>"
      castType, castLval = cast_izraz()

      if not castType in castDict[imeType]:
         throwError(production)

      return imeType, False

#IME TIPA# - FINISHED
#SPECIFIKATOR TIPA# - FINISHED
def ime_tipa():
   # print(list(genTreeInput)[0:5])

   #Dodaj lhs na produkciju
   production = genTreeInput.popleft()[0] + " ::="

   isConst = False
   #KR CONST - dodaj na produkciju
   if "KR_CONST" in genTreeInput[0][0]:
      production += Util.stringify(genTreeInput.popleft()[0])
      isConst = True
   
   # print(list(genTreeInput)[0:5])
   #Specifikator tipa - dodaj na produkciju
   production += " " + genTreeInput.popleft()[0]

   #Tip
   tip = genTreeInput.popleft()[0].split(" ")[0][3:]

   if tip == VOID and isConst:
      throwError(production)

   return int(isConst)*"CONST " + tip

#IZRAZI# FINISHED
def operacijski_izrazi(top): #Returns type, lval
   #LHS production
   production = genTreeInput.popleft()[0] + " ::="

   #Podizraz
   if izrazi[top] == genTreeInput[0][0]:
      if izrazi[top] != "<cast_izraz>":
         return operacijski_izrazi(izrazi[top])
      else:
         return cast_izraz()
      
   #Isti izraz - dodaj u produkciju
   elif top == genTreeInput[0][0]:
      topType, topLval = operacijski_izrazi(top)
      production += " " + top

      #Operator - dodaj u produkciju
      production += Util.stringify(genTreeInput.popleft()[0])

      #Podizraz - dodaj u produkciju
      production += " " + izrazi[top]

      if not topType in castDict[INT]:
         throwError(production)

      bottomType, bottomLval = None, None

      if izrazi[top] != "<cast_izraz>":
         bottomType, bottomLval = operacijski_izrazi(izrazi[top])
      else:
         bottomType, bottomLval = cast_izraz()

      if not bottomType in castDict[INT]:
         throwError(production)

      return INT, False
      

izrazi = {
   "<multiplikativni_izraz>" : "<cast_izraz>",
   "<aditivni_izraz>" : "<multiplikativni_izraz>",
   "<odnosni_izraz>" : "<aditivni_izraz>",
   "<jednakosni_izraz>" : "<odnosni_izraz>",
   "<bin_i_izraz>" : "<jednakosni_izraz>",
   "<bin_xili_izraz>" : "<bin_i_izraz>",
   "<bin_ili_izraz>" : "<bin_xili_izraz>",
   "<log_i_izraz>" : "<bin_ili_izraz>",
   "<log_ili_izraz>" : "<log_i_izraz>"
}

#IZRAZ PRIDRUZIVANJA# FINISHED
def izraz_pridruzivanja(): #Returns type, lval
   #LHS production
   production = genTreeInput.popleft()[0] + " ::="

   #LOG ILI IZRAZ
   if "<log_ili_izraz>" == genTreeInput[0][0]:
      return operacijski_izrazi("<log_ili_izraz>")
   
   #POSTFIKS IZRAZ - dodaj na produkciju
   elif "<postfiks_izraz>" == genTreeInput[0][0]:
      production += " <postfiks_izraz>"
      postfiksType, postfiksLval = postfiks_izraz()

      #OP PRIDRUZI - dodaj na produkciju
      production += Util.stringify(genTreeInput.popleft()[0])

      #Izraz pridruzivanja - dodaj na produkciju, ako je sve ispravno nastavi, inace baci gresku
      production += " <izraz_pridruzivanja>"

      if postfiksLval == False:
         throwError(production)

      pridType, pridLval = izraz_pridruzivanja()

      if not postfiksType in castDict[pridType]:
         throwError(production)

      return postfiksType, False
   
#IZRAZ# FINISHED
def izraz(): #Returns type, lval
   genTreeInput.popleft()[0]
   wasIzraz = False

   #Izraz
   if "<izraz>" == genTreeInput[0][0]:
      wasIzraz = True
      izraz()
      #Zarez
      genTreeInput.popleft()[0]

   #Izraz pridruzivanja
   if wasIzraz:
      return izraz_pridruzivanja()[0], False
   return izraz_pridruzivanja()

########################################################################################
#NAREDBENA STRUKTURA ###################################################################
########################################################################################

#SLOZENA NAREDBA# - FINISHED
def slozena_naredba():
   #LHS
   genTreeInput.popleft()[0]

   #L_VIT_ZAGRADA
   genTreeInput.popleft()[0]

   if "<lista_deklaracija>" == genTreeInput[0][0]:
      lista_deklaracija()

   lista_naredbi()

   #D_VIT_ZAGRADA
   genTreeInput.popleft()[0]

#LISTA NAREDBI# - FINISHED
def lista_naredbi():
   genTreeInput.popleft()[0]

   if "<lista_naredbi>" == genTreeInput[0][0]:
      lista_naredbi()

   naredba()

#IZRAZ NAREDBA
def izraz_naredba():
   genTreeInput.popleft()[0]
   t = INT

   if "<izraz>" == genTreeInput[0][0]:
      t, _ = izraz()

   genTreeInput.popleft()[0]
   return t

#NAREDBA# FINISHED - CRITICAL CRITICAL
def naredba():
   global loopStack
   #LHS production
   genTreeInput.popleft()[0]

   if "<slozena_naredba>" == genTreeInput[0][0]:
      global currentScope
      newScope = {
         PARENT : None,
         KIDS: [],
         FUNCS : dict(),
         DECL : dict(),
         SCOPE : dd(lambda : dict())
      }
      newScope[PARENT] = currentScope
      currentScope[KIDS].append(newScope)
      currentScope = newScope
      slozena_naredba()
      currentScope = currentScope[PARENT]

   elif "<izraz_naredba>" == genTreeInput[0][0]:
      izraz_naredba()

   elif "<naredba_grananja>" == genTreeInput[0][0]:
      production = genTreeInput.popleft()[0] + " ::="
      production += Util.stringify(genTreeInput.popleft()[0])
      production += Util.stringify(genTreeInput.popleft()[0])
      production += " <izraz>"
      t, _ = izraz()
      line, depth = genTreeInput.popleft()
      production += Util.stringify(line)
      production += " <naredba>"

      if not t in castDict[INT]:
         genTreeInput.popleft()
         while genTreeInput[0][1] > depth:
            genTreeInput.popleft()
         if "KR_ELSE" in genTreeInput[0][0]:
            production += Util.stringify(genTreeInput.popleft()[0])
            production += " <naredba>"
            throwError(production)
            
      else:
         naredba()

      if "KR_ELSE" in genTreeInput[0][0]:
         production += Util.stringify(genTreeInput.popleft()[0])
         production += " <naredba>"
         naredba()

   elif "<naredba_petlje>" == genTreeInput[0][0]:
      production = genTreeInput.popleft()[0] + " ::="
      if "KR_WHILE" in genTreeInput[0][0]:
         production += Util.stringify(genTreeInput.popleft()[0])
         production += Util.stringify(genTreeInput.popleft()[0])
         production += " <izraz>"
         t, _ = izraz()
         production += Util.stringify(genTreeInput.popleft()[0])
         production += " <naredba>"
         if not t in castDict[INT]:
            throwError(production)

         loopStack.append(1)
         naredba()
         loopStack.pop()

      elif "KR_FOR" in genTreeInput[0][0]:
         line, depthh = genTreeInput.popleft()
         production += Util.stringify(line)
         production += Util.stringify(genTreeInput.popleft()[0])
         production += " <izraz_naredba>"
         production += " <izraz_naredba>"
         izraz_naredba()
         t = izraz_naredba()

         if "<izraz>" == genTreeInput[0][0]:
            production += " <izraz>"

            if not t in castDict[INT]:
               genTreeInput.popleft()
               while genTreeInput[0][1] > depthh:
                  genTreeInput.popleft()
               production += Util.stringify(genTreeInput.popleft()[0])
               production += " <naredba>"
               throwError(production)

            else:
               izraz()
         
         genTreeInput.popleft()
         loopStack.append(1)
         naredba()
         loopStack.pop()

   #Naredba skoka
   elif "<naredba_skoka>" == genTreeInput[0][0]:
      production = genTreeInput.popleft()[0] + " ::="

      if "KR_CONTINUE" in genTreeInput[0][0] or "KR_BREAK" in genTreeInput[0][0]:
         production += Util.stringify(genTreeInput.popleft()[0])
         production += Util.stringify(genTreeInput.popleft()[0])
         
         if len(loopStack) == 0:
            throwError(production)

      #KR RETURN
      elif "KR_RETURN" in genTreeInput[0][0]:
         production += Util.stringify(genTreeInput.popleft()[0])
         returnType = ""

         #Izraz - dodaj na produkciju, stavi u returnType
         if "<izraz>" == genTreeInput[0][0]:
            production += " <izraz>"
            returnType = izraz()[0]

         #Tockazarez - dodaj na produkciju
         production += Util.stringify(genTreeInput.popleft()[0])

         if returnType == "":
            returnType = VOID

         #Throw error ako nije isti povratni tip
         if not funcStack or Util.getFuncType(funcStack[-1], currentScope[PARENT]).split("|")[0] != returnType:
            throwError(production)

   else:
      print("A")      
      
#PRIJEVODNA JEDINICA# - FINISHED
#VANJSKA DEKLARACIJA# - FINISHED
def prijevodna_jedinica():
   genTreeInput.popleft()[0]

   if "<prijevodna_jedinica>" == genTreeInput[0][0]:
      prijevodna_jedinica()

   #Vanjska Deklaracija
   genTreeInput.popleft()[0]

   if  "<definicija_funkcije>" == genTreeInput[0][0]:
      definicija_funkcije()

   elif "<deklaracija>" == genTreeInput[0][0]:
      deklaracija()

      
########################################################################################
#DEKLARACIJE I DEFINICIJE ##############################################################
########################################################################################

#DEFINICIJA FUNKCIJE#
def definicija_funkcije():
   global currentScope, globalScopeNode
   #Dodaj LHS na produkciju
   current = genTreeInput.popleft()[0]
   production = current + " ::= " + "<ime_tipa>"
   error = False

   #Ime tipa - dohvati returnType i provjeri jel const
   returnType = ime_tipa()
   funcType = None
   error |= CONST in returnType

   #IDN - provjeri jel postoji definirana func s tim imenom, dodaj na produkciju
   idn, typeLine, funcName = genTreeInput.popleft()[0].split(" ")
   production += Util.stringify1(idn, typeLine, funcName)
   error |= Util.functionExists(funcName, globalScopeNode)

   #L ZAGRADA - dodaj na produkciju
   production += Util.stringify(genTreeInput.popleft()[0])

   types_names_params = None
   #KR VOID - dodaj na produkciju, dohvati paramType, ako deklarirana, mora bit isti tip, dodaj u scope
   if "KR_VOID" in genTreeInput[0][0]:
      production += Util.stringify(genTreeInput.popleft()[0])
      funcType = returnType + "|"
      if funcName in globalScopeNode[DECL]:
         error |= globalScopeNode[DECL][funcName] != funcType
         del globalScopeNode[DECL][funcName]
      currentScope[FUNCS][funcName] = funcType
   
   #LISTA PARAMETARA - isto kao i KR VOID
   elif "<lista_parametara>" == genTreeInput[0][0]:
      production += " <lista_parametara>"
      if not error:
         types_names_params = lista_parametara()
         funcType = returnType + "|" + ",".join([tn[0] for tn in types_names_params])
         if funcName in globalScopeNode[DECL]:
            error |= globalScopeNode[DECL][funcName] != funcType
            del globalScopeNode[DECL][funcName]
         globalScopeNode[FUNCS][funcName] = funcType

      else:
         #Poppaj do zatvorene zagrade
         cnt = 1
         while not (cnt == 1 and  "D_ZAGRADA" in genTreeInput[0][0]):
            if "L_ZAGRADA" in genTreeInput[0][0]:
               cnt += 1
            elif "D_ZAGRADA" in genTreeInput[0][0]:
               cnt -= 1
            genTreeInput.popleft()[0]

   #D ZAGRADA - dodaj na produkciju
   production += Util.stringify(genTreeInput.popleft()[0])

   #Slozena naredba - dodaj na produkciju, napravi novi scope i udi, dodaj function stack, dodaj parametre u scope, udji u slozenu funkciju, skini function stack, izadi iz scopea
   production += " <slozena_naredba>"
   if not error:
      #Ulaz u function scope
      newNode = {
         PARENT : currentScope,
         KIDS: [],
         FUNCS : dict(),
         DECL : dict(),
         SCOPE : dd(lambda : dd(None))
      }
      currentScope[KIDS].append(newNode)
      currentScope = newNode

      if types_names_params:
         for t,n in types_names_params:
            currentScope[SCOPE][n][TYPE] = t
            currentScope[SCOPE][n][LVAL] = not CONST in currentScope[SCOPE][n][TYPE] and not ARRAY in currentScope[SCOPE][n][TYPE]

      #Stavljanje funkcije na stack
      global funcStack
      funcStack.append(funcName)

      #Slozena naredba
      slozena_naredba()

      #Skidanje sa stacka
      funcStack.pop()

      #Izlaz iz function scopea
      currentScope = currentScope[PARENT]

   #KRAJ
   if error:
      throwError(production)

#LISTA PARAMETARA# FINISHED
def lista_parametara():
   #LHS production
   production = genTreeInput.popleft()[0] + " ::="
   types_names_list = []

   if "<lista_parametara>" == genTreeInput[0][0]:
      types_names_list.extend(lista_parametara())
      production += " <lista_parametara>"
      production += genTreeInput.popleft()[0]

   production += " <deklaracija_parametra>"
   types_names_list.append(deklaracija_parametra())

   names = set()
   for tn in types_names_list:
      names.add(tn[1])

   if len(names) != len(types_names_list):
      throwError(production)

   return types_names_list

#DEKLARACIJA PARAMETRA# FINISHED
def deklaracija_parametra():
   # print("dekl",list(genTreeInput)[0:5])

   #LHS production
   production = genTreeInput.popleft()[0] + " ::="
   production += " <ime_tipa>"

   t = ime_tipa()

   kros, line, val = genTreeInput.popleft()[0].split(" ")
   production += Util.stringify1(kros, line, val)

   if "L_UGL_ZAGRADA" in genTreeInput[0][0]:
      production += Util.stringify(genTreeInput.popleft()[0])
      production += Util.stringify(genTreeInput.popleft()[0])
      t = t + " " + ARRAY

   if VOID in t:
      throwError(production)

   # global currentScope
   # currentScope[DECL][val] = t
   
   return t, val

#LISTA DEKLARACIJA# FINISHED
def lista_deklaracija():
   genTreeInput.popleft()[0]

   if "<lista_deklaracija>" == genTreeInput[0][0]:
      lista_deklaracija()

   deklaracija()

#DEKLARACIJA# FINISHED
def deklaracija():
   genTreeInput.popleft()[0]
   t = ime_tipa()
   lista_init_deklaratora(t)
   genTreeInput.popleft()[0]

#LISTA INIT DEKLARATORA# FINISHED
def lista_init_deklaratora(t):
   genTreeInput.popleft()[0]

   if "<lista_init_deklaratora>" == genTreeInput[0][0]:
      lista_init_deklaratora(t)
      genTreeInput.popleft()[0]
   
   init_deklarator(t)

#INIT DEKLARATOR# FINISHED - CRITICAL
def init_deklarator(t):
   global currentScope
   #LHS production
   production = genTreeInput.popleft()[0] + " ::="

   #Izravni deklarator
   production += " <izravni_deklarator>"
   declType, declSize, declName = izravni_deklarator(t)

   #Operator - dodaj u produkciju
   if "OP_PRIDRUZI" in genTreeInput[0][0]:
      production += Util.stringify(genTreeInput.popleft()[0])
      production += " <inicijalizator>"
   
   elif CONST in declType:
      throwError(production)

   else:
      return

   #inicijalizator - dodan vec u produkciju
   initTypes = inicijalizator()

   #Inicijalizator je array manji ili jednak i sadrzi sve castable objekte
   if ARRAY in declType:
      if declSize < len(initTypes):
         throwError(production)
      else:
         for type in initTypes:
            if type not in castDict[declType]:
               throwError(production)

   #Nema pridruzivanja funkciji
   elif "|" in declType:
      throwError(production)

   #Inicijalizator nije array i jedan objekt je castable
   elif len(initTypes) > 1 or (not initTypes[0] == declType and not initTypes[0] in equalDict[declType]):
      throwError(production)

   del currentScope[DECL][declName]
   currentScope[SCOPE][declName][TYPE] = declType

#IZRAVNI DEKLARATOR# FINISHED - CRITICAL
def izravni_deklarator(t): #Returns type, size, name
   #LHS production
   production = genTreeInput.popleft()[0] + " ::="

   #IDN
   kros, line, name = genTreeInput.popleft()[0].split(" ")
   production += Util.stringify1(kros, line, name)
   
   if "L_UGL_ZAGRADA" in genTreeInput[0][0]:
      production += Util.stringify(genTreeInput.popleft()[0])

      #BROJ
      kros, line, val = genTreeInput.popleft()[0].split(" ")
      production += Util.stringify1(kros, line, val)
      val = int(val)

      #D UGL ZAGRADA
      production += Util.stringify(genTreeInput.popleft()[0])

      if val < 1 or val > 1024 or t == VOID or name in currentScope[DECL]:
         throwError(production)

      t = t + " " + ARRAY
      currentScope[DECL][name] = t
      return t, val, name

   elif "L_ZAGRADA" in genTreeInput[0][0]:
      production += Util.stringify(genTreeInput.popleft()[0])

      #Funkcija bez parametara
      if "KR_VOID" in genTreeInput[0][0]:
         production += Util.stringify(genTreeInput.popleft()[0])
         production += Util.stringify(genTreeInput.popleft()[0])
         t = t + "|"

         if name in currentScope[DECL]:
            if currentScope[DECL][name] != t:
               throwError(production)
         else:
            currentScope[DECL][name] = t
         
         return t, 1, name

      #Funkcija s parametrima
      elif "<lista_parametara>" == genTreeInput[0][0]:
         production += " <lista_parametara>"
         types_names_params = lista_parametara()
         types = [t for t,n in types_names_params]
         production += Util.stringify(genTreeInput.popleft()[0])

         t = t + "|" + ",".join(types)

         if name in currentScope[DECL]:
            if currentScope[DECL][name] != t:
               throwError(production)
         else:
            currentScope[DECL][name] = t
         
         return t, 1, name
         
   #Samo IDN
   else:
      # print(globalScopeNode)
      if name in currentScope[DECL] or t == VOID or t == "":
         throwError(production)
      
      currentScope[DECL][name] = t
      return t, 1, name

#INICIJALIZATOR# FINISHED - CRITICAL
def inicijalizator(): #Returns types
   genTreeInput.popleft()[0]

   if "<izraz_pridruzivanja>" == genTreeInput[0][0]:
      t, lval = izraz_pridruzivanja()

      if CHAR in t and ARRAY in t:
         return [CHAR] * lastCharArrayLen

      return [t]

   elif "L_VIT_ZAGRADA" in genTreeInput[0][0]:
      genTreeInput.popleft()[0]
      types = lista_izraza_pridruzivanja()
      genTreeInput.popleft()[0]
      return types

#LISTA IZRAZA PRIDRUZIVANJA# FINISHED
def lista_izraza_pridruzivanja(): #Returns list of types
   genTreeInput.popleft()[0]

   if "<izraz_pridruzivanja>" == genTreeInput[0][0]:
      return [izraz_pridruzivanja()[0]]

   elif "<lista_izraza_pridruzivanja>" == genTreeInput[0][0]:
      types = lista_izraza_pridruzivanja()
      genTreeInput.popleft()[0]
      return types + [izraz_pridruzivanja()[0]]

########################################################################################
#MAIN ##################################################################################
########################################################################################
def main():
   global genTreeInput
   for line in fileinput.input():
      line = line.rstrip("\n")
      size = len(line)
      line = line.strip(" ")
      size -= len(line)
      genTreeInput.append((line,size))

   prijevodna_jedinica()

   if "main" not in globalScopeNode[FUNCS]:
      print("main")

   elif not Util.allDeclared(globalScopeNode):
      print("funkcija")

if __name__ == "__main__":
   main()