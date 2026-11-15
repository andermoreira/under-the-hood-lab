load ../DMux4Way.hdl,
output-file DMux4Way.out,
compare-to DMux4Way.cmp,
output-list in%B1.1.1 sel%D1.1.1 a%B1.1.1 b%B1.1.1 c%B1.1.1 d%B1.1.1;

set in 0, set sel 0, eval, output;
set in 1, set sel 0, eval, output;
set in 1, set sel 1, eval, output;
set in 1, set sel 2, eval, output;
set in 1, set sel 3, eval, output;
set in 0, set sel 3, eval, output;
