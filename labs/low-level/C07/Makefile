CC := gcc
CFLAGS := -std=c11 -O2 -g -Wall -Wextra -Werror
.PHONY: all test inspect clean
all: flags-demo
flags-demo: main.c flags.s
	$(CC) $(CFLAGS) -o $@ $^
test: flags-demo
	python3 test.py
inspect: flags-demo
	objdump -d flags-demo
clean:
	rm -f flags-demo
