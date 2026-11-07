load ../Register.hdl,
output-file Register.out,
compare-to Register.cmp,
output-list in%X1.4.1 load%B1.1.1 out%X1.4.1;

set in %X0000, set load 0, tick, tock, output;
set in %X1234, set load 1, tick, tock, output;
set in %Xffff, set load 0, tick, tock, output;
set in %X8001, set load 1, tick, tock, output;
set in %X0000, set load 0, tick, tock, output;
