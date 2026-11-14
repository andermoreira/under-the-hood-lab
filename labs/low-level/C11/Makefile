CC := gcc
CFLAGS := -std=c11 -O2 -Wall -Wextra -Werror
.PHONY: all test inspect clean
all: dynamic static
dynamic: main.c
	$(CC) $(CFLAGS) -o $@ $<
static: main.c
	$(CC) $(CFLAGS) -static -o $@ $<
test: all
	python3 test.py
inspect: all
	readelf -l dynamic
	readelf -l static
	readelf -d dynamic
clean:
	rm -f dynamic static
