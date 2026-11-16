load ../Memory.hdl,
output-file Memory.out,
compare-to Memory.cmp,
output-list in%D1.6.1 load%B1.1.1 address%D1.5.1 out%D1.6.1;

set in 1234, set load 1, set address 0, tick, tock, output;
set in 0, set load 0, set address 0, tick, tock, output;
set in 4321, set load 1, set address 16383, tick, tock, output;
set in 0, set load 0, set address 16383, tick, tock, output;
set in 5678, set load 1, set address 16384, tick, tock, output;
set in 0, set load 0, set address 16384, tick, tock, output;
set in 0, set load 0, set address 0, tick, tock, output;
