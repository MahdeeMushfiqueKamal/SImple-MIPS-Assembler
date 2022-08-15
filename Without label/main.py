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

for line in lines:
    line = line.strip().lower().replace(","," ")
    if line == "":
        outfile.write('\n')
        continue
    print(line)
    
    tokens = line.split()     
    for i in range(len(tokens)):
        tokens[i] = tokens[i].strip()

    instruction = tokens[0]        

    if instruction in ["add","sub","and","or","nor"]:
        # R format detected. dst = src1 + src2. 
        # Output format: opp src1 src2 dst
        if len(tokens) != 4:
            print("Invalid Syntax")
            sys.exit()
        towrite = OppCodeConverter(instruction) + " " + RegisterConverter(tokens[2]) + " " + \
                RegisterConverter(tokens[3])+" " + RegisterConverter(tokens[1])

    elif instruction in ["addi","subi","andi","ori","beq","bne"]:
        # dst = src + amount 
        # Output Format: opp dst src immediate
        if len(tokens) != 4:
            print("Invalid Syntax")
            sys.exit()

        towrite = OppCodeConverter(instruction) + " " + RegisterConverter(tokens[2]) + " " + \
                RegisterConverter(tokens[1])+" " + ConvertNumber(tokens[3])
    
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

    elif instruction == "j":
        if len(tokens) != 2:
            print("Invalid Syntax")
            sys.exit()
        addr = int(tokens[1])
        if addr >= 256 or addr <0: 
            print("Invalid address for J format")
            sys.exit()
        addr = bin(addr).replace("0b", "")
        while len(addr) < 8:
            addr = "0"+addr
        towrite = OppCodeConverter(instruction) + " " + addr[0:4] +" "+ addr[4:8] + " 0000"
    
    elif instruction == "push":
        if len(tokens) != 2:
            print("Invalid Syntax")
            sys.exit()
        register = tokens[1]
        # sw register 0($sp)
        towrite = OppCodeConverter("sw") + " "+ RegisterConverter("$sp")+" "+RegisterConverter(register)+" 0000\n"
        # subi $sp, $sp, 1
        towrite += OppCodeConverter("subi") + " " + RegisterConverter("$sp") + " " + RegisterConverter("$sp") + " 0001"

    elif instruction == "pop":
        if len(tokens) != 2:
            print("Invalid Syntax")
            sys.exit()
        register = tokens[1]
        # addi $sp, $sp, 1
        towrite = OppCodeConverter("addi") + " " + RegisterConverter("$sp") + " " + RegisterConverter("$sp") + " 0001\n"
        # lw register 0($sp)
        towrite += OppCodeConverter("lw") + " " + RegisterConverter("$sp")+" "+RegisterConverter(register)+" 0000\n"


    
    else:
        print("Could not process line: ",line)
        sys.exit()
    #processed one line
    print(towrite + "\n\n")
    outfile.write(towrite) 
    outfile.write('\n')


infile.close()
outfile.close()
