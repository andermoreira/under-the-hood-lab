.PHONY: test verify test-hdl-offline test-hdl-official test-assembler test-kernel-build test-kernel-boot verify-kernel-docker
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

test-kernel-build:
	bash scripts/build-kernel.sh

test-kernel-boot: test-kernel-build
	bash scripts/test-kernel-boot.sh

# Local kernel verification inside a container that mirrors the CI toolchain
# (cross GCC + QEMU + Limine). Needed on hosts without an x86_64-elf toolchain
# or QEMU (e.g. macOS). Builds the image on first use.
verify-kernel-docker:
	docker build -f scripts/verify.Dockerfile -t uth-verify .
	docker run --rm -v "$(CURDIR)":/work uth-verify bash -c '\
		ln -sf /usr/bin/x86_64-linux-gnu-objdump /usr/local/bin/objdump; \
		export PATH=/usr/local/bin:$$PATH; \
		bash scripts/build-kernel.sh && bash scripts/test-kernel-boot.sh'
