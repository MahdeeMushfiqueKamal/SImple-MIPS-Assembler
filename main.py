#to run: python main.py input.mips output.txt

import sys
from SupportFunctions import *

if len(sys.argv) < 2:
    print("Input filename is not provided")
    sys.exit()
if len(sys.argv) < 3:
    print("Output filename is not provided")
    sys.exit()
elif len(sys.argv) > 3:
    print("Too many argument for filename is provided")
    sys.exit()

infilename = sys.argv[1]
infile = open(infilename,'r')

outfilename = sys.argv[2]
outfile = open(outfilename,'w')


lines = infile.readlines()

instructions_list = []
labels_list = {}

for line in lines:
    line = line.strip().lower().replace(","," ")
    if line == "":
        continue
    tokens = line.split()     
    for i in range(len(tokens)):
        tokens[i] = tokens[i].strip()
    
    if tokens[0].endswith(':'):
        label_name = tokens[0].replace(':','')
        labels_list[label_name] = len(instructions_list)
        instructions_list.append(tokens[1:])
    elif tokens[0] == 'push':
        register = tokens[1]
        # sw register 0($sp)
        line1 = ['sw']
        line1.append(register)
        line1.append('0($sp)')
        instructions_list.append(line1)
        # subi $sp, $sp, 1
        line2 = ['subi', '$sp', '$sp', '1']
        instructions_list.append(line2)
    elif tokens[0] == 'pop':
        register = tokens[1]
        # addi $sp, $sp, 1
        line1 = ['addi','$sp', '$sp', '1']
        instructions_list.append(line1)
        # lw register 0($sp)
        line2 = ['lw']
        line2.append(register)
        line2.append('0($sp)')
        instructions_list.append(line2)
    else: 
        instructions_list.append(tokens)
print("---------Pass 1 Done---------\nPush and pop are converted into simple instructions\nall labels are identified")
print('Full instruction list:')
for line_no in range(len(instructions_list)):
    print(line_no," \t", instructions_list[line_no])
print('Full label list:\n',labels_list)
print('\n\n---------Starting Pass 2: ---------')

#pass 2
for line_no in range(len(instructions_list)): 
    tokens = instructions_list[line_no]
    print(line_no," \t", instructions_list[line_no])
    if len(tokens) == 0:
        continue
    instruction = tokens[0]    

    if instruction in ["add","sub","and","or","nor"]:
        # R format detected. dst = src1 + src2. 
        # Output format: opp src1 src2 dst
        if len(tokens) != 4:
            print("Invalid Syntax")
            sys.exit()
        towrite = OppCodeConverter(instruction) + " " + RegisterConverter(tokens[2]) + " " + \
                RegisterConverter(tokens[3])+" " + RegisterConverter(tokens[1])

    elif instruction in ["addi","subi","andi","ori"]:
        # dst = src + amount 
        # Output Format: opp dst src immediate
        if len(tokens) != 4:
            print("Invalid Syntax")
            sys.exit()

        towrite = OppCodeConverter(instruction) + " " + RegisterConverter(tokens[2]) + " " + \
                RegisterConverter(tokens[1])+" " + SignedConverter_4bit(tokens[3])

    elif instruction in ["sll","srl"]:
        if len(tokens) != 4:
            print("Invalid Syntax")
            sys.exit()
        shamt = int(tokens[3])
        if(shamt <0 or shamt>15):
            print("Invalid shift amount")
            sys.exit()
        shamt = bin(shamt).replace("0b", "")
        while len(shamt) < 4:
            shamt = "0"+shamt
        
        towrite = OppCodeConverter(instruction) + " " + RegisterConverter(tokens[2]) + " " + \
                RegisterConverter(tokens[1])+" " + shamt

    elif instruction in ["lw","sw"]:
        # output format: Opcode Src Dst Shamt
        if len(tokens) != 3:
            print("Invalid Syntax")
            sys.exit()
        dst = RegisterConverter(res=tokens[1])
        src, shamt =  ShamtRegisterConverter(token=tokens[2])
        towrite = OppCodeConverter(instruction) + " "+ src+" "+dst+" "+shamt

    # "beq","bneq" kora lagbe
    elif instruction in ['beq', 'bneq']:
        if len(tokens) != 4:
            print("Invalid Syntax")
            sys.exit()
        label_name = tokens[3]
        label_position = labels_list[label_name]
        print('Branch instruction on line: ', line_no, 'need to jump to ', label_position)
        shamt = label_position - line_no - 1
        print('Shift amount is: ', shamt)
        towrite = OppCodeConverter(instruction) + " " + RegisterConverter(tokens[2]) + " " + \
                RegisterConverter(tokens[1])+" " + SignedConverter_4bit(str(shamt))

    else:
        print("Could not process line: ",tokens)
        #sys.exit()
    #processed one line
    print(towrite + "\n\n")
    outfile.write(towrite) 
    outfile.write('\n')


infile.close()
outfile.close()
