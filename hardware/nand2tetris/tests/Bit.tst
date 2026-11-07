load ../Bit.hdl,
output-file Bit.out,
compare-to Bit.cmp,
output-list in%B1.1.1 load%B1.1.1 out%B1.1.1;

set in 0, set load 0, tick, tock, output;
set in 1, set load 1, tick, tock, output;
set in 0, set load 0, tick, tock, output;
set in 0, set load 1, tick, tock, output;
set in 1, set load 0, tick, tock, output;
