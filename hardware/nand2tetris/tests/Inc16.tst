load ../Inc16.hdl,
output-file Inc16.out,
compare-to Inc16.cmp,
output-list in%X1.4.1 out%X1.4.1;

set in %X0000, eval, output;
set in %X0001, eval, output;
set in %X00ff, eval, output;
set in %Xffff, eval, output;
