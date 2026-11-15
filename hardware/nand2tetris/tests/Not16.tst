load ../Not16.hdl,
output-file Not16.out,
compare-to Not16.cmp,
output-list in%D1.6.1 out%D1.6.1;

set in 0, eval, output;
set in 65535, eval, output;
set in 43690, eval, output;
set in 21845, eval, output;
