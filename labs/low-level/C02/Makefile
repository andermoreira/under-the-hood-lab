AS := as
LD := ld
READELF := readelf
OBJDUMP := objdump

.PHONY: all test inspect clean
all: anatomy

anatomy.o: anatomy.s
	$(AS) --64 -o $@ $<

anatomy: anatomy.o
	$(LD) -o $@ $<

test: anatomy
	python3 test.py

inspect: anatomy
	$(READELF) -h -S -l -s anatomy
	$(OBJDUMP) -d anatomy

clean:
	rm -f anatomy anatomy.o
