import fileinput
from collections import deque, defaultdict as dd

#DEBUGGING & ERRORS #######################################################################################
__DEBUG__ = False

__ERROR__ = False
__ERROR_INFO__ = None

PARENT = "PARENT"
KIDS = "KIDS"
SCOPE = "SCOPE"
TYPE = "TYPE"
NAME = "NAME"
FUNC = "FUNC"
DECL = "DECL"
LVAL = "LVAL"
INT = "INT"
CHAR = "CHAR"
ARR = "NIZ"
CONST = "CONST"
FUNC = "FUNC"
VOID = "VOID"

genTreeInput = deque()
prevGenTree = []
currentElement = []

#Current scope
#scopeNode[PARENT] = scopeNodeParent if not global else None
#scopeNode[DECL] = dict of declarations
globalScopeNode = {
   PARENT : None,
   KIDS: [],
   FUNC : None,
   DECL : dict(),
   SCOPE : dd(lambda : dd(None))
}
currentScope = globalScopeNode


castDict = {
   INT : {INT, INT + " " + CONST, CHAR, CHAR + " " + CONST},
   INT + " " + CONST : {INT, INT + " " + CONST, CHAR, CHAR + " " + CONST},

   CHAR : {INT, INT + " " + CONST, CHAR, CHAR + " " + CONST},
   CHAR + " " + CONST : {INT, INT + " " + CONST, CHAR, CHAR + " " + CONST}
}

def throwError(id = ""):
   global __ERROR__, __ERROR_INFO__
   __ERROR__ = True
   if not __ERROR_INFO__:
      __ERROR_INFO__ = "ERROR " + str(id) + " -> " + genTreeInput[0]

def throwErrorExact(e):
   global __ERROR__, __ERROR_INFO__
   __ERROR__ = True
   if not __ERROR_INFO__:
      __ERROR_INFO__ = e


###########################################################################################################
#PRIMITIVES ###############################################################################################
###########################################################################################################
   
#IDN ######################################################################################################
#IDN.ime je deklarirano
def IDN(info = None):
   if __ERROR__:
      return None, None, None
   
   global currentScope

   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, "IDN" in currentElement)

   idn, line, name = currentElement.split(" ")

   scope = currentScope
   while scope and not name in currentScope[SCOPE]:
      scope = scope[PARENT]

   #TYPE, LVAL, NAME
   if scope != None:
      return scope[SCOPE][name][TYPE], scope[SCOPE][name][LVAL], name
   else:
      return None, None, name

#BROJ ###################################################################################################
#BROJ.val je u rasponu int
def BROJ():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, "BROJ" in currentElement)

   br, line, value = currentElement.split(" ")
   value = int(value)

   #TYPE, LVAL, NAME
   return INT, False, value

#ZNAK ##################################################################################################
#Valid character
def ZNAK():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, "ZNAK" in currentElement)

   zn, line, value = currentElement.split(" ")

   #Validation---------
   if len(value) == 2:
      if value[0] != "\\" or not value[1] in {'\\', "t", "n", "\"", "\'", "0"}:
         throwError()
   else:
      if value[0] in {'\\', '\''}:
         throwError()
   #------------------
         
   #TYPE, LVAL, NAME
   return CHAR, False, value

#NIZ ZNAKOVA ############################################################################################
#Valid char array
def NIZ_ZNAKOVA(parent = None):
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, "NIZ_ZNAKOVA" in currentElement)

   niz_zn, line, value = currentElement.split(" ")

   #Validation----------------------------
   if value[0] != "\"" or value[-1] != "\"":
      throwError()
   else:   
      for pos in range(1,len(value)-1):
         if value[pos] == "\\" and (pos == len(value)-2 or not value[pos+1] in {'\\', "t", "n", "\"", "\'", "0"}):
            throwError()
   #---------------------------------------

   #TYPE, LVAL, NAME
   return ARR + " " + CHAR + " " + CONST, False, len(value)

#L_ZAGRADA ############################################################################################
def L_ZAGRADA():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "L_ZAGRADA")

   return None, None, None

#D_ZAGRADA ############################################################################################
def D_ZAGRADA():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "D_ZAGRADA")

   return None, None, None

#L_UGL_ZAGRADA ########################################################################################
def L_UGL_ZAGRADA():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "L_UGL_ZAGRADA")

   return None, None, None

#D_UGL_ZAGRADA ########################################################################################
def D_UGL_ZAGRADA():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "D_UGL_ZAGRADA")

   return None, None, None

#OP_INC ##############################################################################################
def OP_INC():
   if __ERROR__:
      return None, None, None

   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "OP_INC")

   return None, None, None

#OP_DEC ##############################################################################################
def OP_DEC():
   if __ERROR__:
      return None, None, None

   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "OP_DEC")

   return None, None, None

#ZAREZ ################################################################################################
def ZAREZ():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "ZAREZ")

   return None, None, None

#PLUS #################################################################################################
def PLUS():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "PLUS")

   return None, None, None

#MINUS #################################################################################################
def MINUS():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "MINUS")

   return None, None, None

#OP_TILDA #################################################################################################
def OP_TILDA():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "OP_TILDA")

   return None, None, None

#OP_NEG #################################################################################################
def OP_NEG():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "OP_NEG")

   return None, None, None

#KR_CONST ###############################################################################################
def KR_CONST():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "KR_CONST")

   return None, None, None

#KR_VOID ###############################################################################################
def KR_VOID():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "KR_VOID")

   return None, None, None

#KR_CHAR ###############################################################################################
def KR_CHAR():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "KR_CHAR")

   return None, None, None

#KR_INT ###############################################################################################
def KR_INT():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "KR_INT")

   return None, None, None

#OP_PUTA ###############################################################################################
def OP_PUTA():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "OP_PUTA")

   return None, None, None

#OP_DIJELI ###############################################################################################
def OP_DIJELI():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "OP_DIJELI")

   return None, None, None

#OP_MOD ###############################################################################################
def OP_MOD():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "OP_MOD")

   return None, None, None

#OP_LT ###############################################################################################
def OP_LT():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "OP_LT")

   return None, None, None

#OP_GT ###############################################################################################
def OP_GT():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "OP_GT")

   return None, None, None

#OP_LTE ###############################################################################################
def OP_LTE():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "OP_LTE")

   return None, None, None

#OP_GTE ###############################################################################################
def OP_GTE():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "OP_GTE")

   return None, None, None

#OP_EQ ###############################################################################################
def OP_EQ():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "OP_EQ")

   return None, None, None

#OP_NEQ ###############################################################################################
def OP_NEQ():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "OP_NEQ")

   return None, None, None

#OP_BIN_I ###############################################################################################
def OP_BIN_I():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "OP_BIN_I")

   return None, None, None

#OP_BIN_XILI ###############################################################################################
def OP_BIN_XILI():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "OP_BIN_XILI")

   return None, None, None

#OP_BIN_ILI ###############################################################################################
def OP_BIN_ILI():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "OP_BIN_ILI")

   return None, None, None

#OP_I ###############################################################################################
def OP_I():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "OP_I")

   return None, None, None

#OP_ILI ###############################################################################################
def OP_ILI():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "OP_ILI")

   return None, None, None

#OP_PRIDRUZI ###############################################################################################
def OP_PRIDRUZI():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "OP_PRIDRUZI")

   return None, None, None

#L_VIT_ZAGRADA ###############################################################################################
def L_VIT_ZAGRADA():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "L_VIT_ZAGRADA")

   return None, None, None

#D_VIT_ZAGRADA ###############################################################################################
def D_VIT_ZAGRADA():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "D_VIT_ZAGRADA")

   return None, None, None

#TOCKAZAREZ ###############################################################################################
def TOCKAZAREZ():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "TOCKAZAREZ")

   return None, None, None

#KR_IF ###############################################################################################
def KR_IF():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "KR_IF")

   return None, None, None

#KR_ELSE ###############################################################################################
def KR_ELSE():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "KR_ELSE")

   return None, None, None

#KR_WHILE ###############################################################################################
def KR_WHILE():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "KR_WHILE")

   return None, None, None

#KR_FOR ###############################################################################################
def KR_FOR():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "KR_FOR")

   return None, None, None

#KR_CONTINUE ###############################################################################################
def KR_CONTINUE():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "KR_CONTINUE")

   return None, None, None

#KR_BREAK ###############################################################################################
def KR_BREAK():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "KR_BREAK")

   return None, None, None

#KR_RETURN ###############################################################################################
def KR_RETURN():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement.split(" ")[0] == "KR_RETURN")

   return None, None, None

##########################################################################################################
#NON ENDINGS #############################################################################################
##########################################################################################################
      
#~PRIMARNI IZRAZ ###########################################################################################
def primarni_izraz_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("IDN")

   line = genTreeInput[0].split(" ")[1]

   t, lval, name = IDN()

   #Validation---------------------
   if t == None and lval == None:
      throwErrorExact("<primarni_izraz> ::= IDN(" + line + "," + name + ")")
   #-------------------------------
   return t, lval, name

def primarni_izraz_2():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("BROJ")

   line = genTreeInput[0].split(" ")[1]
   t, lval, value = BROJ()
   value = int(value)
   
   if value < -2**32 or value >= 2**32:
      throwErrorExact("<primarni_izraz> ::= BROJ(" + line + "," + value + ")")

   return t, lval, value

def primarni_izraz_3():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("ZNAK")

   return ZNAK()

def primarni_izraz_4():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("NIZ_ZNAKOVA")
   
   return NIZ_ZNAKOVA()

def primarni_izraz_5():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("L_ZAGRADA <izraz> D_ZAGRADA")

   L_ZAGRADA()
   t, lval, name = izraz()
   D_ZAGRADA()
   
   return t, lval, name

def primarni_izraz():
   if __ERROR__:
      return None, None, None

   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<primarni_izraz>")

   if "IDN" in genTreeInput[0]:
      return primarni_izraz_1()
   elif "BROJ" in genTreeInput[0]:
      return primarni_izraz_2()
   elif "NIZ_ZNAKOVA" in genTreeInput[0]:
      return primarni_izraz_4()
   elif "ZNAK" in genTreeInput[0]:
      return primarni_izraz_3()
   elif "L_ZAGRADA" in genTreeInput[0]:
      return primarni_izraz_5()
   else:
      throwError()
      return None, None, None   

#~POSTFIKS IZRAZ ###########################################################################################
def postfiks_izraz_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<primarni_izraz>")

   return primarni_izraz()

def postfiks_izraz_2_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<postfiks_izraz> L_UGL_ZAGRADA <izraz> D_UGL_ZAGRADA")
   
   L_UGL_ZAGRADA()
   
   t, lval, name = izraz()
   #Validation -----------------------------------
   if t != INT:
      throwError()
   #----------------------------------------------
      
   D_UGL_ZAGRADA()

   return None, None, None

def postfiks_izraz_2_2(funcType):
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("  <postfiks_izraz> L_ZAGRADA D_ZAGRADA")
      print("  <postfiks_izraz> L_ZAGRADA <lista_argumenata> D_ZAGRADA")
      
   L_ZAGRADA()

   #Funkcija bez parametara
   if genTreeInput[0] == "D_ZAGRADA":
      #Validation ---------------------------------
      if len(funcType.split("|")[1]) > 0:
         throwError()
      #--------------------------------------------
      D_ZAGRADA()

   #Funkcija s parametrima
   elif genTreeInput[0] == "<lista_argumenata>":
      paramsT = lista_argumenata()
      #Validation --------------------------------
      for i,param in funcType.split("|")[1].split(","):
         if param != paramsT[i]:
            throwError()
            break
      #-------------------------------------------
      D_ZAGRADA()

   else:
      throwError()

   return None, None, None
   
def postfiks_izraz_2():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("    <postfiks_izraz> L_UGL_ZAGRADA <izraz> D_UGL_ZAGRADA")
      print("    <postfiks_izraz> L_ZAGRADA D_ZAGRADA")
      print("    <postfiks_izraz> L_ZAGRADA <lista_argumenata> D_ZAGRADA")
      print("    <postfiks_izraz> OP_INC")
      print("    <postfiks_izraz> OP_DEC")

   t, lval, name = postfiks_izraz()
   
   #Adresiranje niza
   if "L_UGL_ZAGRADA" in genTreeInput[0]:
      #Validation ---------------------------------
      if not ARR in t:
         throwError()
      #--------------------------------------------
      t = t.replace(ARR, "").strip(" ")
      lval = not CONST in t
      postfiks_izraz_2_1()

   #Poziv funkcije
   elif "L_ZAGRADA" in genTreeInput[0]:
      #Validation --------------------------------
      if t and not "|" in t:
         throwError()
      #-------------------------------------------
      postfiks_izraz_2_2(t)

   #Increment operator
   elif "OP_INC" in genTreeInput[0]:
      #Validation -------------------------------
      if lval != True or t != INT:
         throwError()
      #------------------------------------------
      lval = False
      return OP_INC()

   #Decrement operator
   elif "OP_DEC" in genTreeInput[0]:
      #Validation -------------------------------
      if lval != True or t != INT:
         throwError()
      #------------------------------------------
      lval = False
      return OP_DEC()

   else:
      throwError()
   
   return t, lval, name

def postfiks_izraz():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print("<postfiks_izraz>", currentElement == "<postfiks_izraz>")
   
   if "<primarni_izraz>" == genTreeInput[0]:
      return postfiks_izraz_1()
   elif "<postfiks_izraz>" == genTreeInput[0]:
      return postfiks_izraz_2()
   else:
      throwError()
   
   return None, None, None

#~LISTA ARGUMENATA #########################################################################################
def lista_argumenata_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<izraz_pridruzivanja>")

   t, lval, name = izraz_pridruzivanja()
   return [t]

def lista_argumenata_2():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<lista_argumenata> ZAREZ <izraz_pridruzivanja>")

   paramsT = lista_argumenata()
   ZAREZ()
   t, lval, name = izraz_pridruzivanja()
   return [t] + paramsT

#Returns array of types
def lista_argumenata():
   if __ERROR__:
      return None, None, None

   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<lista_argumenata>")

   if "<izraz_pridruzivanja>" == genTreeInput[0]:
      return lista_argumenata_1()

   elif "<lista_argumenata>" == genTreeInput[0]:
      return lista_argumenata_2()

   else:
      throwError()

   return []

#~UNARNI IZRAZ #############################################################################################
def unarni_izraz_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<postfiks_izraz>")

   return postfiks_izraz()

def unarni_izraz_2():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("OP_INC")

   OP_INC()

   t, lval, name = unarni_izraz()
   #Validation ----------------------
   if not lval or t != INT:
      throwError()
   #---------------------------------

   return t, lval, name

def unarni_izraz_3():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("OP_DEC")

   OP_DEC()
   t, lval, name = unarni_izraz()
   #Validation -----------------------
   if not lval or t != INT:
      throwError()
   #----------------------------------
   return t, lval, name

def unarni_izraz_4():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<unarni_operator> <cast_izraz>")

   unarni_operator()
   
   t, lval, name = cast_izraz()
   #Validation --------------------------
   if t != INT:
      throwError()
   #-------------------------------------
   return INT, False, name

def unarni_izraz():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<unarni_izraz>")

   if "<postfiks_izraz>" == genTreeInput[0]:
      return unarni_izraz_1()

   elif "OP_INC" in genTreeInput[0]:
      return unarni_izraz_2()

   elif "OP_DEC" in genTreeInput[0]:
      return unarni_izraz_3()

   elif "<unarni_operator>" == genTreeInput[0]:
      return unarni_izraz_4()

   else:
      throwError()

   return None, None, None

#~UNARNI OPERATOR
def unarni_operator():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<unarni_operator>")

   if "PLUS" in genTreeInput[0]:
      PLUS()
   elif "MINUS" in genTreeInput[0]:
      MINUS()
   elif "OP_TILDA" in genTreeInput[0]:
      OP_TILDA()
   elif "OP_NEG" in genTreeInput[0]:
      OP_NEG()
   else:
      throwError()

   return None, None, None

#~CAST IZRAZ ###############################################################################################
def cast_izraz_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<unarni_izraz>")

   return unarni_izraz()

def cast_izraz_2():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("L_ZAGRADA <ime_tipa> D_ZAGRADA <cast_izraz>")

   L_ZAGRADA()

   t = ime_tipa()

   D_ZAGRADA()

   castT, castLval, castName = cast_izraz()
   #Validation---------------------------------
   if not ((t in {CHAR, CHAR + " " + CONST} and castT in {INT, INT + " " + CONST}) or (castT in {CHAR, CHAR + " " + CONST} and t in {INT, INT + " " + CONST})):
      throwError()
   #-------------------------------------------

   return t, 0, castName
      
def cast_izraz():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<cast_izraz>")

   if "<unarni_izraz>" == genTreeInput[0]:
      return cast_izraz_1()
   elif "L_ZAGRADA" in genTreeInput[0]:
      return cast_izraz_2()
   else:
      throwError()

   return None, None, None

#~IME TIPA #################################################################################################
def ime_tipa_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<specifikator_tipa>")

   return specifikator_tipa()

def ime_tipa_2():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("KR_CONST <specifikator_tipa>")

   KR_CONST()

   t = specifikator_tipa()

   #Validation --------------------------------------
   if t == VOID:
      throwError()
   #--------------------------------------------------

   return t + " " + CONST

def ime_tipa():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<ime_tipa>")

   if "<specifikator_tipa>" == genTreeInput[0]:
      return ime_tipa_1()

   elif "KR_CONST" in genTreeInput[0]:
      return ime_tipa_2()

   else:
      throwError()

   return None

#~SPECIFIKATOR TIPA ########################################################################################
def specifikator_tipa_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("KR_VOID")

   KR_VOID()

   return VOID

def specifikator_tipa_2():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("KR_CHAR")

   KR_CHAR()

   return CHAR

def specifikator_tipa_3():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("KR_INT")

   KR_INT()

   return INT

def specifikator_tipa():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<specifikator_tipa>")

   if "KR_VOID" in genTreeInput[0]:
      return specifikator_tipa_1()

   elif "KR_CHAR" in genTreeInput[0]:
      return specifikator_tipa_2()

   elif "KR_INT" in genTreeInput[0]:
      return specifikator_tipa_3()

   else:
      throwError()

   return None

#~MULTIPLIKATIVNI IZRAZ ####################################################################################
def multiplikativni_izraz_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<cast_izraz>")

   return cast_izraz()

def multiplikativni_izraz_2():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<multiplikativni_izraz> (OP_PUTA | OP_DIJELI | OP_MOD) <cast_izraz>")
   
   t, lval, name = multiplikativni_izraz()

   #Validation -----------------------------------------
   if t != INT and t != (INT + " " + CONST):
      throwError()
   #----------------------------------------------------

   if "OP_PUTA" in genTreeInput[0]:
      OP_PUTA()
   elif "OP_DIJELI" in genTreeInput[0]:
      OP_DIJELI()
   elif "OP_MOD" in genTreeInput[0]:
      OP_MOD()
   else:
      throwError()

   castT, castLval, castName = cast_izraz()

   #Validation----------------------------------------
   if castT != INT and castT != (INT + " " + CONST):
      throwError()
   #--------------------------------------------------
   return INT, 0, None
      
def multiplikativni_izraz():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<multiplikativni_izraz>")

   if "<cast_izraz>" == genTreeInput[0]:
      return multiplikativni_izraz_1()

   elif "<multiplikativni_izraz>" == genTreeInput[0]:
      return multiplikativni_izraz_2()

   else:
      throwError()

   return None, None, None

#~ADITIVNI IZRAZ ###########################################################################################
def aditivni_izraz_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<multiplikativni_izraz>")

   return multiplikativni_izraz()

def aditivni_izraz_2():
   if __ERROR__:
      return None, None, None 
   if __DEBUG__:
      print("<aditivni_izraz> (PLUS | MINUS) <multiplikativni_izraz>")
   
   addT, addLval, addName = aditivni_izraz()
   #Validation---------------------------------------------
   if addT != INT and addT != INT + " " + CONST:
      throwError()
   #-------------------------------------------------------

   mulT, mulLval, mulName = multiplikativni_izraz()
   #Validation---------------------------------------------
   if mulT != INT and mulT != INT + " " + CONST:
      throwError()
   #-------------------------------------------------------

   return INT, False, None
   
def aditivni_izraz():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<aditivni_izraz>")

   if "<multiplikativni_izraz>" == genTreeInput[0]:
      return aditivni_izraz_1()

   elif "<aditivni_izraz>" == genTreeInput[0]:
      return aditivni_izraz_2()

   else:
      throwError()

   return None, None, None

#~ODNOSNI IZRAZ ############################################################################################
def odnosni_izraz_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<aditivni_izraz>")

   return aditivni_izraz()

def odnosni_izraz_2():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<odnosni_izraz> (OP_LT | OP_GT | OP_LTE | OP_GTE) <aditivni_izraz>")

   t, lval, name = odnosni_izraz()

   #Validation---------------------------------------------
   if t != INT and t != INT + " " + CONST:
      throwError()
   #-------------------------------------------------------

   if "OP_LTE" in genTreeInput[0]:
      OP_LTE()
   elif "OP_LT" in genTreeInput[0]:
      OP_LT()
   elif "OP_GTE" in genTreeInput[0]:
      OP_GTE()
   elif "OP_GT" in genTreeInput[0]:
      OP_GT()
   else:
      throwError("(Odnosni operator ne postoji)")
   
   addT, addLval, addName = aditivni_izraz()

   #Validation---------------------------------------------
   if addT != INT and addT != INT + " " + CONST:
      throwError()
   #-------------------------------------------------------

   return INT, False, None


def odnosni_izraz():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<odnosni_izraz>")

   if "<aditivni_izraz>" == genTreeInput[0]:
      return odnosni_izraz_1()

   elif "<odnosni_izraz>" == genTreeInput[0]:
      return odnosni_izraz_2()

   else:
      throwError()

   return None, None, None

#~JEDNAKOSNI IZRAZ #########################################################################################
def jednakosni_izraz_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<odnosni_izraz>")
   
   return odnosni_izraz()

def jednakosni_izraz_2():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<jednakosni_izraz> (OP_EQ | OP_NEQ) <odnosni_izraz>")

   jednT, jednLval, jednName = jednakosni_izraz()

   #Validation---------------------------------------------
   if jednT != INT and jednT != INT + " " + CONST:
      throwError()
   #-------------------------------------------------------

   if "OP_EQ" in genTreeInput[0]:
      OP_EQ()
   elif "OP_NEQ" in genTreeInput[0]:
      OP_NEQ()

   odnT, odnLval, odnName = odnosni_izraz()

   #Validation---------------------------------------------
   if odnT != INT and odnT != INT + " " + CONST:
      throwError()
   #-------------------------------------------------------

   return INT, False, None
      
def jednakosni_izraz():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<jednakosni_izraz>")

   if "<odnosni_izraz>" == genTreeInput[0]:
      return jednakosni_izraz_1()

   elif "<jednakosni_izraz>" == genTreeInput[0]:
      return jednakosni_izraz_2()

   else:
      throwError()

   return None, None, None

#~BIN I IZRAZ ##############################################################################################
def bin_i_izraz_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<jednakosni_izraz>")

   return jednakosni_izraz()

def bin_i_izraz_2():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<bin_i_izraz> OP_BIN_I <jednakosni_izraz>")

   binT, binLval, binName = bin_i_izraz()

   #Validation---------------------------------------------
   if binT != INT and binT != INT + " " + CONST:
      throwError()
   #-------------------------------------------------------

   OP_BIN_I()

   jednT, jednLval, jednName = jednakosni_izraz()

   #Validation---------------------------------------------
   if jednT != INT and jednT != INT + " " + CONST:
      throwError()
   #-------------------------------------------------------

   return INT, False, None

def bin_i_izraz():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<bin_i_izraz>")

   if "<jednakosni_izraz>" in genTreeInput[0]:
      return bin_i_izraz_1()

   elif "<bin_i_izraz>" in genTreeInput[0]:
      return bin_i_izraz_2()

   else:
      throwError()

   return None, None, None

#~BIN XILI IZRAZ ##############################################################################################
def bin_xili_izraz_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<bin_i_izraz>")

   return bin_i_izraz()

def bin_xili_izraz_2():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<bin_xili_izraz> OP_BIN_XILI <bin_i_izraz>")

   xT, xLval, xName = bin_xili_izraz()

   #Validation---------------------------------------------
   if xT != INT and xT != INT + " " + CONST:
      throwError()
   #-------------------------------------------------------

   OP_BIN_XILI()

   iT, iLval, iName = bin_i_izraz()

   #Validation---------------------------------------------
   if iT != INT and iT != INT + " " + CONST:
      throwError()
   #-------------------------------------------------------

   return INT, False, None

def bin_xili_izraz():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<bin_xili_izraz>")

   if "<bin_i_izraz>" in genTreeInput[0]:
      return bin_xili_izraz_1()

   elif "<bin_xili_izraz>" in genTreeInput[0]:
      return bin_xili_izraz_2()

   else:
      throwError()

   return None, None, None

#~BIN ILI IZRAZ ############################################################################################
def bin_ili_izraz_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<bin_xili_izraz>")

   return bin_xili_izraz()

def bin_ili_izraz_2():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<bin_ili_izraz> OP_BIN_ILI <bin_xili_izraz>")

   iliT, iliLval, iliName = bin_ili_izraz()

   #Validation---------------------------------------------
   if iliT != INT and iliT != INT + " " + CONST:
      throwError()
   #-------------------------------------------------------

   OP_BIN_ILI()

   xiliT, xiliLval, xiliName = bin_xili_izraz()

   #Validation---------------------------------------------
   if xiliT != INT and xiliT != INT + " " + CONST:
      throwError()
   #-------------------------------------------------------

   return INT, False, None

def bin_ili_izraz():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<bin_ili_izraz>")

   if "<bin_xili_izraz>" in genTreeInput[0]:
      return bin_ili_izraz_1()

   elif "<bin_ili_izraz>" in genTreeInput[0]:
      return bin_ili_izraz_2()

   else:
      throwError()

   return None, None, None

#~LOG I IZRAZ ##############################################################################################
def log_i_izraz_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<bin_ili_izraz>")

   return bin_ili_izraz()

def log_i_izraz_2():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<log_i_izraz> OP_LOG_I <bin_ili_izraz>")

   iT, iLval, iName = log_i_izraz()

   #Validation---------------------------------------------
   if iT != INT and iT != INT + " " + CONST:
      throwError()
   #-------------------------------------------------------

   OP_I()

   iliT, iliLval, iliName = bin_ili_izraz()

   #Validation---------------------------------------------
   if iliT != INT and iliT != INT + " " + CONST:
      throwError()
   #-------------------------------------------------------

   return INT, False, None

def log_i_izraz():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<log_i_izraz>")

   if "<bin_ili_izraz>" in genTreeInput[0]:
      return log_i_izraz_1()

   elif "<log_i_izraz>" in genTreeInput[0]:
      return log_i_izraz_2()

   else:
      throwError()

   return None, None, None

#~LOG ILI IZRAZ ############################################################################################
def log_ili_izraz_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<log_i_izraz>")

   return log_i_izraz()

def log_ili_izraz_2():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<log_ili_izraz> OP_LOG_ILI <log_i_izraz>")

   iliT, iliLval, iliName = log_ili_izraz()

   #Validation---------------------------------------------
   if iliT != INT and iliT != INT + " " + CONST:
      throwError()
   #-------------------------------------------------------

   OP_ILI()

   iT, iLval, iName = log_i_izraz()

   #Validation---------------------------------------------
   if iT != INT and iT != INT + " " + CONST:
      throwError()
   #-------------------------------------------------------

   return INT, False, None

def log_ili_izraz():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<log_ili_izraz>")

   if "<log_i_izraz>" in genTreeInput[0]:
      return log_ili_izraz_1()

   elif "<log_ili_izraz>" in genTreeInput[0]:
      return log_ili_izraz_2()

   else:
      throwError()

   return None, None, None

#~IZRAZ PRIDRUZIVANJA ######################################################################################
def izraz_pridruzivanja_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<log_ili_izraz>")

   return log_ili_izraz()

def izraz_pridruzivanja_2():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<postfiks_izraz> OP_PRIDRUZI <izraz_pridruzivanja>")

   postT, postLval, postName = postfiks_izraz()

   #Validation---------------------------------------------
   if postLval == False:
      throwError()
   #-------------------------------------------------------

   OP_PRIDRUZI()

   pridT, pridLval, pridName = izraz_pridruzivanja()

   #Validation---------------------------------------------
   if pridT != postT and pridT != postT + " " + CONST:
      throwError() 
   #-------------------------------------------------------

   return postT, False, None

def izraz_pridruzivanja():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<izraz_pridruzivanja>")

   if "<log_ili_izraz>" == genTreeInput[0]:
      return izraz_pridruzivanja_1()

   elif "<postfix_izraz>" == genTreeInput[0]:
      return izraz_pridruzivanja_2()

   else:
      throwError()

   return None, None, None

#~IZRAZ ####################################################################################################
def izraz_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<izraz_pridruzivanja>")

   return izraz_pridruzivanja()

def izraz_2():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<izraz> ZAREZ <izraz_pridruzivanja>")

   izraz()

   return izraz_pridruzivanja()[0], False, None

def izraz():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<izraz>")

   if "<izraz_pridruzivanja>" == genTreeInput[0]:
      return izraz_1()
   
   elif "<izraz>" == genTreeInput[0]:
      return izraz_2()
   
   else:
      throwError()

   return None, None, None

############################################################################################################
#NAREDBENA STRUKTURA #######################################################################################
############################################################################################################

#~SLOZENA NAREDBA ##########################################################################################
def slozena_naredba_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print(" L_VIT_ZAGRADA <lista_naredbi> D_VIT_ZAGRADA")

   lista_naredbi()

   D_VIT_ZAGRADA()

   return None, None, None

def slozena_naredba_2():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("L_VIT_ZAGRADA <lista_deklaracija> <lista_naredbi> D_VIT_ZAGRADA")

   lista_deklaracija()

   lista_naredbi()

   D_VIT_ZAGRADA()

   return None, None, None

def slozena_naredba():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<slozena_naredba>")

   L_VIT_ZAGRADA()

   if "<lista_naredbi>" == genTreeInput[0]:
      slozena_naredba_1()

   elif "<lista_deklaracija>" == genTreeInput[0]:
      slozena_naredba_2()

   return None, None, None

#~LISTA NAREDBI ############################################################################################
def lista_naredbi_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<naredba>")

   naredba()

   return None, None, None

def lista_naredbi_2():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<lista_naredbi> <naredba>")

   lista_naredbi()

   naredba()

   return None, None, None

def lista_naredbi():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<lista_naredbi>")

   if "<naredba>" == genTreeInput[0]:
      lista_naredbi_1()

   elif "<lista_naredbi>" == genTreeInput:
      lista_naredbi_2()

   else:
      throwError()
   
   return None, None, None
   
#~NAREDBA #################################################################################################
def naredba():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<naredba>")

   if "<slozena_naredba>" == genTreeInput[0]:
      slozena_naredba()
   
   elif "<izraz_naredba>" == genTreeInput[0]:
      izraz_naredba()

   elif "<naredba_grananja>" == genTreeInput[0]:
      naredba_grananja()

   elif "<naredba_petlje>" == genTreeInput[0]:
      naredba_petlje()

   elif "<naredba_skoka>" == genTreeInput[0]:
      naredba_skoka()

   else:
      throwError()
   
   return None, None, None

#~IZRAZ NAREDBA ############################################################################################
def izraz_naredba_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<izraz> TOCKAZAREZ")

   t, lval, name = izraz()

   TOCKAZAREZ()

   return t, lval, name

def izraz_naredba():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<izraz_naredba>")

   if "TOCKAZAREZ" in genTreeInput[0]:
      TOCKAZAREZ()
      return INT, False, None
   
   elif "<izraz>" == genTreeInput[0]:
      return izraz_naredba_1() 

   return 

#~NAREDBA GRANANJA #########################################################################################
def naredba_grananja():
   if __ERROR__:
      return None, None, None

   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<naredba_grananja>")

   KR_IF()

   L_ZAGRADA()

   t, lval, name = izraz()
   #Validation -----------------------------
   if t != INT:
      throwError()
   #----------------------------------------

   D_ZAGRADA()

   naredba()

   if "KR_ELSE" != genTreeInput[0]:
      return None, None, None

   KR_ELSE()

   naredba()

#~NAREDBA PETLJE ###########################################################################################
def naredba_petlje_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("KR_WHILE L_ZAGRADA <izraz> D_ZAGRADA <naredba>")
   
   KR_WHILE()

   L_ZAGRADA()

   t, lval, name = izraz()
   #Validation --------------------------
   if t != INT and t != INT + " " + CONST:
      throwError()
   #-------------------------------------
   
   D_ZAGRADA()

   naredba()

   return None, None, None

def naredba_petlje_2():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("KR_FOR L_ZAGRADA <izraz_naredba> <izraz_naredba> D_ZAGRADA <naredba>")
      print(" KR_FOR L_ZAGRADA <izraz_naredba> <izraz_naredba> <izraz> D_ZAGRADA <naredba>")

   KR_FOR()

   L_ZAGRADA()

   izraz_naredba()

   t, lval, name = izraz_naredba()
   #Validation --------------------------
   if t != INT and t != INT + " " + CONST:
      throwError()
   #-------------------------------------

   D_ZAGRADA()

   if "<naredba>" != genTreeInput[0]:
      return None, None, None

   naredba()
   return None, None, None


def naredba_petlje():
   if __ERROR__:
      return None, None, None

   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print("<naredba_petlje>")

   if "KR_WHILE" == genTreeInput[0]:
      naredba_petlje_1()

   elif "KR_FOR" == genTreeInput[0]:
      naredba_petlje_2()

   return None, None, None

#~NAREDBA SKOKA ############################################################################################
def naredba_skoka():
   if __ERROR__:
      return None, None, None
   
   global currentScope

   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<naredba_skoka>")

   if "KR_CONTINUE" in genTreeInput[0]:
      KR_CONTINUE()
      TOCKAZAREZ()
      return None, None, None

   elif "KR_BREAK" in genTreeInput[0]:
      KR_BREAK()
      TOCKAZAREZ()
      return None, None, None
   
   elif "KR_RETURN" in genTreeInput[0]:
      KR_RETURN()

   else:
      throwError("(Nepoznata keyword skoka)")

   #Validation ------------------------
   if currentScope[FUNC] == None:
      throwError()
      return None, None, None
   #-----------------------------------

   if "TOCKAZAREZ" in genTreeInput[0]:
      #Validation---------------------
      if currentScope[FUNC].split("|")[0] != VOID:
         throwError()
      #-------------------------------
      TOCKAZAREZ()

   elif "<izraz>" == genTreeInput[0]:
      t, lval, name = izraz()
      #Validation -------------------
      if t != currentScope[FUNC].split("|")[0]:
         throwError()
      #------------------------------
      TOCKAZAREZ()
   
   return None, None, None

#~PRIJEVODNA JEDINICA ######################################################################################
def prijevodna_jedinica_1():
   if __ERROR__:
      return None, None, None   
   if __DEBUG__:
      print("<vanjska_deklaracija>")

   vanjska_deklaracija()
   return None, None, None

def prijevodna_jedinica_2():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<prijevodna_jedinica> <vanjska_deklaracija>")

   prijevodna_jedinica()
   vanjska_deklaracija()
   return None, None, None

def prijevodna_jedinica():
   if __ERROR__:
      return None, None, None

   currentElement = genTreeInput.popleft()   
   if __DEBUG__:
      print("<prijevodna_jedinica>", currentElement == "<prijevodna_jedinica>")


   if genTreeInput[0] == "<prijevodna_jedinica>":
      prijevodna_jedinica_2()
   elif genTreeInput[0] == "<vanjska_deklaracija>":
      prijevodna_jedinica_1()
   else:
      throwError()
      
   return None, None, None

      
#~VANJSKA DEKLARACIJA ######################################################################################
def vanjska_deklaracija():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<vanjska_deklaracija>")

   if "<definicija_funkcije>" == genTreeInput[0]:
      definicija_funkcije()
   
   elif "<deklaracija>" == genTreeInput[0]:
      deklaracija()

   else:
      throwError()

   return None, None, None

###########################################################################################################
#DEKLARACIJE I DEFINICIJE #################################################################################
###########################################################################################################

#~DEFINICIJA FUNKCIJE #####################################################################################
def definicija_funkcije():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<definicija_funkcije>")

   global currentScope

   t = ime_tipa()

   #Validation -------------------------------------
   if CONST in t:
      throwError("(Funkcija nije CONST)")
   #------------------------------------------------

   funcType, funcLval, funcName = IDN()

   #Validation -------------------------------------
   tmpScope = currentScope
   while tmpScope != None:
      if funcName in tmpScope[SCOPE] and tmpScope[SCOPE][funcName][0] == FUNC:
         throwError("(Funkcija vec postoji)")
         break
      tmpScope = tmpScope[PARENT]
   #------------------------------------------------

   L_ZAGRADA()

   params = None

   if "KR_VOID" in genTreeInput[0]:
      KR_VOID()
      funcType = t + "|" + VOID

   elif "<lista_parametara>" == genTreeInput[0]:
      params = lista_parametara()
      funcType = t + "|" + ",".join(params[0])
   
   else:
      throwError()

   #Validation -------------------------------------
   if funcName in globalScopeNode[DECL]:
      if funcType.split("|")[0] != globalScopeNode[DECL].split("|")[0]:
         throwError()
      elif funcType.split("|")[1].split(",") != globalScopeNode[DECL].split("|")[1].split(","):
         throwError()
   #------------------------------------------------

   currentScope[SCOPE][funcName][TYPE] = funcType

   if funcName in globalScopeNode[DECL]:
      del globalScopeNode[DECL][funcName]

   D_ZAGRADA()

   newNode = {
      PARENT : currentScope,
      KIDS : [],
      FUNC : funcName,
      DECL : dict(),
      SCOPE : dd(lambda : dd(None))
   }

   currentScope[KIDS].append(newNode)
   currentScope = newNode

   if params:
      for i in range(len(params[0])):
         currentScope[SCOPE][params[1][i]][TYPE] = params[0][i]
         currentScope[SCOPE][params[1][i]][LVAL] = not CONST in params[0][i]

   slozena_naredba()

   currentScope = newNode[PARENT]

   return None, None, None

#~LISTA PARAMETARA #####################################################################################
def lista_parametara_1():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<deklaracija_parametra>")

   t, lval, name = deklaracija_parametra()

   return [[t],[name]]

def lista_parametara_2():
   if __ERROR__:
      return None, None, None
   if __DEBUG__:
      print("<lista_parametara> ZAREZ <deklaracija_parametra>")

   types_names_params = lista_parametara()

   ZAREZ()

   t, lval, name = deklaracija_parametra()

   #Validation -------------------------------
   if name in types_names_params[1]:
      throwError()
   #------------------------------------------

   types_names_params[0].append(t)
   types_names_params[1].append(name)
   return types_names_params


def lista_parametara():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<lista_parametara>")

   if "<deklaracija_parametara>" == genTreeInput[0]:
      return lista_parametara_1()
   
   elif "<lista_parametara>" == genTreeInput[0]:
      return lista_parametara_2()
   
   else:
      throwError()

   return [[],[]]

#~DEKLARACIJA PARAMETRA ###################################################################################
def deklaracija_parametra():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<deklaracija_parametra>")

   t = ime_tipa()

   #Validation ------------------------------------
   if t == VOID:
      throwError()
   #-----------------------------------------------

   _, _, name = IDN()

   if not "L_UGLATA_ZAGRADA" in genTreeInput[0]:
      return t, False, name
   
   L_UGL_ZAGRADA()

   D_UGL_ZAGRADA()

   t = ARR + " " + t

   return t, False, name

#~LISTA DEKLARACIJA #######################################################################################
def lista_deklaracija():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<lista_deklaracija>")

   if "<deklaracija>" == genTreeInput[0]:
      deklaracija()

   elif "<lista_deklaracija>" == genTreeInput[0]:
      lista_deklaracija()
      deklaracija()

#~DEKLARACIJA #############################################################################################
def deklaracija():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<deklaracija>")

   t = ime_tipa()

   lista_init_deklaratora(t)

   TOCKAZAREZ()

   return None, None, None

#~LISTA INIT DEKLARATORA ##################################################################################
def lista_init_deklaratora(t):
   if __ERROR__:
      return None, None, None

   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<lista_init_deklaratora>")

   if "<init_deklarator>" == genTreeInput[0]:
      init_deklarator(t)

   elif "<lista_init_deklaratora>":
      lista_init_deklaratora(t)
      ZAREZ()
      init_deklarator(t)

   else:
      throwError()

   return None, None, None
      
#~INIT DEKLARATOR #########################################################################################
def init_deklarator(t1):
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<init_deklarator>")

   t2, lval2, name2, value2 = izravni_deklarator(t1)

   if not "OP_PRIDRUZI" in genTreeInput[0]:
      #Validation--------------------------
      if CONST in t2:
         throwError()
      #------------------------------------
      return None, None, None
   
   OP_PRIDRUZI()

   types = inicijalizator(t1)

   #Validation -------------------------------------
   if len(types) > value2:
      throwError()
   else:
      for type in types:
         if not (type == t2 or type in castDict[t2]):
            throwError()
   #------------------------------------------------
   
   return None, None, None

#~IZRAVNI DEKLARATOR ######################################################################################
def izravni_deklarator(t):
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<izravni_deklarator>")

   global currentScope

   _, _, name = IDN()

   #Validation------------------------
   if name in currentScope[SCOPE] and len(currentScope[SCOPE][name]) > 0:
      throwError()
   elif t == VOID:
      throwError()
   #----------------------------------

   if not "L_UGL_ZAGRADA" in genTreeInput[0] and not "L_ZAGRADA" in genTreeInput[0]: 
      currentScope[SCOPE][name][TYPE] = t
      currentScope[SCOPE][name][LVAL] = not CONST in t
      return t, not CONST in t, name, 1
   
   elif "L_UGL_ZAGRADA" in genTreeInput[0]:
      L_UGL_ZAGRADA()
      numType, lval, value = BROJ()
      D_UGL_ZAGRADA()
      #Validation --------------------------
      if value <= 0 or value > 1024:
         throwError()
      #-------------------------------------
      t = ARR + " " + t
      currentScope[SCOPE][name][TYPE] = t
      currentScope[SCOPE][name][LVAL] = not CONST in t
      return t, not CONST in t, name, value
   
   elif "L_ZAGRADA" in genTreeInput[0]:
      L_ZAGRADA()
      
      if "KR_VOID" in genTreeInput[0]:
         KR_VOID()
         t = t + "|" + VOID
      
      elif "<lista_parametara>" == genTreeInput[0]:
         types, names = lista_parametara()
         t = t + "|" + ",".join(types)

      else:
         throwError()

      #Validation---------------------------
      if name in currentScope[DECL]:
         if currentScope[DECL][name] == t:
            del currentScope[DECL][name]
         else:
            throwError()
      #------------------------------------

      D_ZAGRADA()
      return t, False, name, 1
      
   else:
      throwError()

   return None, None, None, None

#~INICIJALIZATOR ##########################################################################################
def inicijalizator(t):
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<inicijalizator>")

   if "<izraz_pridruzivanja>" == genTreeInput[0]:
      t, lval, info = izraz_pridruzivanja()
      br_elem = 1
      if ARR in t and CHAR in t:
         br_elem = info + 1

      return [t]*br_elem, lval, info
   
   elif "L_VIT_ZAGRADA" in genTreeInput[0]:
      L_VIT_ZAGRADA()
      types = lista_izraza_pridruzivanja()

      return types
   
   else:
      throwError()

   return None, None, None

#~LISTA IZRAZA PRIDRUZIVANJA ##############################################################################
def lista_izraza_pridruzivanja():
   if __ERROR__:
      return None, None, None
   
   currentElement = genTreeInput.popleft()
   if __DEBUG__:
      print(currentElement, currentElement == "<lista_izraza_pridruzivanja>")

   if "<izraz_pridruzivanja>" == genTreeInput[0]:
      t, lval, info = izraz_pridruzivanja()
      return [t]
   
   elif "<lista_izraza_pridruzivanja>" == genTreeInput[0]:
      types = lista_izraza_pridruzivanja()
      ZAREZ()
      type = [izraz_pridruzivanja()[0]]
      return types + type

   else:
      throwError()

   return None, None, None
###########################################################################################################
#MAIN ##################################################################################################
###########################################################################################################

def main():
   for line in fileinput.input():
      line = line.rstrip("\n")
      line  = line.lstrip(" ")
      genTreeInput.append(line)
   
   global globalScopeNode

   prijevodna_jedinica()

   if not __ERROR__:
      if not "main" in globalScopeNode[SCOPE]:
         print("main")
         print(globalScopeNode)
      
      toVisit = [globalScopeNode]

      while toVisit:
         current = toVisit.pop()
         if len(current[DECL]) > 0:
            print("funkcija")
            break
         toVisit.extend(current[KIDS])

   if __ERROR_INFO__:
      print(__ERROR_INFO__)
   
   if not genTreeInput:
      return True
   else:
      return False
   

if __name__ == "__main__":
   main()