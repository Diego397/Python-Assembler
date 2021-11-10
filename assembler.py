import sys

fsrc = open(str(sys.argv[1]), 'r')

lines = []
lines_bin = []
names = []

instructions = ['add', 'sub', 'goto', 'mov', 'jz', 'halt', 'wb', 'ww', 'mult', 'div', 'lsh', 'rsh', 'blsh', 'set', 'and', 'mod']
instruction_set = {'addx'  : 0x02,
                   'addy'  : 0x11,
                   'subx'  : 0x0D,
                   'suby'  : 0x40,
                   'goto'  : 0x09, 
                   'movx'  : 0x06,
                   'movy'  : 0x32,
                   'jzx'   : 0x0B,
                   'jzy'   : 0x3E,
                   'halt'  : 0xFF,
                   'mult'  : 0x36,
                   'lshx'  : 0x22,
                   'lshy'  : 0x35,
                   'rsh'   : 0x23,
                   'blsh'  : 0x24,
                   'setx'  : 0x19,
                   'sety'  : 0x1D,
                   'div'   : 0x25,
                   'mod'   : 0x25,
                   'and'   : 0x2E}

def is_instruction(str):
   global instructions
   inst = False
   for i in instructions:
      if i == str:
         inst = True
         break
   return inst
   
def is_name(str):
   global names
   name = False
   for n in names:
      if n[0] == str:
         name = True
         break
   return name

def encode_mov(ops):
    line_bin = []
    if ops[0] == 'x':
        line_bin = []
        if is_name(ops[1]):
            line_bin.append(instruction_set['movx'])
            line_bin.append(ops[1])
    if ops[0] == 'y':
        if is_name(ops[1]):
            line_bin.append(instruction_set['movy'])
            line_bin.append(ops[1])
    return line_bin

def encode_add(ops):
   line_bin = []
   if len(ops) > 1:
      if ops[0] == 'x':
         if is_name(ops[1]):
            line_bin.append(instruction_set['addx'])
            line_bin.append(ops[1])
      if ops[0] == 'y':
         if is_name(ops[1]):
            line_bin.append(instruction_set['addy'])
            line_bin.append(ops[1])
   return line_bin

def encode_goto(ops):
   line_bin = []
   if len(ops) > 0:
      if is_name(ops[0]):
         line_bin.append(instruction_set['goto'])
         line_bin.append(ops[0])
   return line_bin
   
def encode_halt():
   line_bin = []
   line_bin.append(instruction_set['halt'])
   return line_bin

def encode_wb(ops):
   line_bin = []
   if len(ops) > 0:
      if ops[0].isnumeric():
         if int(ops[0]) < 256:
            line_bin.append(int(ops[0]))
   return line_bin   

def encode_ww(ops):
   line_bin = []
   if len(ops) > 0:
      if ops[0].isnumeric():
         val = int(ops[0])
         if val < pow(2,32):
            line_bin.append(val & 0xFF)
            line_bin.append((val & 0xFF00) >> 8)
            line_bin.append((val & 0xFF0000) >> 16)
            line_bin.append((val & 0xFF000000) >> 24)
   return line_bin

def encode_mult():
    line_bin = []
    line_bin.append(instruction_set['mult'])
    return line_bin

def encode_set(ops):
    line_bin = []
    if len(ops) > 1:
        if ops[0] == 'x':
            if is_name(ops[1]):
                line_bin.append(instruction_set['setx'])
                line_bin.append(ops[1])
        if ops[0] == 'y':
             if is_name(ops[1]):
                line_bin.append(instruction_set['sety'])
                line_bin.append(ops[1])
    return line_bin

def encode_sub(ops):
    line_bin = []
    if len(ops) > 1:
        if ops[0] == 'x':
            if is_name(ops[1]):
                line_bin.append(instruction_set['subx'])
                line_bin.append(ops[1])
        if ops[0] == 'y':
            if is_name(ops[1]):
                line_bin.append(instruction_set['suby'])
                line_bin.append(ops[1])
    return line_bin

def encode_jz(ops):
    line_bin = []
    if len(ops) > 1:
        if ops[0] == 'x':
            if is_name(ops[1]):
                line_bin.append(instruction_set['jzx'])
                line_bin.append(ops[1])
        if ops[0] == 'y':
            if is_name(ops[1]):
                line_bin.append(instruction_set['jzy'])
                line_bin.append(ops[1])
    return line_bin

def encode_div():
    line_bin = []
    line_bin.append(instruction_set['div'])
    return line_bin

def encode_and(ops):
    line_bin = []
    if len(ops) > 1:
        if is_name(ops[1]):
            line_bin.append(instruction_set['and'])
            line_bin.append(ops[1])
    return line_bin

def encode_lsh(ops):
    line_bin = []
    if ops[0] == 'x':
        line_bin.append(instruction_set['lshx'])
    if ops[0] == 'y':
        line_bin.append(instruction_set['lshy'])
    return line_bin

def encode_rsh(ops):
    line_bin = []
    if ops[0] == 'x':
        line_bin.append(instruction_set['rsh'])
    return line_bin

def encode_blsh(ops):
    line_bin = []
    if ops[0] == 'x':
        line_bin.append(instruction_set['blsh'])
    return line_bin

def encode_mod():
    line_bin = []
    line_bin.append(instruction_set['mod'])
    return line_bin

def encode_instruction(inst, ops):
    if inst == 'add':
        return encode_add(ops) 
    elif inst == 'mult':
        return encode_mult()
    elif inst == 'div':
        return encode_div()
    elif inst == 'set':
        return encode_set(ops)
    elif inst == 'sub':
        return encode_sub(ops)
    elif inst == 'mov':
        return encode_mov(ops)
    elif inst == 'and':
        return encode_and(ops)
    elif inst == 'jz':
        return encode_jz(ops)
    elif inst == 'lsh':
        return encode_lsh(ops)
    elif inst == 'rsh':
        return encode_rsh(ops)
    elif inst == 'blsh':
        return encode_blsh(ops)
    elif inst == 'mod':
        return encode_mod()
    elif inst == 'goto':
        return encode_goto(ops)
    elif inst == 'halt':
        return encode_halt()
    elif inst == 'wb':
        return encode_wb(ops)
    elif inst == 'ww':
        return encode_ww(ops)
    else:
        return []
   
   
def line_to_bin_step1(line):
   line_bin = []
   if is_instruction(line[0]):
      line_bin = encode_instruction(line[0], line[1:])
      print("instrucao = ", line[0], "  | operacao = ", line[1:])
   else:
      line_bin = encode_instruction(line[1], line[2:])
      print("instrucao = ", line[1], "  | operacao = ", line[2:])
   return line_bin
   
def lines_to_bin_step1():
   global lines
   for line in lines:
      line_bin = line_to_bin_step1(line)
      if line_bin == []:
         print("Erro de sintaxe na linha ", lines.index(line))
         print(line)
         return False
      lines_bin.append(line_bin)
   return True

def find_names():
   global lines
   for k in range(0, len(lines)):
      is_label = True
      for i in instructions:
          if lines[k][0] == i:
             is_label = False
             break
      if is_label:
         names.append((lines[k][0], k))
         
def count_bytes(line_number):
   line = 0
   byte = 1
   while line < line_number:
      byte += len(lines_bin[line])
      line += 1
   return byte

def get_name_byte(str):
   for name in names:
      if name[0] == str:
         return name[1]
         
def resolve_names():
   for i in range(0, len(names)):
      names[i] = (names[i][0], count_bytes(names[i][1]))
   for line in lines_bin:
      for i in range(0, len(line)):
         if is_name(line[i]):
            if line[i-1] in {instruction_set[x] for x in ['addx', 'addy', 'subx', 'suby', 'mult', 'setx', 'sety', 'div', 'and', 'movx', 'movy', 'lshx', 'lshy', 'rsh', 'blsh', 'mod']}:
               line[i] = get_name_byte(line[i])//4
            else:
               line[i] = get_name_byte(line[i])

for line in fsrc:
   tokens = line.replace('\n','').replace(',','').lower().split(" ")
   i = 0
   while i < len(tokens):
      if tokens[i] == '':
         tokens.pop(i)
         i -= 1
      i += 1
   if len(tokens) > 0:
      lines.append(tokens)
   
find_names()
if lines_to_bin_step1():
   resolve_names()
   byte_arr = [0]
   for line in lines_bin:
      for byte in line:
         byte_arr.append(byte)
   for i in range (len(lines_bin)):
      print(i, lines_bin[i])
   fdst = open(str(sys.argv[2]), 'wb')
   fdst.write(bytearray(byte_arr))
   fdst.close()

fsrc.close()