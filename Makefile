.PHONY: test verify test-hdl-offline test-hdl-official
test:
	python3 -m unittest discover -s tests -v
test-hdl-offline:
	python3 tools/verify_hdl.py
test-hdl-official:
	bash scripts/test-hdl.sh
verify: test test-hdl-offline
