load ../Mux16.hdl,
output-file Mux16.out,
compare-to Mux16.cmp,
output-list a%D1.6.1 b%D1.6.1 sel%B1.1.1 out%D1.6.1;

set a 0, set b 65535, set sel 0, eval, output;
set a 0, set b 65535, set sel 1, eval, output;
set a 43690, set b 21845, set sel 0, eval, output;
set a 43690, set b 21845, set sel 1, eval, output;
