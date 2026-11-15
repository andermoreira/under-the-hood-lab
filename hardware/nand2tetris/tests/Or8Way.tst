load ../Or8Way.hdl,
output-file Or8Way.out,
compare-to Or8Way.cmp,
output-list in%D1.6.1 out%B1.1.1;

set in 0, eval, output;
set in 1, eval, output;
set in 128, eval, output;
set in 16, eval, output;
set in 255, eval, output;
set in 170, eval, output;
