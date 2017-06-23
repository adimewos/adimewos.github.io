---
layout: post
title: Learn Reverse Engineering
description: "Introduction to Reverse Engineering on x86 Linux"
date: 2017-06-17
tags: [x86, re]
comments: true
share: true
---

This is the first of the series of posts I'll be making on x86 binary exploitation. To start off binary exploitation, I recommend learning reverse engineering on the Linux x86 platform.

This post is intended for beginners that have no experience whatsoever in x86 reverse engineering.

## Learn x86 Assembly
Knowledge of x86 Assembly is definitely necessary if you want to do x86 binary exploitation.

I recommend finishing this [playlist](https://www.youtube.com/playlist?list=PL038BE01D3BAEFDB0) to learn the basics about 32-bit x86 assembly. The course will cover on the basics about the x86 Assembly language, the stack, and discuss the CMUBomb crackme challenge.

Maybe before starting we can have a look at [this](http://security.cs.rpi.edu/courses/binexp-spring2015/lectures/2/02_lecture.pdf) slides prepared by RPISEC for the MBE course. However, it is prepared to be used in their lectures so without demonstration some slides may be less intuitive.

## Tools
In the playlist above, the instructor, Xeno demonstrated how to do reverse engineering with GDB. However, plain GDB is really hard to look at. There are some other better tools designed for doing binary analysis.

Binary analysis can be split into 2 different types. Static analysis refers to looking at the disassembly to find out what the program is doing. Dynamic analysis refers to looking at the program's memory, such as the stack, heap or registers while running to have a clearer view of what is going on.

Neither is considered better, as you most of the time need to do static analysis first to have an overview of what the program is supposed to do, only after that you can try to have a clearer understanding of what the program is doing.

### Static Analysis
* GDB: Well you can technically do `disas _insert_function_here_` and that's totally fine. But it's totally unnecessary to make your life so difficult.

* objdump: Linux has a built in command `objdump` that allows you to view the disassembly of a binary by doing `objdump -d`. Again, why torture yourself?

* [IDA](https://www.hex-rays.com/products/ida/support/download_demo.shtml): Arguably the best disassembler out there, except that it's expensive and not everyone can afford the full version. The trial version only supports limited architectures some of which includes 32-bit x86 Linux ELF Binaries and 32-bit x86 Windows PE Executables.

* [Hopper](https://www.hopperapp.com/): Another (not free) disassembler. I have not tried this before so I can't give comments.

* [Binary Ninja](https://binary.ninja/): Quite new in the scene but received very good reviews. Also not free. However, I recommend to give it a try as it has a built in hex editor and allows you to write extensions in python.

* [Radare2](https://github.com/radare/radare2): Free and Open Source! It supports almost every architecture. Highly recommend to learn and use it. However as there is no GUI it may not be very intuitive at the start. [Here](http://sushant94.me/2015/05/31/Introduction_to_radare2/) is a pretty nice guide to start with radare2. [LiveOverflow](https://youtu.be/3NTXFUxcKPc?t=8m34s) also has a really good introduction to radare2.
	
### Dynamic Analysis
* [GDB PEDA](https://github.com/longld/peda): PEDA is an extension for GDB which gives you a better view of the registers and memory state while debugging.

* [Radare2](https://github.com/radare/radare2): Besides static analysis, radare2 is also capable of doing dynamic analysis like GDB. However I prefer using GDB for this.

* [qira](http://qira.me/): A debugger that allows you to run your program first then do the analysis afterwards, to save the hassle of keep needing to rerun the program if using GDB. Control flow graphs are also present in the debugger. Definitely should give it a try.
	
### There are so many choices, so which one should I use?
For me, I currently use radare2 for static analysis and GDB with PEDA for dynamic analysis. Will probably try out qira some time soon.

## Challenges
After finishing the playlist, it's time to test our skills on the following crackmes (sorted in the order I recommend).
* Intro [crackmes](http://security.cs.rpi.edu/courses/binexp-spring2015/lectures/2/challenges.zip) by RPISEC
* Bomb [crackmes](http://security.cs.rpi.edu/courses/binexp-spring2015/lectures/3/bombs.zip) by RPI and CMU

### MBE
After finishing the crackmes above, you should be able to understand x86 assembly pretty well already. So let's set up the [MBE](https://github.com/RPISEC/MBE) VM which we will be using for the rest of this series.

The README contains pretty well documentation for setting up the VM so it won't be covered here. Once you are done setting up, try to solve the crackmes in the Lab01 folder.

## Final words
These should be sufficient practice to get yourself into x86 reverse engineering. Make sure that you fully understand x86 assembly so that the future parts are easier to grasp.



