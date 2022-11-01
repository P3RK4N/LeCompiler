import difflib
import os
import time

cnt = 0
LAB_FOLDER = 'lab1_teza'
TEST_FOLDER = 'Unit_Test'
dt = 0

PRINT_DIFF = True
SPECIFIC_CASE = False
case = "09_poredak"

os.chdir(LAB_FOLDER)
for folder in os.listdir(TEST_FOLDER):
    if SPECIFIC_CASE and not folder == case:
        continue

    tocompile = TEST_FOLDER + '/' + folder + '/' + "test" + '.in'
    regexdef = TEST_FOLDER + '/' + folder + '/' + "test" + '.lan'
    wanted_result = TEST_FOLDER + '/' + folder + '/' + "test" + '.out'
    
    t = time.time()

    os.system('python3 GLA.py < ' + regexdef)
    os.system('python3 analizator/LA.py < ' + tocompile +' > out.txt')

    dt += time.time()-t

    with open(wanted_result) as file_1:
        file_1_text = file_1.readlines()
    
    with open('out.txt') as file_2:
        file_2_text = file_2.readlines()
    
    a = folder + '.out'
    print(a)
    wrong = False
    if PRINT_DIFF:
        for line in difflib.unified_diff(
                file_1_text, file_2_text, fromfile=a, 
                tofile='out.txt', lineterm=''):
            print(line[:100])
            wrong = True
    else:
        for line in file_2_text:
            print(line)

    cnt = cnt if wrong else cnt+1

print(cnt)
print('total time = ', dt)

""