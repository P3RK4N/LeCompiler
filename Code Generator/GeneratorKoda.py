import fileinput
from collections import deque, defaultdict as dd
from copy import deepcopy as cp
from pprint import pprint

WORD_SIZE = 4
LOG_WORD_SIZE = 2
STACK_START = 0x002020 # grows by substracting
CONST_START = 0x002030 # grows by adding

# TODO incrementing

def throwError(e = ""):
	# print("ERROR",e)
	print(e)
	exit(0)

# asadfasdf sadfdsa constante popravit 

########################################################################################
#IZRAZI ################################################################################
########################################################################################

loop_id = []
#PRIMARNI IZRAZ# FINISHED REFACTORED
string_init_size = None
def primarni_izraz(): #Returns type, lval
	iline = len(genTreeInput_base) -  len(genTreeInput)
	genTreeInput.popleft()

	if "IDN" in genTreeInput[0][0]:
		_, _, val = genTreeInput.popleft()[0].split(" ")
		push_var_onto_stack(val, iline, shift=0)
		return val

	elif "BROJ" in genTreeInput[0][0]:
		_, _, val = genTreeInput.popleft()[0].split(" ")
		val = int(val)
		push_const_onto_stack(val, iline)

	elif "NIZ_ZNAKOVA" in genTreeInput[0][0]:
		_, _, val = genTreeInput.popleft()[0].split(" ")
		global string_init_size
		filled_val = val[1:-1] + '\0'*(string_init_size - len(val)+1)
		for i, c in enumerate(filled_val):
			push_const_onto_stack(ord(c), iline=f'{iline}_{i}')
			do_op("OP_ASSIGN_ARRAY")
		push_const_onto_stack(ord('\0'), iline)


	elif "ZNAK" in genTreeInput[0][0]:
		_, _, val = genTreeInput.popleft()[0].split(" ")
		val = val[1:-1]
		push_const_onto_stack(ord(val), iline)
	
	elif "L_ZAGRADA" in genTreeInput[0][0]:
		genTreeInput.popleft()
		izraz()
		genTreeInput.popleft()

	return None

#POSTFIKS IZRAZ# FINISHED REFACTORED - CRITICAL
def postfiks_izraz(): #Returns type, lval
	genTreeInput.popleft()
	
	if "<primarni_izraz>" == genTreeInput[0][0]:
		return primarni_izraz()
	
	#Postfix izraz - dodaj u produkciju
	elif "<postfiks_izraz>" == genTreeInput[0][0]:
		func_name = postfiks_izraz()

		#ARRAY ELEMENT
		#L UGL ZAGRADA - provjeri jel niz i jel tip izraza int
		if "L_UGL_ZAGRADA" in genTreeInput[0][0]:
			genTreeInput.popleft()

			izraz()

			#D_UGL_ZAGRADA
			genTreeInput.popleft()
			do_op('INDEX')
			
		#INCREMENTIRANJE
		elif "OP_INC" in genTreeInput[0][0] or "OP_DEC" in genTreeInput[0][0]:
			op = genTreeInput.popleft()[0].split()[0]
			do_op('POSTFIX_'+op)
			
		#FUNCTION CALL
		elif "L_ZAGRADA" in genTreeInput[0][0]:
			genTreeInput.popleft()

			#Lista argumenata - dodaj u produkciju, provjeri jel su tipovi isti
			if "<lista_argumenata>" in genTreeInput[0][0]:
				lista_argumenata()

			#D ZAGRADA
			genTreeInput.popleft()
			do_call_function(func_name)
		return None

#LISTA ARGUMENATA# FINISHED REFACTORED
def lista_argumenata(): #Returns list(types)
	genTreeInput.popleft()

	if "<izraz_pridruzivanja>" == genTreeInput[0][0]:
		izraz_pridruzivanja()

	elif "<lista_argumenata>" == genTreeInput[0][0]:
		lista_argumenata()
		#ZAREZ
		genTreeInput.popleft()[0]
		izraz_pridruzivanja()

	do_op("POP_JUST_POINTER")
	

	

#UNARNI IZRAZ# FINISHED REFACTORED
#UNARNI OPERATOR# FINISHED REFACTORED
def unarni_izraz():
	iline = len(genTreeInput_base) -  len(genTreeInput)
	genTreeInput.popleft()

	if "<postfiks_izraz>" == genTreeInput[0][0]:
		postfiks_izraz()

	#Provjeri jel tip INT
	elif "OP_INC" in genTreeInput[0][0] or "OP_DEC" in genTreeInput[0][0]:
		#Operator
		op = genTreeInput.popleft()[0].split()[0]

		#Unarni izraz
		unarni_izraz()
		do_op('PREFIX_'+op)

	elif "<unarni_operator>" == genTreeInput[0][0]:
		#Unarni operator
		genTreeInput.popleft()[0]
		#Cast izraz
		op = genTreeInput.popleft()[0].split()[0]
		cast_izraz()
		do_op('UNARY_'+op, iline)


#CAST IZRAZ# FINISHED REFACTORED
def cast_izraz(): #Returns type, lval
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
		cast_izraz()

#IME TIPA# - FINISHED REFACTORED
#SPECIFIKATOR TIPA# - FINISHED REFACTORED
def ime_tipa():
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

	return int(isConst)*"CONST " + tip

#IZRAZI# FINISHED REFACTORED
def operacijski_izrazi(top): #Returns type, lval
	iline = len(genTreeInput_base) -  len(genTreeInput)
	genTreeInput.popleft()

	#Podizraz
	if izrazi[top] == genTreeInput[0][0]:
		if izrazi[top] != "<cast_izraz>":
			operacijski_izrazi(izrazi[top])
		else:
			cast_izraz()
		
	#Isti izraz - dodaj u produkciju
	elif top == genTreeInput[0][0]:
		operacijski_izrazi(top)

		#Operator
		op = genTreeInput.popleft()[0].split()[0]
		if op in ['OP_ILI', 'OP_I']:
			do_half_log_and_or(op, iline)

		if izrazi[top] != "<cast_izraz>":
			operacijski_izrazi(izrazi[top])
		else:
			cast_izraz()

		if op in ['OP_ILI', 'OP_I']:
			do_end_log_and_or(op, iline)
		else:
			do_op(op, iline)
		

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
	genTreeInput.popleft()

	#LOG ILI IZRAZ
	if "<log_ili_izraz>" == genTreeInput[0][0]:
		return operacijski_izrazi("<log_ili_izraz>")
	
	#POSTFIKS IZRAZ - dodaj na produkciju
	elif "<postfiks_izraz>" == genTreeInput[0][0]:
		postfiks_izraz()

		#OP PRIDRUZI
		genTreeInput.popleft()

		izraz_pridruzivanja()
		do_op('OP_ASSIGN')
	
#IZRAZ# FINISHED REFACTORED
def izraz(): #Returns type, lval
	genTreeInput.popleft()[0]

	#Izraz
	if "<izraz>" == genTreeInput[0][0]:
		izraz()
		do_op("POP")

		#Zarez
		genTreeInput.popleft()[0]

	#Izraz pridruzivanja
	izraz_pridruzivanja()

########################################################################################
#NAREDBENA STRUKTURA ###################################################################
########################################################################################

#SLOZENA NAREDBA# - FINISHED REFACTORED
def slozena_naredba():
	iline = len(genTreeInput_base) -  len(genTreeInput)
	mem = {}
	genTreeInput.popleft()[0]

	#L_VIT_ZAGRADA
	genTreeInput.popleft()[0]

	if "<lista_deklaracija>" == genTreeInput[0][0]:
		mem.update(lista_deklaracija())

	genTreeInput[0]
	mem.update(lista_naredbi())

	#D_VIT_ZAGRADA
	genTreeInput.popleft()[0]
	return {iline:mem}

#LISTA NAREDBI# - FINISHED REFACTORED
def lista_naredbi():
	genTreeInput.popleft()[0]
	mem = {}

	if "<lista_naredbi>" == genTreeInput[0][0]:
		mem.update(lista_naredbi())

	genTreeInput[0]
	mem.update(naredba())
	return mem

#IZRAZ NAREDBA
def izraz_naredba():
	genTreeInput.popleft()[0]

	if "<izraz>" == genTreeInput[0][0]:
		izraz()
		do_op("POP")

	else:
		do_move_true_to_rv()

	genTreeInput.popleft()[0]

#NAREDBA# FINISHED REFACTORED - CRITICAL CRITICAL
def naredba():
	genTreeInput.popleft()[0]

	if "<slozena_naredba>" == genTreeInput[0][0]:
		return slozena_naredba()

	elif "<izraz_naredba>" == genTreeInput[0][0]:
		izraz_naredba()
		return {}

	elif "<naredba_grananja>" == genTreeInput[0][0]:
		iline = len(genTreeInput_base) -  len(genTreeInput)
		genTreeInput.popleft()
		#IF
		genTreeInput.popleft()
		#L ZAGRADA
		genTreeInput.popleft()
		#IZRAZ
		izraz()
		do_if(id=iline)
		#D ZAGRADA
		genTreeInput.popleft()
		#NAREDBA
		mem = {iline:naredba()}
		#ELSE i NAREDBA
		do_else(id=iline)
		if "KR_ELSE" in genTreeInput[0][0]:
			genTreeInput.popleft()
			iline_else = len(genTreeInput_base) -  len(genTreeInput)
			mem[iline_else] = naredba()
		do_end_if(id = iline)
		return mem

	elif "<naredba_petlje>" == genTreeInput[0][0]:
		iline = len(genTreeInput_base) -  len(genTreeInput)
		loop_id.append(iline)
		genTreeInput.popleft()

		if "KR_WHILE" in genTreeInput[0][0]:
			genTreeInput.popleft()
			#L ZAGRADA
			genTreeInput.popleft()
			#IZRAZ
			do_for_start(id=iline)	# we just mimic the for loop
			izraz()
			do_op("POP")	# this is needed cause there is no ; in while(here)
			do_for_compare(id=iline)
			do_for_inc(id=iline)
			#D ZAGRADA
			genTreeInput.popleft()
			naredba_out = naredba()
			do_for_end(id=iline)

			return {iline:naredba_out}

		elif "KR_FOR" in genTreeInput[0][0]:
			genTreeInput.popleft()
			#L ZAGRADA
			genTreeInput.popleft()
			#IZRAZ NAREDBA 1 i 2
			izraz_naredba()
			do_for_start(id=iline)
			t = izraz_naredba()
			do_for_compare(id=iline)		# TODO sto ako su naredbe ;

			if "<izraz>" == genTreeInput[0][0]:
				izraz()
				do_op("POP")
			do_for_inc(id=iline)

			#D ZAGRADA         
			genTreeInput.popleft()
			naredba_out = naredba()
			do_for_end(id=iline)

			return {iline:naredba_out}

		loop_id.pop()

	#Naredba skoka
	elif "<naredba_skoka>" == genTreeInput[0][0]:
		genTreeInput.popleft()

		if "KR_CONTINUE" in genTreeInput[0][0] or "KR_BREAK" in genTreeInput[0][0]:
			op = genTreeInput.popleft()[0].split()[0]
			genTreeInput.popleft()
			do_loop_jump(op, id=loop_id[-1])


		#KR RETURN
		elif "KR_RETURN" in genTreeInput[0][0]:
			genTreeInput.popleft()
			#Izraz - dodaj na produkciju, stavi u returnType
			if "<izraz>" == genTreeInput[0][0]:
				izraz()
			else:
				do_op("PUSH")
			#Tockazarez
			genTreeInput.popleft()
			do_function_end_jump()
		return {}
		
#PRIJEVODNA JEDINICA# - FINISHED REFACTORED
#VANJSKA DEKLARACIJA# - FINISHED REFACTORED
def prijevodna_jedinica():
	genTreeInput.popleft()

	if "<prijevodna_jedinica>" == genTreeInput[0][0]:
		prijevodna_jedinica()

	#Vanjska Deklaracija
	genTreeInput.popleft()
	genTreeInput[0][0]

	if  "<definicija_funkcije>" == genTreeInput[0][0]:
		scope, iline = definicija_funkcije()
		global_mem['functions'][iline] = scope

	elif "<deklaracija>" == genTreeInput[0][0]:
		global_mem['globals'].update(deklaracija())

		
########################################################################################
#DEKLARACIJE I DEFINICIJE ##############################################################
########################################################################################

#DEFINICIJA FUNKCIJE# REFACTORED
def definicija_funkcije():
	# production = Util.getProduction(genTreeInput) ???
	iline = len(genTreeInput_base) -  len(genTreeInput)
	function_begin(iline)
	genTreeInput.popleft()

	#Ime tipa - dohvati returnType i provjeri jel const
	returnType = ime_tipa()

	#IDN - provjeri jel postoji definirana func s tim imenom
	idn, typeLine, funcName = genTreeInput.popleft()[0].split(" ")

	#L ZAGRADA
	genTreeInput.popleft()

	params = []
	#KR VOID - dohvati paramType, ako deklarirana, mora bit isti tip, dodaj u scope
	if "KR_VOID" in genTreeInput[0][0]:
		genTreeInput.popleft()
	
	#LISTA PARAMETARA - isto kao i KR VOID
	elif "<lista_parametara>" == genTreeInput[0][0]:
		params = lista_parametara()

	#D ZAGRADA
	genTreeInput.popleft()

	#Slozena naredba - napravi novi scope i udi, dodaj function stack, dodaj parametre u scope, udji u slozenu funkciju, skini function stack, izadi iz scopea
	mem = slozena_naredba()
	do_op("PUSH")	# if it comes here it means it was void so we need to put somehitng on the stack
	function_end(iline)
	return {'inner':mem, 'params':params, 'name':funcName}, iline

#LISTA PARAMETARA# FINISHED REFACTORED
def lista_parametara():
	genTreeInput.popleft()
	params = []

	if "<lista_parametara>" == genTreeInput[0][0]:
		params.extend(lista_parametara())
		#ZAREZ
		genTreeInput.popleft()

	params.append(deklaracija_parametra())

	return params

#DEKLARACIJA PARAMETRA# FINISHED REFACTORED
def deklaracija_parametra():
	genTreeInput.popleft()

	t = ime_tipa()

	_, _, name = genTreeInput.popleft()[0].split(" ")

	if "L_UGL_ZAGRADA" in genTreeInput[0][0]:
		genTreeInput.popleft()
		genTreeInput.popleft()

	return name

#LISTA DEKLARACIJA# FINISHED REFACTORED
def lista_deklaracija():
	genTreeInput.popleft()[0]
	mem = {}

	if "<lista_deklaracija>" == genTreeInput[0][0]:
		mem.update(lista_deklaracija())

	mem.update(deklaracija())
	return mem

#DEKLARACIJA# FINISHED REFACTORED
# TODO sta ako ne idu deklaracije pa funkcije ???
def deklaracija():
	genTreeInput.popleft()[0]
	t = ime_tipa()
	mem = lista_init_deklaratora()
	genTreeInput.popleft()[0]
	do_op("POP")
	return mem

#LISTA INIT DEKLARATORA# FINISHED REFACTORED
def lista_init_deklaratora():
	genTreeInput.popleft()[0]
	mem = {}

	if "<lista_init_deklaratora>" == genTreeInput[0][0]:
		mem.update(lista_init_deklaratora())
		genTreeInput.popleft()[0]
		do_op("POP")
	mem.update(init_deklarator())
	return mem

#INIT DEKLARATOR# FINISHED REFACTORED - CRITICAL
def init_deklarator():
	iline = len(genTreeInput_base) -  len(genTreeInput)
	genTreeInput.popleft()

	#Izravni deklarator
	declType, declSize, declName = izravni_deklarator()
	global string_init_size 
	string_init_size = declSize
	push_var_onto_stack(declName, iline, shift=0)

	#Operator - dodaj u produkciju
	if "OP_PRIDRUZI" in genTreeInput[0][0]:
		genTreeInput.popleft()   

		#inicijalizator - dodan vec u produkciju
		initTypes = inicijalizator(declSize)

	if declType != 'function':
		return {declName:declSize}
	return {}


#IZRAVNI DEKLARATOR# FINISHED REFACTORED - CRITICAL
def izravni_deklarator(): #Returns type, size, name
	genTreeInput.popleft()

	#IDN
	_, _, name = genTreeInput.popleft()[0].split(" ")
	
	if "L_UGL_ZAGRADA" in genTreeInput[0][0]:
		genTreeInput.popleft()
		#BROJ
		_, _, val = genTreeInput.popleft()[0].split(" ")
		val = int(val)
		#D UGL ZAGRADA
		genTreeInput.popleft()
		return '?', val, name

	elif "L_ZAGRADA" in genTreeInput[0][0]:
		genTreeInput.popleft()

		#Funkcija bez parametara
		if "KR_VOID" in genTreeInput[0][0]:
			genTreeInput.popleft()
			genTreeInput.popleft()

		#Funkcija s parametrima
		elif "<lista_parametara>" == genTreeInput[0][0]:
			types_names_params = lista_parametara()
			#D ZAGRADA
			genTreeInput.popleft()[0]

		do_op("PUSH")		
		return 'function', 1, name
	#Samo IDN
	else:
		return '?', 1, name

#INICIJALIZATOR# FINISHED REFACTORED - CRITICAL
def inicijalizator(init_size): #Returns types
	iline = len(genTreeInput_base) -  len(genTreeInput)
	genTreeInput.popleft()[0]

	if "<izraz_pridruzivanja>" == genTreeInput[0][0]:
		izraz_pridruzivanja()
		do_op("OP_ASSIGN_ARRAY")

	elif "L_VIT_ZAGRADA" in genTreeInput[0][0]:
		genTreeInput.popleft()[0]
		n_left = lista_izraza_pridruzivanja(init_size)
		for i in range(n_left):
			push_const_onto_stack(0, iline=f'{iline}_{i}')
			do_op("OP_ASSIGN_ARRAY")
		genTreeInput.popleft()[0]

#LISTA IZRAZA PRIDRUZIVANJA# FINISHED REFACTORED
def lista_izraza_pridruzivanja(init_size): #Returns list of types
	genTreeInput.popleft()[0]

	if "<izraz_pridruzivanja>" == genTreeInput[0][0]:
		izraz_pridruzivanja()
		do_op("OP_ASSIGN_ARRAY")
		return init_size - 1

	elif "<lista_izraza_pridruzivanja>" == genTreeInput[0][0]:
		n_left = lista_izraza_pridruzivanja(init_size-1)
		genTreeInput.popleft()[0]
		izraz_pridruzivanja()
		do_op("OP_ASSIGN_ARRAY")
		return n_left



########################################################################################
#PRINTING ##############################################################################
########################################################################################
SP = 'r7'	# stack pointer
FP = 'r5'	# frame pointer
RV = 'r6'	# return value register
TMP = 'r1'	# temporaty register
TMP2= 'r2'	# temporaty register
TMP3= 'r3'	# temporaty register
TMP4= 'r4'	# temporaty register
const_stack_pointer = CONST_START
const_printed = []
printed = dd(lambda: [])
printed_scope_name = 'global'
def mprint(s, rm_tabs=2, scope_name=None, reset_scope=False, save_scope=True):
	'''
	does not print first and last line
	and skipps first two tabs
	'''
	global printed_scope_name
	tmp = printed_scope_name
	if scope_name is not None:
		tmp = scope_name
	for line in s.split('\n')[1:-1]:
		printed[tmp].append(line[rm_tabs:])
	if save_scope:
		printed_scope_name = tmp
	if reset_scope:
		printed_scope_name = 'global'

def hex0(num):
	return '0'+hex(num)[2:]
		
def print_all():
	for line in printed['global']:
		print(line)
	print('	CALL main')
	print('	HALT')
	for k in printed:
		if k != 'global' and k != 'constants':
			for line in printed[k]:
				print(line)
	print(f'	`ORG {hex0(CONST_START)}')
	for line in printed['constants']:
		print(line)

def write_to_file_all():
	with open('a.frisc', 'w') as fout:
		fout.writelines((l+'\n' for l in printed['global']))
		fout.writelines([
			'	CALL main\n',
			'	HALT\n'
		])
		for k in printed:
			if k != 'global' and k != 'constants':
				fout.writelines((l+'\n' for l in printed[k]))
		fout.write(f'	`ORG {hex0(CONST_START)}\n')
		fout.writelines((l+'\n' for l in printed['constants']))
	

def program_start():
	mprint(
	f'''	
			MOVE {hex0(sp_after_allocated_globals)}, {SP}
			MOVE {SP}, {FP}
	'''
	)

def function_begin(iline):
	if first_pass:
		return 
	mprint(f'''
		{function_names[iline]}
			PUSH {SP}			; save stack pointer
			PUSH {FP}			; save frame pointer
			MOVE {SP}, {FP}		; set frame pointer
			SUB {SP}, {hex0(stack_size[iline])}, {SP}		; allocate local function vars
	''', scope_name=function_names[iline])
	
def function_end(iline):
	if first_pass:
		return 
	mprint(f'''
		F_END_{printed_scope_name}
			POP {TMP}		; pointer ...
			POP {RV}		; the return value of the function is on the stack
			ADD {SP}, {hex0(stack_size[iline])}, {SP}	; deallocate local function vars
			POP {FP} 		; return frame pointer
			POP {SP} 		; return stack pointer
			RET
	''', reset_scope=True)

# pointer is pushed onto stack after value
# which means that later it will be poped before value
def push_var_onto_stack(var, iline, shift):
	if first_pass:
		return 
	if var not in flat_global_mem[iline2scope[iline]] and var in function_names_to_iline:
		return
	# have to also PUSH functions !!!
	mem_addr, size, absolute = flat_global_mem[iline2scope[iline]][var]
	# print(var, flat_global_mem[iline2scope[iline]][var], iline2scope[iline])
	pointer = size > WORD_SIZE # it is pointer if it commands bigger memory
	if absolute:
		mem_addr += shift * 2 * WORD_SIZE
		mem_addr = hex0(mem_addr)
		if pointer:
			mprint(f'''
					MOVE {mem_addr}, {TMP}			; it is a pointer
					PUSH {TMP}
					PUSH {TMP}
			''', 3)
		else:
			mprint(f'''
					LOAD {TMP}, ({mem_addr})
					PUSH {TMP}
					MOVE {mem_addr}, {TMP}
					PUSH {TMP}
			''', 3)
	else:
		mem_addr += shift * 2 * WORD_SIZE
		signed_mem_addr = '+'+hex0(-mem_addr) if mem_addr<0 else '-'+hex0(mem_addr)
		if pointer:
			mprint(f'''
				ADD  {FP}, {signed_mem_addr}, {TMP}			; it is a pointer
				PUSH {TMP}
				PUSH {TMP}
			''', 3)
		else:
			mprint(f'''
					LOAD {TMP}, ({FP}{signed_mem_addr})
					PUSH {TMP}									; {var}
					ADD  {FP}, {signed_mem_addr}, {TMP}			; add pointer ui
					PUSH {TMP}
			''', 3)

def push_string_onto_stack(s, iline):
	for i, c in enumerate(s):
		push_const_onto_stack(ord(c), f'{iline}_{i}')

def push_const_onto_stack(num, iline):
	if first_pass:
		return 
	mprint(f'''
		CONST__{iline}	DW {hex0(num)}
	''', save_scope=False, scope_name='constants')
	mprint(f'''
			LOAD {TMP}, (CONST__{iline})
			PUSH {TMP}
			PUSH {TMP}
	''')

def do_call_function(func_name):
	if first_pass:
		return
	iline = function_names_to_iline[func_name]
	num_params = param_count[iline]
	mprint(f'''
			CALL {func_name}
	''')
	for _ in range(num_params):
		do_op("POP_HALF")
	mprint(f'''
			PUSH {RV}
			PUSH {RV}
	''')

def do_if(id):
	if first_pass:
		return
	mprint(f'''
			POP {TMP}		; start if
			POP {TMP}		; 
			CMP {TMP}, 0
			JP_EQ ELSE_{id}
	''')

def do_else(id):
	if first_pass:
		return
	mprint(f'''
			JP END_IF_{id}
		ELSE_{id}
	''')

def do_end_if(id):
	if first_pass:
		return
	mprint(f'''
		END_IF_{id}
	''')

def do_function_end_jump():
	if first_pass:
		return
	mprint(f'''
			JP F_END_{printed_scope_name}
	''')

def do_for_start(id):
	if first_pass:
		return
	mprint(f'''
		FOR_LOOP_START_{id}
	''')

def do_for_compare(id):
	if first_pass:
		return
	mprint(f'''
			CMP {RV}, 0			;  start for compare
			JP_EQ FOR_END_{id}
			JP FOR_BODY_{id}
		FOR_INC_{id}
	''')

def do_for_inc(id):
	if first_pass:
		return
	mprint(f'''
			JP FOR_LOOP_START_{id}
		FOR_BODY_{id}
	''')

def do_for_end(id):
	if first_pass:
		return
	mprint(f'''
			JP FOR_INC_{id}
		FOR_END_{id}
	''')

def do_loop_jump(op, id):
	if first_pass:
		return
	if 'CONTINUE' in op:
		mprint(f'''
				JP FOR_INC_{id}
		''', 3)
	else:
		mprint(f'''
				JP FOR_END_{id}
		''', 3)

def do_half_log_and_or(op, id):
	if first_pass:
		return
	condition = {
		'OP_ILI' : 'EQ',
		'OP_I' : 'NE',
	}
	mprint(f'''
			POP {TMP2}
			POP {TMP}
			CMP	{TMP}, 0
			JP_{condition[op]} CONTINUE_{op}_{id}
			PUSH {TMP}
			PUSH {TMP2}
			JP END_{op}_{id}
		CONTINUE_{op}_{id}
	''')

def do_end_log_and_or(op, id):
	if first_pass:
		return
	mprint(f'''
			POP {TMP2}
			POP {TMP}
			CMP {TMP}, 0
			JP_EQ LOG_0_{op}_{id}
			MOVE 1, {TMP}
		LOG_0_{op}_{id}
			PUSH {TMP}
			PUSH {TMP2}
		END_{op}_{id}
	''')

def do_move_true_to_rv():
	if first_pass:
		return
	mprint(f'''
			MOVE 1, {RV}
	''')	

def make_tmp_and_tmp2_positive_store_sign_in_tmp3_builtin_function():
	mprint(f'''
		F_make_tmp_and_tmp2_positive_store_sign_in_tmp3_builtin
			MOVE 0, {TMP3}	;   this holds sign
			CMP {TMP}, 0
			JP_SGE NOT_NEGATIVE_divide_1
			MOVE 1, {TMP3}
			XOR {TMP}, 0FFFFFFFF, {TMP}
			ADD {TMP}, 1, {TMP}
		NOT_NEGATIVE_divide_1
			CMP {TMP2}, 0
			JP_SGE NOT_NEGATIVE_divide_2
			XOR {TMP3}, 1, {TMP3}
			XOR {TMP2}, 0FFFFFFFF, {TMP2}
			ADD {TMP2}, 1, {TMP2}
		NOT_NEGATIVE_divide_2
			RET

	''', scope_name='F_make_tmp_and_tmp2_positive_store_sign_in_tmp3_builtin', reset_scope=True, save_scope=False)

def negate_rv_if_tmp3_builtin_function():
	mprint(f'''
		F_negate_rv_if_tmp3_builtin
			CMP {TMP3}, 0
			JP_EQ negate_rv_if_tmp3_builtin_end
			XOR {RV}, 0FFFFFFFF, {RV}
			ADD {RV}, 1, {RV}
		negate_rv_if_tmp3_builtin_end
			RET

	''', scope_name='F_negate_rv_if_tmp3_builtin', reset_scope=True, save_scope=False)


def multiply_builtin_function():
	mprint(f'''
		F_multiply_builtin
			POP {TMP4}		;   holds return addr
			POP {TMP2}		;	
			POP {TMP2}		;   second op
			POP {TMP}
			POP {TMP}		;   first op
			CALL F_make_tmp_and_tmp2_positive_store_sign_in_tmp3_builtin
			MOVE 0, {RV}
		
			JP F_multiply_builtin_loop_condition
		F_multiply_builtin_loop_start
			ADD {RV}, {TMP}, {RV}
			SUB {TMP2}, 1, {TMP2}
		F_multiply_builtin_loop_condition
			CMP {TMP2}, 0
			JP_SGT F_multiply_builtin_loop_start

			CALL F_negate_rv_if_tmp3_builtin
			PUSH {TMP4}
			RET

	''', scope_name='F_multiply_builtin', reset_scope=True, save_scope=False)

def divide_builtin_function():
	mprint(f'''
		F_divide_builtin
			POP {TMP4}		;   holds return addr
			POP {TMP2}		;	
			POP {TMP2}		;   second op
			POP {TMP}
			POP {TMP}		;   first op
			CALL F_make_tmp_and_tmp2_positive_store_sign_in_tmp3_builtin

			MOVE 0, {RV}
			JP F_divide_builtin_loop_condition
		F_divide_builtin_loop_start
			ADD {RV}, 1, {RV}
			SUB {TMP}, {TMP2}, {TMP}
		F_divide_builtin_loop_condition
			CMP {TMP}, {TMP2}
			JP_SGE F_divide_builtin_loop_start

			CALL F_negate_rv_if_tmp3_builtin
			PUSH {TMP4}
			RET

	''', scope_name='F_divide_builtin', reset_scope=True, save_scope=False)

def modulo_builtin_function():
	# Semantička pravila operatora %
	mprint(f'''
		F_modulo_builtin
			POP {TMP4}		;   holds return addr
			POP {TMP2}		;	
			POP {TMP2}		;   second op
			POP {TMP}
			POP {TMP}		;   first op
			CALL F_make_tmp_and_tmp2_positive_store_sign_in_tmp3_builtin

			JP F_modulo_builtin_loop_condition
		F_modulo_builtin_loop_start
			SUB {TMP}, {TMP2}, {TMP}
		F_modulo_builtin_loop_condition
			CMP {TMP}, {TMP2}
			JP_SGE F_modulo_builtin_loop_start

			MOVE {TMP}, {RV}
			CALL F_negate_rv_if_tmp3_builtin
			PUSH {TMP4}
			RET

	''', scope_name='F_modulo_builtin', reset_scope=True, save_scope=False)




# TODO
# Evaluacija operanada logičkih operatora
# 
def do_op(op, iline=None, size=None):
	if first_pass:
		return 
	func = {
		'OP_PUTA': 'F_multiply_builtin',
		'OP_DIJELI': 'F_divide_builtin',
		'OP_MOD': 'F_modulo_builtin',
	}
	binary = {
		'PLUS': 'ADD',
		'MINUS': 'SUB',
		'OP_BIN_I': 'AND',
		'OP_BIN_XILI': 'XOR',
		'OP_BIN_ILI': 'OR',
	}
	relation = {
		'OP_LT': 'SLT',
		'OP_GT': 'SGT',
		'OP_LTE': 'SLE',
		'OP_GTE': 'SGE',
		'OP_EQ': 'EQ',
		'OP_NEQ': 'NE',
	}
	incdec_prefix = {
		'PREFIX_OP_INC': 'ADD',
		'PREFIX_OP_DEC': 'SUB',
	}
	incdec_postfix = {
		'POSTFIX_OP_INC': 'ADD',
		'POSTFIX_OP_DEC': 'SUB',
	}

	if op in binary:
		mprint(f'''
				POP {TMP2}		; {op}
				POP {TMP2}		; get first op
				POP {TMP}
				POP {TMP}		; get second op
				{binary[op]} {TMP}, {TMP2}, {TMP}
				PUSH {TMP}		; {op} end
				PUSH {TMP}		; put dummy pointer
		''', 3)

	elif op in relation:
		label = op + str(iline)
		mprint(f'''
				POP {TMP2}		; have to pop pointer first
				POP {TMP2}		; {op}
				POP {TMP}
				POP {TMP}
				CMP {TMP}, {TMP2}
				MOVE 1, {TMP}
				JP_{relation[op]} {label}
				MOVE 0, {TMP}
			{label}
				PUSH {TMP}		; {op} end
				PUSH {TMP}		; put dummy pointer
		''', 3)

	elif op in incdec_postfix:
		# since the pointer is on the top of the stack and the value should stay the same
		# we dont pop the value
		mprint(f'''
				POP {TMP}		; {op}
				LOAD {TMP2}, ({TMP}+0)
				{incdec_postfix[op]} {TMP2}, 1, {TMP2}
				STORE {TMP2}, ({TMP}+0)
				PUSH {TMP}		; {op} end
		''', 3)

	elif op in incdec_prefix:
		mprint(f'''
				POP {TMP}		; {op}
				POP {TMP2}
				LOAD {TMP2}, ({TMP}+0)
				{incdec_prefix[op]} {TMP2}, 1, {TMP2}
				STORE {TMP2}, ({TMP}+0)
				PUSH {TMP2}		; 
				PUSH {TMP}		; {op} end
		''', 3)

	elif op == 'UNARY_OP_TILDA':
		mprint(f'''
				POP {TMP}		; {op}
				POP {TMP}		; 
				XOR {TMP}, 0FFFFFFFF, {TMP}
				PUSH {TMP}		; 
				PUSH {TMP}		; {op} end
		''', 3)

	elif op == 'UNARY_OP_NEG':
		mprint(f'''
				POP {TMP}		; {op}
				POP {TMP}		; 
				MOVE 1, {TMP2}
				CMP {TMP}, 0
				JP_EQ EXIT_{op}_{iline}
				MOVE 0, {TMP2}
			EXIT_{op}_{iline}
				PUSH {TMP2}		; 
				PUSH {TMP2}		; {op} end
		''', 3)

	elif op == 'UNARY_PLUS':
		pass	# this does nothing

	elif op == 'UNARY_MINUS':
		mprint(f'''
				POP {TMP}		; {op}
				POP {TMP}		; 
				XOR {TMP}, 0FFFFFFFF, {TMP}
				ADD {TMP}, 1, {TMP}
				PUSH {TMP}		; 
				PUSH {TMP}		; {op} end
		''', 3)

	elif op == 'OP_ASSIGN':
		# TODO we should put the result onto stack so that they can be chained
		mprint(f'''
				POP {TMP}			; {op}
				POP {TMP}			; get value
				POP {TMP2}			; get pointer to write to
				POP {TMP3}			; dummy to rm this
				STORE {TMP}, ({TMP2}+0)
				PUSH {TMP}			; push result so it can be
				PUSH {TMP2}
		''', 3)

	elif op == 'OP_ASSIGN_ARRAY':
		mprint(f'''
				POP {TMP}			; {op}
				POP {TMP}			; get value
				POP {TMP2}			; get pointer to write to
				POP {TMP3}			; dummy to rm this
				STORE {TMP}, ({TMP2}+0)
				PUSH {TMP}			; push result so it can be
				ADD {TMP2}, {WORD_SIZE}, {TMP2}
				PUSH {TMP2}
		''', 3)

	elif op == 'POP':
		mprint(f'''
				POP {RV}
				POP {RV}
		''', 3)

	elif op == 'PUSH':
		mprint(f'''
				PUSH {RV}
				PUSH {RV}
		''', 3)

	elif op == 'POP_JUST_POINTER' or op == 'POP_HALF':
		mprint(f'''
				POP {TMP}
		''', 3)

	elif op == 'INDEX':
		mprint(f'''
				POP {TMP}
				POP {TMP}		; get value of index
				POP {TMP2}		; throw away pointer
				POP {TMP2}		; we have to use the value cause the value of the pointer is the addr
				ROTL {TMP}, {hex0(LOG_WORD_SIZE)}, {TMP}	; we need to multipy index by WORD_SIZE
				ADD {TMP}, {TMP2}, {TMP2}
				LOAD {TMP}, ({TMP2}+0)
				PUSH {TMP}
				PUSH {TMP2}
		''', 3)

	elif op in func:
		mprint(f'''
			CALL {func[op]}
			PUSH {RV}
			PUSH {RV}
		''')
		

	else:
		raise ValueError(f'There is no impremented operation for {op}!')

########################################################################################
#MAIN ##################################################################################
########################################################################################


global_vars = {}


if __name__ == "__main__":

	global_mem = dd(lambda: {})

	# load the program
	genTreeInput_base = deque()
	for line in fileinput.input():
		line = line.rstrip("\n")
		size = len(line)
		line = line.strip(" ")
		size -= len(line)
		genTreeInput_base.append((line,size))

	# make the first pass which will count the number of unique varibales
	# inside each function
	genTreeInput = cp(genTreeInput_base)
	first_pass = True
	prijevodna_jedinica()


	# assign unique memory addresses to global vars
	sp = STACK_START
	for k, v in global_mem['globals'].items(): 
		sp -= v * WORD_SIZE #TODO ??????????
		global_mem['globals'][k] = (sp, v * WORD_SIZE, True)
	sp_after_allocated_globals = sp - WORD_SIZE


	# assign unique offset to every variable inside the fuction
	def allocate_memory(scope, sp_offset):
		for var, length in scope.items():
			if type(length) == int:
				# (length-1)*WORD_SIZE is needed because the stack grows by decrementing addr
				# so this is needed for arrays to work
				# the pointer should be to the top of the allocated stack space
				scope[var] = (sp_offset + (length-1)*WORD_SIZE, length * WORD_SIZE, False)
				sp_offset += length * WORD_SIZE
			else:
				sp_offset = allocate_memory(length, sp_offset)
		return sp_offset

	stack_size = {}
	function_names = {}
	param_count = {}
	function_names_to_iline = {}
	for function, scope in global_mem['functions'].items():
		sp_offset = WORD_SIZE #, frame pointer
		sp_offset = allocate_memory(scope['inner'], sp_offset)
		stack_size[function] = sp_offset - WORD_SIZE # one is occupied by frame pointer
		function_names[function] = scope['name']
		function_names_to_iline[scope['name']] = function

		# merge params with other variables
		params = scope['params']
		param_count[function] = len(params)
		# we have to do -2 because of the frame and stack pointers and return addr
		# plus 1 because sp is pointing at the last element (and not the one that is not allocated yet)
		visible = {p:((-len(params)+i-3+1)*WORD_SIZE, WORD_SIZE, False) for i, p in enumerate(params)}
		visible.update(scope['inner'])
		global_mem[function] = visible


	globals = global_mem["globals"]
	del global_mem["functions"]
	del global_mem["globals"]


	# convert nested global memory dictionary to a flat one
	def flatten_scope(prev, iline, scope):
		new = cp(prev)
		new.update(scope)
		toret = {}
		for k, v in new.items():
			if type(k) == str:
				toret[k] = v
		for k, v in new.items():
			if type(k) != str:
				flatten_scope(toret, k, v)

		flat_global_mem[iline] = toret
		

	# convert nested global memory dictionary to a flat one
	flat_global_mem = {}
	for k, v in global_mem.items():
		flatten_scope(globals, k, v)

		# overwrite global scope with local
		tmp = cp(globals)
		tmp.update(flat_global_mem[k])
		flat_global_mem[k] = tmp
	flat_global_mem[len(flat_global_mem)] = globals


	# map every line of the program to its coresponding scope
	iline2scope = ['nan' for _ in range(len(genTreeInput_base))]
	ordered_scopes = [k for k in flat_global_mem] + [float('inf')]
	ordered_scopes.sort()
	iscope = 0
	for iline in range(len(genTreeInput_base)):
		if iline >= ordered_scopes[iscope+1]:
			iscope += 1
		iline2scope[iline] = ordered_scopes[iscope]


	# pprint([(i, iline2scope[i], el) for i, el in enumerate(genTreeInput_base)])
	# pprint(global_mem)
	# pprint(flat_global_mem)
	# print('stack sizes', stack_size)
	# print('function names', function_names)


	# run the second pass where program will be printed
	program_start()
	genTreeInput = cp(genTreeInput_base)
	first_pass = False
	prijevodna_jedinica()

	multiply_builtin_function()
	divide_builtin_function()
	modulo_builtin_function()
	make_tmp_and_tmp2_positive_store_sign_in_tmp3_builtin_function()
	negate_rv_if_tmp3_builtin_function()

	# print_all()
	write_to_file_all()
