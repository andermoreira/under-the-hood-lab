AS := as
LD := ld
.PHONY: all test inspect clean
all: echo cat wc
%.o: %.s
	$(AS) --64 -o $@ $<
echo cat wc: %: %.o
	$(LD) -o $@ $<
test: all
	python3 test.py
inspect: all
	@for bin in echo cat wc; do readelf -h $$bin; objdump -d $$bin; done
clean:
	rm -f echo cat wc echo.o cat.o wc.o
