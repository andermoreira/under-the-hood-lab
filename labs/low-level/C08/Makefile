CC := gcc
CFLAGS := -std=c11 -O2 -Wall -Wextra -Werror
.PHONY: all test clean
all: benchmark
benchmark: benchmark.c
	$(CC) $(CFLAGS) -o $@ $<
test: benchmark
	python3 test.py
clean:
	rm -f benchmark
