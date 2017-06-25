---
layout: post
title: Learn Shellcoding
permalink: /notes/learn-shellcoding
description: "Introduction to Shellcoding on x86 Linux"
date: 2017-06-24 10:03:23 +0800
tags: [x86, pwn, stack, shellcoding, notes]
comments: true
share: true

---

This post is a continuation of the [Learn Buffer Overflow](https://dowsll.github.io/2017-06-24/Learn-Buffer-Overflow/) post, but covers more on crafting our shellcode than just using shellcode from shellstorm or exploit-db.

If you do not know what is a buffer overflow vulnerability, please have a look at my previous post first.

## Introduction
When we first learnt about buffer overflows with nop sled and shellcode, we just used a shellcode taken from online, that spawn a shell when arbitrary code execution is gained.

However, it is normally not that easy, as mitigations can be made by the programmer to stop us from spawning our shell, or we can be more creative with our shellcoding like spawning a reverse shell instead, which tries to connect to a listening port on the attacker's machine.

## Reading materials
### Hacking: The Art of Exploitation 2nd Edition (Part 0x500)
This book teaches most of the things we need to know about shellcoding.
#### Techniques covered
* Assembly programming
* Tricks to avoid null bytes in shellcoding
* Tricks to shorten shellcode
* Shell-spawning shellcode
* Port-binding and connect-back shellcode

### Slides by RPISEC/MBE
Slides [here](http://security.cs.rpi.edu/courses/binexp-spring2015/lectures/7/05_lecture.pdf)

## Tools
* strace - Run `strace` while sending the input into the program to check if the shellcode is being executed.
* [Online x86 Assembler/Disassembler](https://defuse.ca/online-x86-assembler.htm) - You can use this if you are lazy to compile assembly, then link it, then... So many steps...
* [Shellcode testing tool](https://github.com/hellman/shtest) - Test your shellcode to make sure it works!

## Practice
### MBE
Their [repository](https://github.com/RPISEC/MBE) has a nice set of instructions to set up the wargame VM. Once done with that, head on to finish Lab03. I guarantee you can't just use an `execve /bin/sh` shellcode found online.

If you are stuck with the challenges, don't forget to use `strace` to see if your shellcode is being executed.

## Final Notes
Knowing how to create our own shellcode is very important, so that we can craft different shellcodes for different situations or to bypass certain mitigations.

Also, shellcoding prepares us for Return-oriented Programming, which is a very smart way to bypass Data Execution Prevention, as programs are normally compiled without the stack being executable.
