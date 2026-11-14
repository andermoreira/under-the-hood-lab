AS := as
LD := ld
OBJDUMP := objdump
READELF := readelf

.PHONY: all test inspect clean
all: hello

hello.o: hello.s
	$(AS) --64 -o $@ $<

hello: hello.o
	$(LD) -o $@ $<

test: hello
	python3 test.py

inspect: hello
	$(READELF) -h hello
	$(OBJDUMP) -d hello

clean:
	rm -f hello hello.o
