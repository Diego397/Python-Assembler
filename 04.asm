goto main
     wb 0

RES  ww 7
A    ww 1
B    ww 0

main set x, RES
     set y, B

test sub x, A
     jz x, fim
     add x, A

log  rsh x
     add y, A
     sub x, A
     jz x, fim
     add x, A
     goto log

fim  mov y, RES
     halt