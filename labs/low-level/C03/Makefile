AS := as
LD := ld
.PHONY: all test inspect clean
all: copy
copy.o: copy.s
	$(AS) --64 -o $@ $<
copy: copy.o
	$(LD) -o $@ $<
test: copy
	python3 test.py
inspect: copy
	readelf -h -l copy
	objdump -d copy
clean:
	rm -f copy copy.o
