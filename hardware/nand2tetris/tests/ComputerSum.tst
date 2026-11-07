// Integration: assemble source, load binary into ROM, execute a counted loop.
load ../Computer.hdl,
output-file ComputerSum.out,
compare-to ComputerSum.cmp,
output-list RAM16K[0]%D1.6.1 RAM16K[1]%D1.6.1 RAM16K[2]%D1.6.1;

ROM32K load ../programs/Sum1To5.hack,
set reset 1,
tick,
tock,
set reset 0,
repeat 100 {
    tick,
    tock;
}
output;
