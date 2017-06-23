---
layout: post
title: Learn Buffer Overflow
description: "Introduction to Buffer Overflows on x86 Linux"
date: 2017-06-24
tags: [x86, pwn, stack]
comments: true
share: true
---

This post will be a compilation of resources and challenges to learn buffer overflow.
If you have no experience with reverse engineering x86 binaries, you can refer to my previous [post](https://dowsll.github.io/2017-06-17/Learn-Reverse-Engineering/) on learning reverse engineering.

This post is intended for beginners that are new to the concept of buffer overflows. To be more precise, stack-based buffer overflow.

## Learn Buffer Overflow
In short, buffer overflow occurs when the programmer reads input into a buffer that has a size smaller than the received input. For example, I have a char[] of size 100, but I read in 200 bytes. Basically bad programming.

## Reading materials
### Hacking: The Art of Exploitation (pages 119-167, 0x320 to 0x342)

This basically covers most of the stuff you need to know about buffer overflow vulnerabilities, and related methods to exploit it to gain remote code execution.

#### Techniques covered
* Buffer overflow to overwrite variables for authentication
* Buffer overflow with nop sled and shellcode
* Buffer overflow with environment variables
* Buffer overflow in the heap

### [Slides by RPISEC/MBE](http://security.cs.rpi.edu/courses/binexp-spring2015/lectures/5/04_lecture.pdf) 

Some slides if you want a more visual guide.

### [Smashing the Stack for Fun and Profit - setuid, ssh and exploit-exercises.com](https://www.youtube.com/watch?v=Y-4WHf0of6Y) 

Some knowledge about setuid binaries, how to ssh into a remote server, and how to set up the protostar vm.

## Practice
Now it's time for some practice.

### Protostar
[Protostar](https://exploit-exercises.com/protostar/) is the best place to start with. Following the video above, you should be able to set up your protostar VM.
You should be able to complete stack1 to stack5.

If you are stuck, refer back to the book, which should contain what you need to know. If you are really stuck, you can refer to guides by [LiveOverflow](http://liveoverflow.com/binary_hacking/index.html) (starting from 0x0C)

### Narnia
[Narnia](http://overthewire.org/wargames/narnia/) is a really nice wargame for you to practice your skills as a beginner. It is slightly harder than protostar as it does not have hints.

You should be able to work on narnia0 to narnia4.

If you are stuck with the challlenges, there is an IRC where you can seek help from. I am usually online there with username dows.

### MBE
If you followed my previous post, there is a link to [MBE](https://github.com/RPISEC/MBE) and instructions on setting up the VM are provided there.

MBE labs are also very good at testing the understanding of a concept, with increasing difficulty, so be sure to finish up Lab02.

## Final notes
Buffer overflow is one of the vulnerabilities found in programs, and there are still way more to learn. 

### DEP
While it's fun injecting shellcode and running them, OS developers are definitely not dumb and have came up with mitigations such as [DEP](https://en.wikipedia.org/wiki/Executable_space_protection), where not all parts of a binary are executable.

#### Does that mean no more remote code execution through buffer overflows?
Well DEP does prevent us from redirecting eip to run our shellcode, it doesn't stop us from writing stuff. So, through another smart technique called [ROP](https://en.wikipedia.org/wiki/Return-oriented_programming) that still allows us to make use of the code present in the binary. Don't worry, more of these will be covered later.

### Heap-based buffer overflow
If you've realised, all of the challenges are stack-based. This is because the eip is located in the stack and so it can be easily overwritten to gain arbitrary code execution.

Heap-based buffer overflows do not have access to the return address in the stack, and hence heap-based exploits require making use of holes in the heap implementation to gain arbitrary code execution.
