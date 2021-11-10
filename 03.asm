goto main
     wb 0

RES  ww 1
AUX  ww 0
THR  ww 3
TWO  ww 2
ONE  ww 1
ZERO ww 0

main   set y, RES
       set x, TWO
       mod
       jz x, auxp

auxi   set x, RES
       sub x, ONE
       jz x, nprim
       sub x, ONE

impar  mov x, AUX
       sub x, ONE
       jz x, prim
       add x, ONE
       mod
       jz x, nprim
       set x, AUX
       sub x, TWO
       goto impar

auxp   sub y, TWO
       jz y, prim
       goto nprim

prim   set x, ONE
       mov x, RES
       halt

nprim  set x, ZERO
       mov x, RES
       halt