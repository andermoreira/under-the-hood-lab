.PHONY: test verify test-hdl-offline test-hdl-official test-assembler
test:
	python3 -m unittest discover -s tests -v
test-hdl-offline:
	python3 tools/verify_hdl.py
test-hdl-official:
	bash scripts/test-hdl.sh
test-assembler:
	python3 tools/hack_assembler.py hardware/nand2tetris/programs/FillRAM.asm -o /tmp/under-the-hood-FillRAM.hack
	cmp /tmp/under-the-hood-FillRAM.hack hardware/nand2tetris/programs/FillRAM.hack
verify: test test-hdl-offline test-assembler
