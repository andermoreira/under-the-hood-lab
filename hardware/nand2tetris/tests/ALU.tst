load ../ALU.hdl,
output-file ALU.out,
compare-to ALU.cmp,
output-list x%X1.4.1 y%X1.4.1 zx%B1.1.1 nx%B1.1.1 zy%B1.1.1 ny%B1.1.1 f%B1.1.1 no%B1.1.1 out%X1.4.1 zr%B1.1.1 ng%B1.1.1;

set x %X0000, set y %X0000, set zx 1, set nx 0, set zy 1, set ny 0, set f 1, set no 0, eval, output;
set x %X1234, set y %Xabcd, set zx 1, set nx 1, set zy 1, set ny 1, set f 1, set no 1, eval, output;
set x %X1234, set y %Xabcd, set zx 0, set nx 0, set zy 1, set ny 1, set f 0, set no 0, eval, output;
set x %X1234, set y %Xabcd, set zx 1, set nx 1, set zy 0, set ny 0, set f 0, set no 0, eval, output;
set x %X1234, set y %Xabcd, set zx 0, set nx 0, set zy 0, set ny 0, set f 1, set no 0, eval, output;
set x %X1234, set y %Xabcd, set zx 0, set nx 0, set zy 0, set ny 0, set f 0, set no 0, eval, output;
set x %X1234, set y %Xabcd, set zx 0, set nx 1, set zy 0, set ny 1, set f 0, set no 1, eval, output;
set x %X1234, set y %Xabcd, set zx 0, set nx 1, set zy 0, set ny 0, set f 1, set no 1, eval, output;
set x %X1234, set y %Xabcd, set zx 0, set nx 0, set zy 0, set ny 1, set f 1, set no 1, eval, output;
set x %X7fff, set y %X0001, set zx 0, set nx 0, set zy 0, set ny 0, set f 1, set no 0, eval, output;
set x %Xffff, set y %X0001, set zx 0, set nx 0, set zy 0, set ny 0, set f 1, set no 0, eval, output;
set x %X8000, set y %X0000, set zx 0, set nx 0, set zy 1, set ny 1, set f 0, set no 0, eval, output;
set x %X0000, set y %X0000, set zx 1, set nx 1, set zy 1, set ny 1, set f 1, set no 0, eval, output;
set x %X0000, set y %X0000, set zx 1, set nx 1, set zy 1, set ny 0, set f 1, set no 0, eval, output;
set x %X1234, set y %Xabcd, set zx 0, set nx 0, set zy 1, set ny 1, set f 0, set no 1, eval, output;
set x %X1234, set y %Xabcd, set zx 1, set nx 1, set zy 0, set ny 0, set f 0, set no 1, eval, output;
set x %X1234, set y %Xabcd, set zx 0, set nx 0, set zy 1, set ny 1, set f 1, set no 1, eval, output;
set x %X1234, set y %Xabcd, set zx 1, set nx 1, set zy 0, set ny 0, set f 1, set no 1, eval, output;
