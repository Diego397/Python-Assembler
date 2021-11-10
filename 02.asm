goto main
     wb 0

RES  ww 10
VA1  ww 0
VA2  ww 1
SMA  ww 0
AX1  ww 1
TMP  ww 0

main  set x, RES
      sub x, AX1
      jz x, fim
      sub x, AX1
      jz x, fimb

fib   add y, VA1
      add y, VA2
      mov y, SMA
      sub x, AX1
      jz  x, fim
      set y, VA2
      mov y, VA1
      set y, SMA
      mov y, VA2
      set y, TMP
      goto fib

fimb  set y, VA2
      mov y, RES
      halt

fim   set y, SMA
      mov y, RES
      halt
