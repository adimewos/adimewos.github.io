#!/usr/bin/python2

import sys
import random

s = '7c153a474b6a2d3f7d3f7328703e6c2d243a083e2e773c45547748667c1511333f4f745e'.decode('hex')

# part 1: remove chaining encryption
dec1 = [ord(c) for c in s]
for i in range(len(s) - 1, 1, -1):
	dec1[i] = (dec1[i] - dec1[i-1]) % 128
dec1 = dec1[1:]

# part 2: recover key since we know that 23rd character is '|'
key = [0] * 13
c = len(dec1) - 13 - 1
key[c % 13] = (dec1[c] - ord('|')) % 128

for _ in range(12):
	c = (c % 13) + len(dec1) - 13
	key[c % 13] = (dec1[c] - key[(c - (len(dec1) - 13))]) % 128

message = ''
for i in range(0, len(dec1)):
	message += chr((dec1[i] - key[i % len(key)]) % 128)

print message
