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
loopStack = 0
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

#PRIMARNI IZRAZ# FINISHED REFACTORED
def primarni_izraz(): #Returns type, lval
   production = Util.getProduction(genTreeInput)
   genTreeInput.popleft()

   if "IDN" in genTreeInput[0][0]:
      _, _, val = genTreeInput.popleft()[0].split(" ")
      t, lval = Util.getDeclaredType(currentScope, val)
      if t == None:
         throwError(production)
      return t, lval

   elif "BROJ" in genTreeInput[0][0]:
      _, _, val = genTreeInput.popleft()[0].split(" ")
      val = int(val)
      if val < -2**32 or val >= 2**32:
         throwError(production)
      return INT, False

   elif "NIZ_ZNAKOVA" in genTreeInput[0][0]:
      _, _, val = genTreeInput.popleft()[0].split(" ")
      if not Util.isValidString(val):
         throwError(production)

      global lastCharArrayLen
      lastCharArrayLen = len(val) + 1 - len([c for c in val if c == "\\"]) - 2

      return CONST_CHAR_ARRAY, False

   elif "ZNAK" in genTreeInput[0][0]:
      _, _, val = genTreeInput.popleft()[0].split(" ")
      val = val[1:-1]

      if not Util.isValidChar(val):
         throwError(production)

      return CHAR, False
   
   elif "L_ZAGRADA" in genTreeInput[0][0]:
      genTreeInput.popleft()
      t, lval = izraz()
      genTreeInput.popleft()
      return t, lval

#POSTFIKS IZRAZ# FINISHED REFACTORED - CRITICAL
def postfiks_izraz(): #Returns type, lval
   production = Util.getProduction(genTreeInput)
   genTreeInput.popleft()
   
   if "<primarni_izraz>" == genTreeInput[0][0]:
      return primarni_izraz()
   
   #Postfix izraz - dodaj u produkciju
   elif "<postfiks_izraz>" == genTreeInput[0][0]:
      postType, postLval = postfiks_izraz()

      #ARRAY ELEMENT
      #L UGL ZAGRADA - provjeri jel niz i jel tip izraza int
      if "L_UGL_ZAGRADA" in genTreeInput[0][0]:
         genTreeInput.popleft()

         if not ARRAY in postType:
            throwError(production)

         izrazType, izrazLval = izraz()

         #D_UGL_ZAGRADA
         genTreeInput.popleft()

         if not izrazType in castDict[INT]:
            throwError(production)
         
         return postType.replace(" ARRAY", ""), not CONST in postType

      #INCREMENTIRANJE
      elif "OP_INC" in genTreeInput[0][0] or "OP_DEC" in genTreeInput[0][0]:
         genTreeInput.popleft()

         if not postType in castDict[INT] or postLval == False:
            throwError(production) 
         
         return INT, False
      
      #FUNCTION CALL
      elif "L_ZAGRADA" in genTreeInput[0][0]:
         genTreeInput.popleft()
         argsType = ""

         #Lista argumenata - dodaj u produkciju, provjeri jel su tipovi isti
         if "<lista_argumenata>" in genTreeInput[0][0]:
            argsType = ",".join(lista_argumenata())

         #D ZAGRADA
         genTreeInput.popleft()

         #Parametri ne pripadaju ovoj funkciji
         if "|" not in postType or postType.split("|")[1] != argsType:
            throwError(production)

         return postType.split("|")[0], False

#LISTA ARGUMENATA# FINISHED REFACTORED
def lista_argumenata(): #Returns list(types)
   genTreeInput.popleft()

   if "<izraz_pridruzivanja>" == genTreeInput[0][0]:
      return [izraz_pridruzivanja()[0]]

   elif "<lista_argumenata>" == genTreeInput[0][0]:
      types = lista_argumenata()
      #ZAREZ
      genTreeInput.popleft()[0]
      return types + [izraz_pridruzivanja()[0]]

#UNARNI IZRAZ# FINISHED REFACTORED
#UNARNI OPERATOR# FINISHED REFACTORED
def unarni_izraz():
   production = Util.getProduction(genTreeInput)
   genTreeInput.popleft()

   if "<postfiks_izraz>" == genTreeInput[0][0]:
      return postfiks_izraz()

   #Provjeri jel tip INT
   elif "OP_INC" in genTreeInput[0][0] or "OP_DEC" in genTreeInput[0][0]:
      #Operator
      genTreeInput.popleft()

      #Unarni izraz
      unarniType, unarniLval = unarni_izraz()

      if unarniLval == False or not unarniType in castDict[INT]:
         throwError(production)

      return INT, False

   elif "<unarni_operator>" == genTreeInput[0][0]:
      #Unarni operator
      genTreeInput.popleft()[0]
      #Cast izraz
      genTreeInput.popleft()[0]
      castType, castLval = cast_izraz()

      if not castType in castDict[INT]:
         throwError(production)

      return INT, False

#CAST IZRAZ# FINISHED REFACTORED
def cast_izraz(): #Returns type, lval
   production = Util.getProduction(genTreeInput)
   genTreeInput.popleft()

   if "<unarni_izraz>" == genTreeInput[0][0]:
      return unarni_izraz()

   #Provjeri da se ovo moze eksplicitno castat
   elif "L_ZAGRADA" in genTreeInput[0][0]:
      #L ZAGRADA
      genTreeInput.popleft()

      #IME TIPA
      imeType = ime_tipa()

      #D ZAGRADA
      genTreeInput.popleft()

      #Cast izraz - Provjeri jel moze convertat
      castType, castLval = cast_izraz()

      if not castType in castDict[imeType]:
         throwError(production)

      return imeType, False

#IME TIPA# - FINISHED REFACTORED
#SPECIFIKATOR TIPA# - FINISHED REFACTORED
def ime_tipa():
   production = Util.getProduction(genTreeInput)
   genTreeInput.popleft()

   isConst = False
   #KR CONST - dodaj na produkciju
   if "KR_CONST" in genTreeInput[0][0]:
      genTreeInput.popleft()
      isConst = True
   
   #Specifikator tipa
   genTreeInput.popleft()

   #Tip
   tip = genTreeInput.popleft()[0].split(" ")[0][3:]

   if tip == VOID and isConst:
      throwError(production)

   return int(isConst)*"CONST " + tip

#IZRAZI# FINISHED REFACTORED
def operacijski_izrazi(top): #Returns type, lval
   production = Util.getProduction(genTreeInput)
   genTreeInput.popleft()

   #Podizraz
   if izrazi[top] == genTreeInput[0][0]:
      if izrazi[top] != "<cast_izraz>":
         return operacijski_izrazi(izrazi[top])
      else:
         return cast_izraz()
      
   #Isti izraz - dodaj u produkciju
   elif top == genTreeInput[0][0]:
      topType, topLval = operacijski_izrazi(top)

      #Operator
      genTreeInput.popleft()[0]

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

#IZRAZ PRIDRUZIVANJA# FINISHED REFACTORED
def izraz_pridruzivanja(): #Returns type, lval
   production = Util.getProduction(genTreeInput)
   genTreeInput.popleft()

   #LOG ILI IZRAZ
   if "<log_ili_izraz>" == genTreeInput[0][0]:
      return operacijski_izrazi("<log_ili_izraz>")
   
   #POSTFIKS IZRAZ - dodaj na produkciju
   elif "<postfiks_izraz>" == genTreeInput[0][0]:
      postfiksType, postfiksLval = postfiks_izraz()

      #OP PRIDRUZI
      genTreeInput.popleft()

      #Izraz pridruzivanja - Ako je sve ispravno nastavi, inace baci gresku
      if postfiksLval == False:
         throwError(production)

      pridType, pridLval = izraz_pridruzivanja()

      if not postfiksType in castDict[pridType]:
         throwError(production)

      return postfiksType, False
   
#IZRAZ# FINISHED REFACTORED
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

#SLOZENA NAREDBA# - FINISHED REFACTORED
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

#LISTA NAREDBI# - FINISHED REFACTORED
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

#NAREDBA# FINISHED REFACTORED - CRITICAL CRITICAL
def naredba():
   global loopStack
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
      production = Util.getProduction(genTreeInput)
      genTreeInput.popleft()
      #IF
      genTreeInput.popleft()
      #L ZAGRADA
      genTreeInput.popleft()
      #IZRAZ
      t, _ = izraz()
      #D ZAGRADA
      genTreeInput.popleft()
      #NAREDBA
      if not t in castDict[INT]:
         throwError(production)
      else:
         naredba()
      #ELSE i NAREDBA
      if "KR_ELSE" in genTreeInput[0][0]:
         genTreeInput.popleft()
         naredba()

   elif "<naredba_petlje>" == genTreeInput[0][0]:
      production = Util.getProduction(genTreeInput)
      genTreeInput.popleft()

      if "KR_WHILE" in genTreeInput[0][0]:
         genTreeInput.popleft()
         #L ZAGRADA
         genTreeInput.popleft()
         #IZRAZ
         t, _ = izraz()
         #D ZAGRADA
         genTreeInput.popleft()

         if not t in castDict[INT]:
            throwError(production)

         loopStack += 1
         naredba()
         loopStack -= 1

      elif "KR_FOR" in genTreeInput[0][0]:
         genTreeInput.popleft()
         #L ZAGRADA
         genTreeInput.popleft()
         #IZRAZ NAREDBA 1 i 2
         izraz_naredba()
         t = izraz_naredba()

         if not t in castDict[INT]:
            throwError(production)

         if "<izraz>" == genTreeInput[0][0]:
            izraz()

         #D ZAGRADA         
         genTreeInput.popleft()

         loopStack += 1
         naredba()
         loopStack -= 1

   #Naredba skoka
   elif "<naredba_skoka>" == genTreeInput[0][0]:
      production = Util.getProduction(genTreeInput)
      genTreeInput.popleft()

      if "KR_CONTINUE" in genTreeInput[0][0] or "KR_BREAK" in genTreeInput[0][0]:
         genTreeInput.popleft()
         genTreeInput.popleft()
         
         if loopStack == 0:
            throwError(production)

      #KR RETURN
      elif "KR_RETURN" in genTreeInput[0][0]:
         genTreeInput.popleft()
         returnType = VOID
         #Izraz - dodaj na produkciju, stavi u returnType
         if "<izraz>" == genTreeInput[0][0]:
            returnType = izraz()[0]
         #Tockazarez
         genTreeInput.popleft()
         #Throw error ako nije isti povratni tip
         if not funcStack or Util.getFuncType(funcStack[-1], currentScope[PARENT]).split("|")[0] != returnType:
            throwError(production)
      
#PRIJEVODNA JEDINICA# - FINISHED REFACTORED
#VANJSKA DEKLARACIJA# - FINISHED REFACTORED
def prijevodna_jedinica():
   genTreeInput.popleft()

   if "<prijevodna_jedinica>" == genTreeInput[0][0]:
      prijevodna_jedinica()

   #Vanjska Deklaracija
   genTreeInput.popleft()

   if  "<definicija_funkcije>" == genTreeInput[0][0]:
      definicija_funkcije()

   elif "<deklaracija>" == genTreeInput[0][0]:
      deklaracija()

      
########################################################################################
#DEKLARACIJE I DEFINICIJE ##############################################################
########################################################################################

#DEFINICIJA FUNKCIJE# REFACTORED
def definicija_funkcije():
   global currentScope, globalScopeNode, funcStack

   production = Util.getProduction(genTreeInput)
   genTreeInput.popleft()

   #Ime tipa - dohvati returnType i provjeri jel const
   returnType = ime_tipa()
   funcType = None

   if CONST in returnType:
      throwError(production)

   #IDN - provjeri jel postoji definirana func s tim imenom
   idn, typeLine, funcName = genTreeInput.popleft()[0].split(" ")

   if Util.functionExists(funcName, globalScopeNode):
      throwError(production)

   #L ZAGRADA
   genTreeInput.popleft()

   types_names_params = None
   #KR VOID - dohvati paramType, ako deklarirana, mora bit isti tip, dodaj u scope
   if "KR_VOID" in genTreeInput[0][0]:
      genTreeInput.popleft()
      funcType = returnType + "|"
   
   #LISTA PARAMETARA - isto kao i KR VOID
   elif "<lista_parametara>" == genTreeInput[0][0]:
      types_names_params = lista_parametara()
      funcType = returnType + "|" + ",".join([tn[0] for tn in types_names_params])
      
   if funcName in globalScopeNode[DECL]:
      if globalScopeNode[DECL][funcName] != funcType:
         throwError(production)
      del globalScopeNode[DECL][funcName]
   globalScopeNode[FUNCS][funcName] = funcType

   #D ZAGRADA
   genTreeInput.popleft()

   #Slozena naredba - napravi novi scope i udi, dodaj function stack, dodaj parametre u scope, udji u slozenu funkciju, skini function stack, izadi iz scopea

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
   funcStack.append(funcName)
   #Slozena naredba
   slozena_naredba()
   #Skidanje sa stacka
   funcStack.pop()
   #Izlaz iz function scopea
   currentScope = currentScope[PARENT]

#LISTA PARAMETARA# FINISHED REFACTORED
def lista_parametara():
   production = Util.getProduction(genTreeInput)
   genTreeInput.popleft()
   types_names_list = []

   if "<lista_parametara>" == genTreeInput[0][0]:
      types_names_list.extend(lista_parametara())
      #ZAREZ
      genTreeInput.popleft()

   types_names_list.append(deklaracija_parametra())

   names = set()
   for tn in types_names_list:
      names.add(tn[1])

   if len(names) != len(types_names_list):
      throwError(production)

   return types_names_list

#DEKLARACIJA PARAMETRA# FINISHED REFACTORED
def deklaracija_parametra():
   production = Util.getProduction(genTreeInput)
   genTreeInput.popleft()

   t = ime_tipa()

   _, _, val = genTreeInput.popleft()[0].split(" ")

   if "L_UGL_ZAGRADA" in genTreeInput[0][0]:
      genTreeInput.popleft()
      genTreeInput.popleft()
      t = t + " " + ARRAY

   if VOID in t:
      throwError(production)

   return t, val

#LISTA DEKLARACIJA# FINISHED REFACTORED
def lista_deklaracija():
   genTreeInput.popleft()[0]

   if "<lista_deklaracija>" == genTreeInput[0][0]:
      lista_deklaracija()

   deklaracija()

#DEKLARACIJA# FINISHED REFACTORED
def deklaracija():
   genTreeInput.popleft()[0]
   t = ime_tipa()
   lista_init_deklaratora(t)
   genTreeInput.popleft()[0]

#LISTA INIT DEKLARATORA# FINISHED REFACTORED
def lista_init_deklaratora(t):
   genTreeInput.popleft()[0]

   if "<lista_init_deklaratora>" == genTreeInput[0][0]:
      lista_init_deklaratora(t)
      genTreeInput.popleft()[0]
   
   init_deklarator(t)

#INIT DEKLARATOR# FINISHED REFACTORED - CRITICAL
def init_deklarator(t):
   global currentScope
   production = Util.getProduction(genTreeInput)
   genTreeInput.popleft()

   #Izravni deklarator
   declType, declSize, declName = izravni_deklarator(t)

   #Operator - dodaj u produkciju
   if "OP_PRIDRUZI" in genTreeInput[0][0]:
      genTreeInput.popleft()   
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

#IZRAVNI DEKLARATOR# FINISHED REFACTORED - CRITICAL
def izravni_deklarator(t): #Returns type, size, name
   production = Util.getProduction(genTreeInput)
   genTreeInput.popleft()

   #IDN
   _, _, name = genTreeInput.popleft()[0].split(" ")
   
   if "L_UGL_ZAGRADA" in genTreeInput[0][0]:
      genTreeInput.popleft()
      #BROJ
      _, _, val = genTreeInput.popleft()[0].split(" ")
      val = int(val)
      if val < 1 or val > 1024 or t == VOID or name in currentScope[DECL]:
         throwError(production)
      #D UGL ZAGRADA
      genTreeInput.popleft()
      t = t + " " + ARRAY
      currentScope[DECL][name] = t
      return t, val, name

   elif "L_ZAGRADA" in genTreeInput[0][0]:
      genTreeInput.popleft()

      #Funkcija bez parametara
      if "KR_VOID" in genTreeInput[0][0]:
         genTreeInput.popleft()
         genTreeInput.popleft()
         t = t + "|"

         if name in currentScope[DECL]:
            if currentScope[DECL][name] != t:
               throwError(production)
         else:
            currentScope[DECL][name] = t
         
         return t, 1, name

      #Funkcija s parametrima
      elif "<lista_parametara>" == genTreeInput[0][0]:
         types_names_params = lista_parametara()
         types = [t for t,n in types_names_params]
         #D ZAGRADA
         genTreeInput.popleft()[0]
         t = t + "|" + ",".join(types)

         if name in currentScope[DECL]:
            if currentScope[DECL][name] != t:
               throwError(production)
         else:
            currentScope[DECL][name] = t
         
         return t, 1, name
         
   #Samo IDN
   else:
      if name in currentScope[DECL] or t == VOID:
         throwError(production)
      
      currentScope[DECL][name] = t
      return t, 1, name

#INICIJALIZATOR# FINISHED REFACTORED - CRITICAL
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

#LISTA IZRAZA PRIDRUZIVANJA# FINISHED REFACTORED
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