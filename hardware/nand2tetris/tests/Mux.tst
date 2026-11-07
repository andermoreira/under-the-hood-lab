load ../Mux.hdl,
output-file Mux.out,
compare-to Mux.cmp,
output-list a%B1.1.1 b%B1.1.1 sel%B1.1.1 out%B1.1.1;

set a 0, set b 0, set sel 0, eval, output;
set a 0, set b 0, set sel 1, eval, output;
set a 0, set b 1, set sel 0, eval, output;
set a 0, set b 1, set sel 1, eval, output;
set a 1, set b 0, set sel 0, eval, output;
set a 1, set b 0, set sel 1, eval, output;
set a 1, set b 1, set sel 0, eval, output;
set a 1, set b 1, set sel 1, eval, output;
