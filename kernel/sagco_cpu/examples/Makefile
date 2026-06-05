# Makefile for SAGCO CPU Examples

CC = gcc
CFLAGS = -Wall -Wextra -O2
LDFLAGS =

EXAMPLES = test_sagco

all: $(EXAMPLES)

test_sagco: test_sagco.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

clean:
	rm -f $(EXAMPLES) *.o

run: test_sagco
	@echo "Running SAGCO CPU test suite..."
	@echo "Note: Requires sudo and loaded kernel module"
	sudo ./test_sagco

.PHONY: all clean run
