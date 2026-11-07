load ../RAM64.hdl,
output-file RAM64.out,
compare-to RAM64.cmp,
output-list in%X1.4.1 load%B1.1.1 address%D1.6.1 out%X1.4.1;

set in %X1234, set load 1, set address 0, tick, tock, output;
set in %X5555, set load 1, set address 1, tick, tock, output;
set in %Xabcd, set load 1, set address 63, tick, tock, output;
set in %Xffff, set load 0, set address 0, tick, tock, output;
set in %X0000, set load 0, set address 63, tick, tock, output;
set in %X8001, set load 1, set address 32, tick, tock, output;
set in %X0000, set load 0, set address 0, tick, tock, output;
