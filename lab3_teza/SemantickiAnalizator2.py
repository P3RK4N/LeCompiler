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

genTreeInput = deque()

funcStack = []
loopStack = []

#Current scope
#scopeNode[PARENT] = scopeNodeParent if not global else None
#scopeNode[DECL] = dict of declarations
globalScopeNode = {
   PARENT : None,
   KIDS: [],
   FUNCS : dict(),
   DECL : dict(),
   SCOPE : dd(lambda : dd(None))
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
   production = genTreeInput.popleft() + " ::="

   if "IDN" in genTreeInput[0]:
      kros, line, val = genTreeInput.popleft().split(" ")
      production += Util.stringify1(kros,line,val)

      t, lval = Util.getDeclaredType(currentScope, val)

      if t == None:
         throwError(production)

      return t, lval

   elif "BROJ" in genTreeInput[0]:
      kros, line, val = genTreeInput.popleft().split(" ")
      production += Util.stringify1(kros,line,val)
      val = int(val)

      if val < -2**32 or val >= 2**32:
         throwError(production)
      
      return INT, False

   elif "NIZ_ZNAKOVA" in genTreeInput[0]:
      kros, line, val = genTreeInput.popleft().split(" ")
      production += Util.stringify1(kros, line, val)

      if val[0] != "\"" or val[-1] != "\"":
         throwError(production)
      else:   
         for pos in range(1,len(val)-1):
            if val[pos] == "\\" and (pos == len(val)-2 or not val[pos+1] in {'\\', "t", "n", "\"", "\'", "0"}):
               throwError(production)

      return CONST_CHAR_ARRAY, False

   elif "ZNAK" in genTreeInput[0]:
      kros, line, val = genTreeInput.popleft().split(" ")
      production += Util.stringify1(kros,line,val)

      if len(val) == 2:
         if val[0] != "\\" or not val[1] in {'\\', "t", "n", "\"", "\'", "0"}:
            throwError(production)
      else:
         if val[0] in {'\\', '\''}:
            throwError(production)

      return CHAR, False
   
   elif "L_ZAGRADA" in genTreeInput[0]:
      production += Util.stringify(genTreeInput.popleft())
      production += " <izraz>"
      t, lval = izraz()
      production += Util.stringify(genTreeInput.popleft())
      return t, lval

#POSTFIKS IZRAZ# FINISHED - CRITICAL
def postfiks_izraz(): #Returns type, lval
   #LHS production
   production = genTreeInput.popleft() + " ::="
   
   if "<primarni_izraz>" == genTreeInput[0]:
      return primarni_izraz()
   
   #Postfix izraz - dodaj u produkciju
   elif "<postfiks_izraz>" == genTreeInput[0]:
      production += " <postfiks_izraz>"
      postType, postLval = postfiks_izraz()

      #ARRAY ELEMENT
      #L UGL ZAGRADA - dodaj u produkciju, provjeri jel niz i jel tip izraza int
      if "L_UGL_ZAGRADA" in genTreeInput[0]:
         production += Util.stringify(genTreeInput.popleft())

         #IZRAZ - dodaj u produkciju
         production += " <izraz>"

         if not ARRAY in postType:
            production += Util.findOtherBracket(genTreeInput, "L_UGL_ZAGRADA", "D_UGL_ZAGRADA")
            throwError(production)

         izrazType, izrazLval = izraz()

         #D_UGL_ZAGRADA - dodaj u produkciju
         production += genTreeInput.popleft()

         if not izrazType in castDict[INT]:
            throwError(production)
         
         return postType.replace(" ARRAY", ""), not CONST in postType

      #INCREMENTIRANJE
      elif "OP_INC" in genTreeInput[0] or "OP_DEC" in genTreeInput[0]:
         production += Util.stringify(genTreeInput.popleft())

         if not postType in castDict[INT] or postLval == False:
            throwError(production) 
         
         return INT, False
      
      #FUNCTION CALL
      elif "L_ZAGRADA" in genTreeInput[0]:
         production += Util.stringify(genTreeInput.popleft())
         argsType = ""

         #Lista argumenata - dodaj u produkciju, provjeri jel su tipovi isti
         if "<lista_argumenata>" in genTreeInput[0]:
            production += " <lista_argumenata>"
            argsType = ",".join(lista_argumenata())

         #D ZAGRADA - dodaj u produkciju
         production += Util.stringify(genTreeInput.popleft())

         #Parametri ne pripadaju ovoj funkciji
         if "|" not in postType or postType.split("|")[1] != argsType:
            throwError(production)

         return postType.split("|")[0], False

#LISTA ARGUMENATA# FINISHED
def lista_argumenata(): #Returns list(types)
   genTreeInput.popleft()

   if "<izraz_pridruzivanja>" == genTreeInput[0]:
      return [izraz_pridruzivanja()[0]]

   elif "<lista_argumenata>" == genTreeInput[0]:
      types = lista_argumenata()
      #ZAREZ
      genTreeInput.popleft()
      return types + [izraz_pridruzivanja()[0]]

#UNARNI IZRAZ# FINISHED
#UNARNI OPERATOR# FINISHED
def unarni_izraz():
   #LHS production
   production = genTreeInput.popleft() + " ::="

   if "<postfiks_izraz>" == genTreeInput[0]:
      return postfiks_izraz()

   #Dodaj u produkciju i provjeri jel tip INT
   elif "OP_INC" in genTreeInput[0] or "OP_DEC" in genTreeInput[0]:
      #Operator
      production += Util.stringify(genTreeInput.popleft())

      #Unarni izraz
      production += " <unarni_izraz>"
      unarniType, unarniLval = unarni_izraz()

      if unarniLval == False or not unarniType in castDict[INT]:
         throwError(production)

      return INT, False

   elif "<unarni_operator>" == genTreeInput[0]:
      production += " <unarni_operator> <cast_izraz>"
      genTreeInput.popleft()
      genTreeInput.popleft()
      castType, castLval = cast_izraz()

      if not castType in castDict[INT]:
         throwError(production)

      return INT, False

#CAST IZRAZ# FINISHED
def cast_izraz(): #Returns type, lval
   #LHS production
   production = genTreeInput.popleft() + " ::="

   if "<unarni_izraz>" == genTreeInput[0]:
      return unarni_izraz()

   #Dodaj u produkciju, provjeri da se ovo moze eksplicitno castat
   elif "L_ZAGRADA" in genTreeInput[0]:
      #L ZAGRADA - dodaj u produkciju
      production += Util.stringify(genTreeInput.popleft())

      #IME TIPA - dodaj u produkciju
      production += " <ime_tipa>"
      imeType = ime_tipa()

      #D ZAGRADA - dodaj u produkciju
      production += Util.stringify(genTreeInput.popleft())

      #Cast izraz - dodaj u produkciju, provjeri jel moze convertat
      production += " <cast_izraz>"
      castType, castLval = cast_izraz()

      if not castType in castDict[imeType]:
         throwError(production)

      return imeType, False

#IME TIPA# - FINISHED
#SPECIFIKATOR TIPA# - FINISHED
def ime_tipa():
   #Dodaj lhs na produkciju
   production = genTreeInput.popleft() + " ::="

   isConst = False
   #KR CONST - dodaj na produkciju
   if "KR_CONST" in genTreeInput[0]:
      production += Util.stringify(genTreeInput.popleft())
      isConst = True
   
   #Specifikator tipa - dodaj na produkciju
   production += " " + genTreeInput.popleft()

   #Tip
   tip = genTreeInput.popleft().split(" ")[0][3:]

   if tip == VOID and isConst:
      throwError(production)

   return int(isConst)*"CONST " + tip

#IZRAZI# FINISHED
def operacijski_izrazi(top): #Returns type, lval
   #LHS production
   production = genTreeInput.popleft() + " ::="

   #Podizraz
   if izrazi[top] == genTreeInput[0]:
      if izrazi[top] != "<cast_izraz>":
         return operacijski_izrazi(izrazi[top])
      else:
         return cast_izraz()
      
   #Isti izraz - dodaj u produkciju
   elif top == genTreeInput[0]:
      topType, topLval = operacijski_izrazi(top)
      production += " " + top

      #Operator - dodaj u produkciju
      production += Util.stringify(genTreeInput.popleft())

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
   production = genTreeInput.popleft() + " ::="

   #LOG ILI IZRAZ
   if "<log_ili_izraz>" == genTreeInput[0]:
      return operacijski_izrazi("<log_ili_izraz>")
   
   #POSTFIKS IZRAZ - dodaj na produkciju
   elif "<postfiks_izraz>" == genTreeInput[0]:
      production += " <postfiks_izraz>"
      postfiksType, postfiksLval = postfiks_izraz()

      #OP PRIDRUZI - dodaj na produkciju
      production += Util.stringify(genTreeInput.popleft())

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
   genTreeInput.popleft()

   #Izraz
   if "<izraz>" == genTreeInput[0]:
      izraz()
      #Zarez
      genTreeInput.popleft()

   #Izraz pridruzivanja
   return izraz_pridruzivanja()[0], False


########################################################################################
#NAREDBENA STRUKTURA ###################################################################
########################################################################################

#SLOZENA NAREDBA# - FINISHED
def slozena_naredba():
   #LHS
   genTreeInput.popleft()

   #L_VIT_ZAGRADA
   genTreeInput.popleft()

   if "<lista_deklaracija>" == genTreeInput[0]:
      lista_deklaracija()

   lista_naredbi()

   #D_VIT_ZAGRADA
   genTreeInput.popleft()

#LISTA NAREDBI# - FINISHED
def lista_naredbi():
   genTreeInput.popleft()

   if "<lista_naredbi>" == genTreeInput[0]:
      lista_naredbi()

   naredba()

#NAREDBA#
def naredba():
   genTreeInput.popleft()
   
   if "<izraz_naredba>" == genTreeInput[0]:
      
      if "TOCKAZAREZ" in genTreeInput[0]:
         pass

      elif "<izraz>" == genTreeInput[0]:
         pass

   elif "<naredba_grananja>" == genTreeInput[0]:
      
      if "KR_ELSE" in genTreeInput[0]:
         pass

   elif "<naredba_petlje>" == genTreeInput[0]:

      if "KR_WHILE" in genTreeInput[0]:
         pass

      elif "KR_FOR" in genTreeInput[0]:
         
         if "<izraz>" == genTreeInput[0]:
            pass

   #Naredba skoka
   elif "<naredba_skoka>" == genTreeInput[0]:
      production = genTreeInput.popleft() + " ::="

      if "KR_CONTINUE" in genTreeInput[0] or "KR_BREAK" in genTreeInput[0]:
         pass #TODO: rjesi naredbu petlje

      #KR RETURN
      elif "KR_RETURN" in genTreeInput[0]:
         production += Util.stringify(genTreeInput.popleft())
         returnType = VOID

         #Izraz - dodaj na produkciju, stavi u returnType
         if "<izraz>" == genTreeInput[0]:
            production += " <izraz>"
            returnType = izraz()[0]

         #Tockazarez - dodaj na produkciju
         production += Util.stringify(genTreeInput.popleft())

         #Throw error ako nije isti povratni tip
         if not funcStack or Util.getFuncType(funcStack[-1], currentScope[PARENT]).split("|")[0] != returnType:
            throwError(production)

#PRIJEVODNA JEDINICA# - FINISHED
#VANJSKA DEKLARACIJA# - FINISHED
def prijevodna_jedinica():
   genTreeInput.popleft()

   if "<prijevodna_jedinica>" == genTreeInput[0]:
      prijevodna_jedinica()

   #Vanjska Deklaracija
   genTreeInput.popleft()

   if  "<definicija_funkcije>" == genTreeInput[0]:
      definicija_funkcije()

   elif "<deklaracija>" == genTreeInput[0]:
      deklaracija()

      
########################################################################################
#DEKLARACIJE I DEFINICIJE ##############################################################
########################################################################################

#DEFINICIJA FUNKCIJE#
def definicija_funkcije():
   global currentScope
   #Dodaj LHS na produkciju
   current = genTreeInput.popleft()
   production = current + " ::= " + "<ime_tipa>"
   error = False

   #Ime tipa - dohvati returnType i provjeri jel const
   returnType = ime_tipa()
   funcType = None
   error |= CONST in returnType

   #IDN - provjeri jel postoji definirana func s tim imenom, dodaj na produkciju
   idn, typeLine, funcName = genTreeInput.popleft().split(" ")
   production += Util.stringify1(idn, typeLine, funcName)
   error |= Util.functionExists(funcName, globalScopeNode)

   #L ZAGRADA - dodaj na produkciju
   production += Util.stringify(genTreeInput.popleft())

   types_names_params = None
   #KR VOID - dodaj na produkciju, dohvati paramType, ako deklarirana, mora bit isti tip, dodaj u scope
   if "KR_VOID" in genTreeInput[0]:
      production += Util.stringify(genTreeInput.popleft())
      funcType = returnType + "|"
      if funcName in globalScopeNode[DECL]:
         error |= globalScopeNode[DECL][funcName] != funcType
         del globalScopeNode[DECL][funcName]
      currentScope[FUNCS][funcName] = funcType
   
   #LISTA PARAMETARA - isto kao i KR VOID
   elif "<lista_parametara>" == genTreeInput[0]:
      production += " <lista_parametara>"
      if not error:
         types_names_params = lista_parametara() #TODO: stvori func type, provjeri deklaraciju, dodaj u scope
         pass

   #D ZAGRADA - dodaj na produkciju
   production += Util.stringify(genTreeInput.popleft())

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
         #TODO: Dodaj imena i tipove u novi scope
         pass

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

#LISTA PARAMETARA#
def lista_parametara():

   if "<deklaracija_parametra>" == genTreeInput[0]:
      pass

   elif "<lista_parametara>" == genTreeInput[0]:
      pass

#DEKLARACIJA PARAMETRA#
def deklaracija_parametra():

   if "L_UGL_ZAGRADA" in genTreeInput[0]:
      pass

#LISTA DEKLARACIJA#
def lista_deklaracija():

   if "<deklaracija>" == genTreeInput[0]:
      pass

   elif "<lista_deklaracija>" == genTreeInput[0]:
      pass

#DEKLARACIJA#
def deklaracija():

   pass

#LISTA INIT DEKLARATORA#
def lista_init_deklaratora():

   if "<init_deklarator>" == genTreeInput[0]:
      pass

   elif "<lista_init_deklaratora>" == genTreeInput[0]:
      pass

#INIT DEKLARATOR#
def init_deklarator():

   if "OP_PRIDRUZI" in genTreeInput[0]:
      pass

#IZRAVNI DEKLARATOR#
def izravni_deklarator():

   if "L_UGL_ZAGRADA" in genTreeInput[0]:
      pass

   elif "L_ZAGRADA" in genTreeInput[0]:
      
      if "KR_VOID" in genTreeInput[0]:
         pass

      elif "<lista_parametara>" == genTreeInput[0]:
         pass

#INICIJALIZATOR#
def inicijalizator():

   if "<izraz_pridruzivanja>" == genTreeInput[0]:
      pass

   elif "L_VIT_ZAGRADA" in genTreeInput[0]:
      pass

#LISTA IZRAZA PRIDRUZIVANJA#
def lista_izraza_pridruzivanja():

   if "<izraz_pridruzivanja>" == genTreeInput[0]:
      pass

   elif "<lista_izraza_pridruzivanja>" == genTreeInput[0]:
      pass


########################################################################################
#MAIN ##################################################################################
########################################################################################
def main():
   global genTreeInput
   for line in fileinput.input():
      genTreeInput.append(line.rstrip("\n").strip(" "))

   prijevodna_jedinica()

   if "main" not in globalScopeNode[FUNCS]:
      print("main")

   elif not Util.allDeclared(globalScopeNode):
      print("function")

if __name__ == "__main__":
   main()