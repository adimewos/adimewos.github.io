---
layout: post
title: Learn Format String Attacks
description: "Introduction to Format String Attacks on x86 Linux"
date: 2017-06-24 18:31:31 +0800
tags: [x86, pwn, stack, fsb, notes]
comments: true
share: true
---

## Introduction
Format string vulnerabilities are still able to be found in programs these days, as programmers are normally not taught the consequences of using the format string functions wrongly. 

### What is a format string vulnerability then?
We have used `printf` and `scanf` before, but have you ever tried doing `printf(string)` instead of `printf("%s", string)`?

Such incorrect usage of format string functions introduces attacks to the binary, as the string may contain format specifiers like `%s` or `%d`, and these specifiers cause the program to think that there are more arguments down the stack for the function, which may not actually be intended for the function.

The format specifier `$n` now comes to play, and what this does is write the amount of currently written bytes into the given address. For example, in `printf("1234567%n", &count)`, `count = 7`. This is problematic as it allows the attacker to write whatever they want into any address they want.

The following materials will further illustrate on how to perform this attack, more particularly on the GOT and the .dtors section.

## Reading Materials
### Hacking: The Art of Exploitation (0x350)
#### Techniques Covered
* Reading from arbitrary memory addresses
* Writing to arbitrary memory addresses
* Using direct parameter access
* Using short writes
* Writing to .dtors and GOT

### Some extra materials
Some [slides](http://security.cs.rpi.edu/courses/binexp-spring2015/lectures/9/06_lecture.pdf) and another [tutorial](https://www.exploit-db.com/docs/28476.pdf). They contain similar content to the one above.

### Cool Tricks
We can do a lot with format string attacks, as we basically are able to overwrite the GOT and take control of the program execution, and leak out whatever addresses we like.

#### Leak addresses
Sometimes we may need the address of the stack, when dealing with executable-stack challenges where our shellcode is located on the stack. 

Or, in the future, when dealing with more realistic challenges where the stack is not executable, we can leak the address of `libc` when there is ASLR to perform ROP. (Don't worry, ROP and ASLR will be covered later)

#### Create a loop
Well when there is ASLR, we need to send in our exploit once we leaked the addresses of interest, thus we cannot let the program terminate so soon. To solve this problem, we can just overwrite an insignificant function in the GOT to the part of the program that we would like to repeat, creating a loop for ourselves.

## Practices
I recommend to practice in the following order.

### Protostar
Plenty of challenges can be found on [protostar](https://exploit-exercises.com/protostar/). The knowledge above should be sufficient to complete `format0` to `format4`.

### Narnia
[Narnia](overthewire.org/wargames/narnia/) also contains some format string attack challenges, namely `narnia5` and `narnia7`.

### MBE
Lab04 of [MBE](https://github.com/RPISEC/MBE) is also pretty good practice.

### Final1
When you are done with the above practice challenges, try [Final1](https://exploit-exercises.com/protostar/final1/) from protostar, which is a blind format string attack challenge. I promise it'll be very fun.

## Final Notes
As most programmers aren't told that doing `printf(string)` is bad, it is still possible to find format string vulnerabilities in poorly written programs.

Format string attacks are interesting as it allows us to change the control flow of the program, and leak the addresses that we need to perform attacks.
