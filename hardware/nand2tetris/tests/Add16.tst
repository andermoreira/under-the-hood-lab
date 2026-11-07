load ../Add16.hdl,
output-file Add16.out,
compare-to Add16.cmp,
output-list a%X1.4.1 b%X1.4.1 out%X1.4.1;

set a %X0000, set b %X0000, eval, output;
set a %X00ff, set b %X0001, eval, output;
set a %Xffff, set b %X0001, eval, output;
set a %X7fff, set b %X0001, eval, output;
set a %X8000, set b %X8000, eval, output;
set a %Xaaaa, set b %X5555, eval, output;
set a %Xffff, set b %Xffff, eval, output;
set a %X0001, set b %X0001, eval, output;
