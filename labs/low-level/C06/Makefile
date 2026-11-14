CC := gcc
CFLAGS := -std=c11 -O2 -g -Wall -Wextra -Werror
.PHONY: all test inspect clean
all: memory
memory: memory.c
	$(CC) $(CFLAGS) -o $@ $<
test: memory
	python3 test.py
inspect: memory
	readelf -h -l -S memory
clean:
	rm -f memory
