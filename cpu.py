from array import array
import memory

MIR = 0
MPC = 0

MAR = 0
MDR = 0
PC  = 0
MBR = 0
X   = 0
Y   = 0
H   = 0
K   = 0

N   = 0
Z   = 1

BUS_A = 0
BUS_B = 0
BUS_C = 0


# INSTRUÇÃO DE 35 BITS:
#                                            1  = K
#                                           1   = H
#                                          1    = Y
#                                         1     = X
#                                        1      = PC
#                                       1       = MDR
#                                      1        = MAR
# 000000000 000    00          000000  0000000         000               000          000
# NEXT_ADD  JMPC   DESLOCADOR  ULA     REGISTRADORES  WRITE/READ/FETCH/  BARRAMENTO B BARRAMENTO A

firmware = array('Q', [0]) * 512

#main
firmware[0] = 0b000000000_100_00_110101_0010000_001_001_000
            #PC <- PC + 1; MBR <- read_byte(PC); GOTO MBR;

#X = X + mem[address]
firmware[2] = 0b000000011_000_00_110101_0010000_001_001_000 
            #PC <- PC + 1; MBR <- read_byte(PC); GOTO 3
firmware[3] = 0b000000100_000_00_010100_1000000_010_010_000 
            #MAR <- MBR; read_word; GOTO 4
firmware[4] = 0b000000101_000_00_010100_0000010_000_000_000 
            #H <- MDR; GOTO 5
firmware[5] = 0b000000000_000_00_111100_0001000_000_011_000 
            #X <- X + H; GOTO MAIN;

#mem[address] = X
firmware[6] = 0b000000111_000_00_110101_0010000_001_001_000 
            #PC <- PC + 1; fetch; GOTO 7
firmware[7] = 0b000001000_000_00_010100_1000000_000_010_000 
            #MAR <- MBR; GOTO 8
firmware[8] = 0b000000000_000_00_010100_0100000_100_011_000 
            #MDR <- X; write; GOTO MAIN

#mem[address] = Y
firmware[50] = 0b000110011_000_00_110101_0010000_001_001_000
            #PC <- PC + 1; fetch; GOTO 51
firmware[51] = 0b000110100_000_00_010100_1000000_000_010_000
            #MAR <- MBR; GOTO 52
firmware[52] = 0b000000000_000_00_010100_0100000_100_100_000 
            #MDR <- Y; write; GOTO MAIN

#goto address
firmware[9]  = 0b000001010_000_00_110101_0010000_001_001_000 
            #PC <- PC + 1; fetch; GOTO 10
firmware[10] = 0b000000000_100_00_010100_0010000_001_010_000 
            #PC <- MBR; fetch; GOTO MBR;

#if X = 0 goto address
firmware[11]  = 0b000001100_001_00_010100_0001000_000_011_000 
            #X <- X; IF ALU = 0 GOTO 268 (100001100) ELSE GOTO 12 (000001100);
firmware[12]  = 0b000000000_000_00_110101_0010000_000_001_000 
            #PC <- PC + 1; GOTO MAIN;
firmware[268] = 0b100001101_000_00_110101_0010000_001_001_000 
            #PC <- PC + 1; fetch; GOTO 269
firmware[269] = 0b000000000_100_00_010100_0010000_001_010_000 
            #PC <- MBR; fetch; GOTO MBR;

#if Y = 0 goto address
firmware[62]  = 0b000111111_001_00_010100_0000100_000_100_010
    #Y <- Y; IF ALU = 0 GOTO 319 (100001100) ELSE GOTO 63 (000001100);
firmware[63]  = 0b000000000_000_00_110101_0010000_000_001_000
    #PC <- PC + 1; GOTO MAIN;
firmware[319] = 0b101000000_000_00_110101_0010000_001_001_000
    #PC <- PC + 1; fetch; GOTO 269
firmware[320] = 0b000000000_100_00_010100_0010000_001_010_000
    #PC <- MBR; fetch; GOTO MBR;

#X = X - mem[address]
firmware[13] = 0b000001110_000_00_110101_0010000_001_001_000 
            #PC <- PC + 1; fetch;
firmware[14] = 0b000001111_000_00_010100_1000000_010_010_000 
            #MAR <- MBR; read;
firmware[15] = 0b000010000_000_00_010100_0000010_000_000_000
            #H <- MDR;
firmware[16] = 0b000000000_000_00_111111_0001000_000_011_000 
            #X <- X - H; GOTO MAIN;

#Y = Y - mem[address]
firmware[64] = 0b001000001_000_00_110101_0010000_001_001_000
    #PC <- PC + 1; fetch;
firmware[65] = 0b001000010_000_00_010100_1000000_010_010_000
    #MAR <- MBR; read;
firmware[66] = 0b001000011_000_00_010100_0000010_000_000_000
    #H <- MDR;
firmware[67] = 0b000000000_000_00_111111_0000100_000_100_000
    #Y <- Y - H; GOTO MAIN;

#Y = Y + mem[adress]
firmware[17] = 0b000010010_000_00_110101_0010000_001_001_000 
            #PC <- PC + 1; MBR <- read_byte(PC); GOTO 18
firmware[18] = 0b000010011_000_00_010100_1000000_010_010_000 
            #MAR <- MBR; read_word; GOTO 19
firmware[19] = 0b000010100_000_00_010100_0000010_000_000_000 
            #H <- MDR; GOTO 20
firmware[20] = 0b000000000_000_00_111100_0000100_000_100_000 
            #Y <- Y + H; GOTO MAIN;
 
#X = mem[address]
firmware[25] = 0b000011010_000_00_110101_0010000_001_001_000
            #PC <- PC + 1; MBR <- read_byte(PC); GOTO 26
firmware[26] = 0b000011011_000_00_010100_1000000_010_010_000 
            #MAR <- MBR; read_word; GOTO 27
firmware[27] = 0b000011100_000_00_010100_0000010_000_000_000
            #H <- MDR; GOTO 28
firmware[28] = 0b000000000_000_00_011000_0001000_000_011_000 
            #X <- H; GOTO MAIN;

#Y = mem[address]
firmware[29] = 0b000011110_000_00_110101_0010000_001_001_000 
            #PC <- PC + 1; MBR <- read_byte(PC); GOTO 18
firmware[30] = 0b000011111_000_00_010100_1000000_010_010_000 
            #MAR <- MBR; read_word; GOTO 19
firmware[31] = 0b000100000_000_00_010100_0000010_000_000_000 
            #H <- MDR; GOTO 20
firmware[32] = 0b000000000_000_00_011000_0000100_000_100_000 
            #Y <- H; GOTO MAIN;

#X = H
firmware[33] = 0b000000000_000_00_011000_0001000_000_000_000
            #X <- H; GOTO MAIN;

#X = X << 1
firmware[34] = 0b000000000_000_01_011000_0001000_000_000_001
            #X <- X << 1; GOTO MAIN;

#Y = Y << 1
firmware[53] = 0b000000000_000_01_011000_0000100_000_000_010
            #Y <- Y << 1; GOTO MAIN;

#X = X >> 1
firmware[35] = 0b000000000_000_10_011000_0001000_000_000_001
            #X <- X >> 1; GOTO MAIN;

#X = X << 8
firmware[36] = 0b000000000_000_11_011000_0001000_000_000_001
            #X <- X << 8; GOTO MAIN;

#X = X and mem[address]
firmware[46] = 0b000101111_000_00_110101_0010000_001_001_000 
            #PC <- PC + 1; MBR <- read_byte(PC); GOTO 3
firmware[47] = 0b000110000_000_00_010100_1000000_010_010_000 
            #MAR <- MBR; read_word; GOTO 4
firmware[48] = 0b000110001_000_00_010100_0000010_000_000_000 
            #H <- MDR; GOTO 5
firmware[49] = 0b000000000_000_00_001100_0001000_000_011_000 
            #X <- X and H; GOTO MAIN;

#X = X * Y
firmware[54] = 0b000110111_000_00_010000_0000010_000_000_000
    #H <- 0; GOTO 55
firmware[55] = 0b000111000_000_00_110001_0000001_000_000_000
    #K<- 1; GOTO 56
firmware[56] = 0b000111001_000_00_001100_0000001_000_011_011
    #K<- X and K; GOTO 57
firmware[57] = 0b000111010_001_00_011000_0000000_000_000_011
    #IF K = 0 GOTO 314; ELSE GOTO 58
firmware[58] = 0b100111010_000_00_111100_0000010_000_100_000
    #H <- H + Y; GOTO 314
firmware[314] = 0b000111100_000_01_011000_0000100_000_000_010
    #Y = Y << 1; GOTO 60
firmware[60] = 0b000111101_000_10_011000_0001000_000_000_001
    #X = X >> 1; GOTO 61
firmware[61] = 0b000110111_001_00_010100_0000000_000_011_000
    #IF X = 0 GOTO 311; ELSE GOTO 55
firmware[311] = 0b000000000_000_00_011000_0001000_000_000_000
    #X = H; GOTO MAIN

#X = Y % X
firmware[37] = 0b000000000_000_00_011001_0001000_000_011_010

def read_regs(reg_numA, reg_numB):
    global BUS_A, BUS_B, H, MDR, PC, MBR, X, Y, K

    if reg_numA == 0:
        BUS_A = H
    if reg_numA == 1:
        BUS_A  = X
    if reg_numA == 2:
        BUS_A = Y
    if reg_numA == 3:
        BUS_A= K
    if reg_numA == 7:
        BUS_A = 0

    if reg_numB == 0:
        BUS_B = MDR
    elif reg_numB == 1:
        BUS_B = PC
    elif reg_numB == 2:
        BUS_B = MBR
    elif reg_numB == 3:
        BUS_B = X
    elif reg_numB == 4:
        BUS_B = Y
    elif reg_numB == 5:
        BUS_B = H
    else:
        BUS_B = 0

def write_regs(reg_bits):
    global MAR, MDR, PC, X, Y, H,K, BUS_C

    if reg_bits & 0b1000000:
        MAR = BUS_C
    if reg_bits & 0b0100000:
        MDR = BUS_C
    if reg_bits & 0b0010000:
        PC = BUS_C
    if reg_bits & 0b0001000:
        X = BUS_C
    if reg_bits & 0b0000100:
        Y = BUS_C
    if reg_bits & 0b0000010:
        H = BUS_C
    if reg_bits & 0b0000001:
        K= BUS_C
    
def alu(control_bits):
    global N, Z, BUS_A, BUS_B, BUS_C

    a = BUS_A
    b = BUS_B
    o = 0

    shift_bits = (0b11000000 & control_bits) >> 6
    control_bits = 0b00111111 & control_bits
        
    if control_bits == 0b011000:
        o = a
    elif control_bits == 0b010100:
        o = b
    elif control_bits == 0b011010:
        o = ~a
    elif control_bits == 0b101100:
        o = ~b
    elif control_bits == 0b111100:
        o = a+b
    elif control_bits == 0b111101:
        o = a+b+1
    elif control_bits == 0b111001:
        o = a+1
    elif control_bits == 0b110101:
        o = b+1
    elif control_bits == 0b111111:
        o = b-a
    elif control_bits == 0b110110:
        o = b-1
    elif control_bits == 0b111011:
        o = -a
    elif control_bits == 0b001100:
        o = a & b
    elif control_bits == 0b011100:
        o = a | b
    elif control_bits == 0b010000:
        o = 0
    elif control_bits == 0b110001:
        o = 1
    elif control_bits == 0b110010:
        o = -1
    elif control_bits == 0b011001:
        o = a % b

    if o == 0:
        N = 0
        Z = 1
    else:
        N = 1
        Z = 0
        
    if shift_bits == 0b01:
        o = o << 1
    elif shift_bits == 0b10:
        o = o >> 1
    elif shift_bits == 0b11:
        o = o << 8
        
    BUS_C = o

def next_instruction(next, jam):
    global MPC, MBR, Z, N

    if jam == 0:
        MPC = next
        return
        
    if jam & 0b001:
        next = next | (Z << 8)

    if jam & 0b010:
        next = next | (N << 8)
        
    if jam & 0b100:
        next = next | MBR
        
    MPC = next

def memory_io(mem_bits):
    global PC, MBR, MDR, MAR

    if mem_bits & 0b001:
        MBR = memory.read_byte(PC)

    if mem_bits & 0b010:
        MDR = memory.read_word(MAR)
        
    if mem_bits & 0b100:
        memory.write_word(MAR, MDR)
        
def step():
    global MIR, MPC

    MIR = firmware[MPC]

    if MIR == 0:
        return False
        
    read_regs((MIR & 0b000000000000000000000000000000000111), ((MIR & 0b000000000000000000000000000000111000) >> 3))   
    alu((MIR & 0b000000000000111111110000000000000000) >> 16)
    write_regs((MIR & 0b000000000000000000001111111000000000) >> 9)
    memory_io((MIR & 0b000000000000000000000000000111000000) >> 6)
    next_instruction((MIR & 0b111111111000000000000000000000000000) >> 27, (MIR & 0b000000000111000000000000000000000000) >> 24)

    return True
