Diego Alejandro Balejo Cardozo Rey - 495908
Marcus Vinícius Paz Barros - 495682

Alterações no Firmware:
Adicionamos um novo barramento;
Adicionamos um novo registrador 'K';

Criamos diversas funções para nos auxiliaram na resolução das questões, dentre elas estão:

Soma para X: firmware[2]  : X = X + mem[address];
Soma para Y: firmware[17] : Y = Y + mem[address];

Mov para  X: firmware[6]  : mem[address] = X;
Mov para  Y: firmware[50] : mem[address] = Y;

Goto       : firmware[9]  : goto adress;

jz  para  X: firmware[10] : if X = 0 goto address;
jz  para  Y: firmware[62] : if Y = 0 goto address;

Sub para  X: firmware[13] : X = X - mem[address];
Sub para  Y: firmware[64] : Y = Y - mem[address];

Set para  X: firmware[25] : X = mem[address];
Set para  Y: firmware[29] : Y = mem[address];

Lsh para  X: firmware[34] : X = X << 1; (left shift bit)
Lsh para  Y: firmware[53] : Y = Y << 1; (left shift bit)
Lsh para  X: firmware[35] : X = X >> 1; (right shift bit)
Bsh para  X: firmware[36] : X = X << 8; (left shift byte)

And para X:  firmware[46] : X = X & mem[address];

Mult       : firmware[54] : X = X * Y:

	54		H = 0 					; GOTO 55
	55		K = 1					; GOTO 56
	56		K = X & K	 			; GOTO 57
	57		IF K = 0, 	GOTO 314	        ; ELSE GOTO 58
	58 		H <- H + Y 				; GOTO 314
	314		Y = Y << 1 				; GOTO 60
	60		X = X >> 1 				; GOTO 61
	61		IF X = 0, 	GOTO 311	; ELSE GOTO 55
	311		X = H 					; Halt

Mod			: firmware[37] : X = Y % X; (X = resto(Y / X))
	
	Criação da ALU : 0b011001
	O circuito para tal funcão está no arquivo mod.pdf

	Fariamos um circuito muito parecido com a divisão. Porém, a saída será somente o resto da divisão.

	Esse circuito faz o seguinte: como exemplo, usaremos Dividendo = 1111 (A4 = 1, A3 = 1, A2 = 1, A1 = 1) e Divisor 0110
	
	1. Pegamos o bit mais significativo do dividendo (A4), que é 1 e vamos ver quantas vezes o divisor (0110) cabe nesse numero (A4). Como 0110 é maior que 1, o dividendo não divide o (A4). Assim, como o dividendo não divide o A4, o bit mais significativo do nosso quociente será 0 (Q4).
	
	2. Multiplicamos o divisor com Q4. Se Q4 for 0, o resultado será 0, se Q4 for 1, o resultado será o próprio divisor. Como no nosso exemplo Q4 = 0, temos que o resultado dessa multiplicação é 0.
	
	3. Subtraimos o A4 pelo resultado anterior, que é zero. Logo, temos que 1 (A4) - 0 = 1. O resultado dessa subtração é a primeira parte da parte temporaria do dividendo. A Segunda parte vem da adição do A3 no fim da parte temporaria do dividendo. Isso resulta na parte temporaria do dividendo sendo igual a 11

    4. Agora vemos quantas vezes conseguimos dividir essa parte temporaria do dividendo (11) pelo divisor (0110). De novo, não conseguimos dividir nenhuma vez. Assim, temos nosso segundo bit da esquerda do cociente (Q3).

    5. Agora basta repetirmos esse processo até que tenhamos calculado todos os bits do quociente.
		
    6. E no final, se ficarmos com um numero maior que zero após fazermos a ultima divisão, teremos que o resto é maior que zero. No nosso exemplo, o resto dessa divisão é 0011.

É isso que ultilizaremos para criar a função mod na ALU, ao criarmos esse circuito de divisão, vamos pegar somente o resto dele e descartar o resultado.
