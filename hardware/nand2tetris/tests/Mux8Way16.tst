load ../Mux8Way16.hdl,
output-file Mux8Way16.out,
compare-to Mux8Way16.cmp,
output-list a%D1.6.1 b%D1.6.1 c%D1.6.1 d%D1.6.1 e%D1.6.1 f%D1.6.1 g%D1.6.1 h%D1.6.1 sel%D1.1.1 out%D1.6.1;

set a 11, set b 22, set c 33, set d 44, set e 55, set f 66, set g 77, set h 88, set sel 0, eval, output;
set a 11, set b 22, set c 33, set d 44, set e 55, set f 66, set g 77, set h 88, set sel 1, eval, output;
set a 11, set b 22, set c 33, set d 44, set e 55, set f 66, set g 77, set h 88, set sel 2, eval, output;
set a 11, set b 22, set c 33, set d 44, set e 55, set f 66, set g 77, set h 88, set sel 3, eval, output;
set a 11, set b 22, set c 33, set d 44, set e 55, set f 66, set g 77, set h 88, set sel 4, eval, output;
set a 11, set b 22, set c 33, set d 44, set e 55, set f 66, set g 77, set h 88, set sel 5, eval, output;
set a 11, set b 22, set c 33, set d 44, set e 55, set f 66, set g 77, set h 88, set sel 6, eval, output;
set a 11, set b 22, set c 33, set d 44, set e 55, set f 66, set g 77, set h 88, set sel 7, eval, output;
