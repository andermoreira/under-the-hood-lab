load ../Mux4Way16.hdl,
output-file Mux4Way16.out,
compare-to Mux4Way16.cmp,
output-list a%D1.6.1 b%D1.6.1 c%D1.6.1 d%D1.6.1 sel%D1.1.1 out%D1.6.1;

set a 1, set b 2, set c 4, set d 8, set sel 0, eval, output;
set a 1, set b 2, set c 4, set d 8, set sel 1, eval, output;
set a 1, set b 2, set c 4, set d 8, set sel 2, eval, output;
set a 1, set b 2, set c 4, set d 8, set sel 3, eval, output;
set a 0, set b 65535, set c 43690, set d 21845, set sel 0, eval, output;
set a 0, set b 65535, set c 43690, set d 21845, set sel 1, eval, output;
set a 0, set b 65535, set c 43690, set d 21845, set sel 2, eval, output;
set a 0, set b 65535, set c 43690, set d 21845, set sel 3, eval, output;
