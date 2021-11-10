import cpu as cpu
import sys
import memory as mem
import clock as clk 
import disk

disk.read(str(sys.argv[1]))

# print("Antes: ", mem.read_word(1))

# clk.start([cpu])

# print("Depois: ", mem.read_word(1))

print(f"Antes: X = {cpu.X}, Y = {cpu.Y}, H = {cpu.H}, mem(1) = {mem.read_word(1)}")

clk.start([cpu])

print(f"Depois: X = {cpu.X}, Y = {cpu.Y}, H = {cpu.H}, mem(1) = {mem.read_word(1)}")