load ../PC.hdl,
output-file PC.out,
compare-to PC.cmp,
output-list in%X1.4.1 load%B1.1.1 inc%B1.1.1 reset%B1.1.1 out%X1.4.1;

set in %X0063, set load 0, set inc 0, set reset 0, tick, tock, output;
set in %X0063, set load 0, set inc 1, set reset 0, tick, tock, output;
set in %X1234, set load 1, set inc 1, set reset 0, tick, tock, output;
set in %X0000, set load 0, set inc 1, set reset 0, tick, tock, output;
set in %X9999, set load 1, set inc 1, set reset 1, tick, tock, output;
set in %Xffff, set load 1, set inc 0, set reset 0, tick, tock, output;
set in %X0000, set load 0, set inc 1, set reset 0, tick, tock, output;
set in %X0000, set load 0, set inc 0, set reset 0, tick, tock, output;
set in %X5555, set load 1, set inc 0, set reset 0, tick, tock, output;
set in %X0000, set load 0, set inc 0, set reset 1, tick, tock, output;
