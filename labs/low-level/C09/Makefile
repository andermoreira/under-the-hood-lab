CC := gcc
CFLAGS := -std=c11 -O0 -g -Wall -Wextra -Werror
.PHONY: all test inspect clean
all: crash
crash: crash.c
	$(CC) $(CFLAGS) -o $@ $<
test: crash
	python3 test.py
inspect: crash
	gdb -q -batch -ex "set pagination off" -ex "run abort" -ex "bt" --args ./crash abort
clean:
	rm -f crash
