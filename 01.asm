goto main
     wb 0

RES  ww 6
ONE  ww 1
B    ww 0
AUX  ww 1

main set x, RES
     set y, RES
loop sub y, ONE
     jz y, fim
     mov y, AUX
     mult X
     set y, AUX
     goto loop
     mov x, RES

fim  mov x, RES
     halt