CC := gcc
CFLAGS := -std=c11 -O2 -g -Wall -Wextra -Werror -fno-pie
LDFLAGS := -no-pie
.PHONY: all test inspect clean
all: abi-demo
abi.o: abi.s
	$(CC) -c -o $@ $<
main.o: main.c
	$(CC) $(CFLAGS) -c -o $@ $<
abi-demo: main.o abi.o
	$(CC) $(LDFLAGS) -o $@ $^
test: abi-demo
	python3 test.py
inspect: abi-demo
	readelf -h -s abi-demo
	objdump -d abi-demo
clean:
	rm -f abi-demo main.o abi.o
