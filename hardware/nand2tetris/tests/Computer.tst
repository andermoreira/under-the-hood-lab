// Load a real binary program into ROM and execute it in the integrated Computer.
load ../Computer.hdl,
output-file Computer.out,
compare-to Computer.cmp,
output-list RAM16K[0]%D1.6.1 RAM16K[1]%D1.6.1;

ROM32K load ../programs/FillRAM.hack,
set reset 1,
tick,
tock,
set reset 0,
repeat 6 {
    tick,
    tock;
}
output;
