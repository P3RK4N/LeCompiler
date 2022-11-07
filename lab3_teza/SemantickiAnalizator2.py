import fileinput
from collections import deque, defaultdict as dd

#DEBUGGING & GLOBALS #######################################################################################
__DEBUG__ = False

PARENT = "PARENT" #Parent Node
KIDS = "KIDS"     #Kid Nodes
SCOPE = "SCOPE"   #Scope identities
TYPE = "TYPE"     #Type of scope identity
NAME = "NAME"     #Name of scope identity (Redundant)
FUNC = "FUNC"     #Current function
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
inFunction = False
inLoop = False

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

def throwError(e = ""):
   print(e)
   exit(0)

########################################################################################
#IZRAZI ################################################################################
########################################################################################

#PRIMARNI IZRAZ#
def primarni_izraz():
   
   if "IDN" in genTreeInput[0]:
      pass

   elif "BROJ" in genTreeInput[0]:
      pass

   elif "ZNAK" in genTreeInput[0]:
      pass

   elif "NIZ_ZNAKOVA" in genTreeInput[0]:
      pass

   elif "L_ZAGRADA" in genTreeInput[0]:
      pass

#POSTFIKS IZRAZ#
def postfiks_izraz():
   
   if "<primarni_izraz>" == genTreeInput[0]:
      pass
   
   elif "<postfiks_izraz>" == genTreeInput[0]:
      
      if "L_UGL_ZAGRADA" in genTreeInput[0]:
         pass

      elif "OP_INC" in genTreeInput[0] or "OP_DEC" in genTreeInput[0]:
         pass
      
      elif "L_ZAGRADA" in genTreeInput[0]:

         if "<lista_argumenata>" in genTreeInput[0]:
            pass

#LISTA ARGUMENATA#
def lista_argumenata():

   if "<izraz_pridruzivanja>" == genTreeInput[0]:
      pass

   elif "<lista_argumenata>" == genTreeInput[0]:
      pass

#UNARNI IZRAZ#
def unarni_izraz():

   if "<postfiks_izraz>" == genTreeInput[0]:
      pass

   elif "OP_INC" in genTreeInput[0] or "OP_DEC" in genTreeInput[0]:
      pass

   elif "<unarni_operator>" == genTreeInput[0]:
      pass

#UNARNI OPERATOR#
#Not needed
   
#CAST IZRAZ#
def cast_izraz():

   if "<unarni_izraz>" == genTreeInput[0]:
      pass

   elif "L_ZAGRADA" in genTreeInput[0]:
      pass

#IME TIPA#
def ime_tipa():

   if "<specifikator_tipa>" == genTreeInput[0]:
      pass

   elif "KR_CONST" in genTreeInput[0]:
      pass

#SPECIFIKATOR TIPA#
#Not Needed
   
#IZRAZI#
def operacijski_izrazi(top, bottom):

   if callable(bottom):
      pass

   elif bottom == genTreeInput[0]:
      pass

   elif top == genTreeInput[0]:
      pass


izrazi = {
   "<multiplikativni_izraz>" : cast_izraz,
   "<aditivni_izraz>" : "<multiplikativni_izraz>",
   "<odnosni_izraz>" : "<aditivni_izraz>",
   "<jednakosni_izraz>" : "<odnosni_izraz>",
   "<bin_i_izraz>" : "<jednakosni_izraz>",
   "<bin_xili_izraz>" : "<bin_i_izraz>",
   "<bin_ili_izraz>" : "<bin_xili_izraz>",
   "<log_i_izraz>" : "<bin_ili_izraz>",
   "<log_ili_izraz>" : "<log_i_izraz>"
}

#IZRAZ PRIDRUZIVANJA#
def izraz_pridruzivanja():

   if "<log_ili_izraz>" == genTreeInput[0]:
      pass

   elif "<postfiks_izraz>" == genTreeInput[0]:
      pass

#IZRAZ#
def izraz():

   if "<izraz_pridruzivanja>" == genTreeInput[0]:
      pass

   elif "<izraz>" == genTreeInput[0]:
      pass



########################################################################################
#NAREDBENA STRUKTURA ###################################################################
########################################################################################

#SLOZENA NAREDBA#
def slozena_naredba():
   
   if "<lista_naredbi>" == genTreeInput[0]:
      pass

   elif "<lista_deklaracija>" == genTreeInput[0]:
      pass

#LISTA NAREDBI#
def lista_naredbi():

   if "<naredba>" == genTreeInput[0]:
      pass

   elif "<lista_naredbi>" == genTreeInput[0]:
      pass

#NAREDBA#
def naredba():

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

   elif "<naredba_skoka>" == genTreeInput[0]:

      if "KR_CONTINUE" in genTreeInput[0] or "KR_BREAK" in genTreeInput[0]:
         pass

      elif "KR_RETURN" in genTreeInput[0]:
         pass

#PRIJEVODNA JEDINICA#
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

   if "KR_VOID" in genTreeInput[0]:
      pass

   elif "<lista_parametara>" == genTreeInput[0]:
      pass

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
   pass

if __name__ == "__main__":
   main()