load ../CPU.hdl,
output-file CPU.out,
compare-to CPU.cmp,
output-list instruction%B1.16.1 inM%D1.6.1 reset%B1.1.1 outM%D1.6.1 writeM%B1.1.1 addressM%D1.5.1 pc%D1.5.1;

set instruction %B0000000000000111, set inM 0, set reset 0, tick, tock, output;
set instruction %B1110110000010000, set inM 0, set reset 0, tick, tock, output;
set instruction %B0000000000000101, set inM 0, set reset 0, tick, tock, output;
set instruction %B1110000010010000, set inM 0, set reset 0, tick, tock, output;
set instruction %B0000000000011001, set inM 0, set reset 0, tick, tock, output;
set instruction %B1110101010000111, set inM 0, set reset 0, tick, tock, output;
