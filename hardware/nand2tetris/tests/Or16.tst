load ../Or16.hdl,
output-file Or16.out,
compare-to Or16.cmp,
output-list a%D1.6.1 b%D1.6.1 out%D1.6.1;

set a 0, set b 65535, eval, output;
set a 65535, set b 0, eval, output;
set a 43690, set b 21845, eval, output;
set a 43690, set b 61680, eval, output;
