---
layout: post
title: Tokyo Westerns CTF 3rd 2017 - My Simple Cipher
permalink: /writeups/tokyowesternctf2017/mysimplecipher
description: "Writeup for Status Box challenge from PoliCTF 2017"
date: 2017-09-05
tags: [tokyowesternctf2017, crypto, writeup]
comments: true
share: true
---

> ### Problem 
>
> This my first cipher system. Can you break it?
>
> [my-simple-cipher.7z](https://github.com/dowsll/dowsll.github.io/raw/master/_posts/writeups/tokyowesternsctf2017/mysimplecipher/my-simple-cipher.7z-bb72c6605237320dfaf8eb3459e8806d27ceb73f118224ec3acbf5f77aa836d1)

## Challenge
Looking at the given [cipher.py](https://github.com/dowsll/dowsll.github.io/blob/master/_posts/writeups/tokyowesternsctf2017/mysimplecipher/cipher.py) file, we can see that this is something like a shift cipher with a key of length 13, used with something like CBC (Cipher Block Chaining). We need to decrypt the given message of length 36.

## Encryption
```
message = flag + "|" + key

encrypted = chr(random.randint(0, 128))

for i in range(0, len(message)):
  encrypted += chr((ord(message[i]) + ord(key[i % len(key)]) + ord(encrypted[i])) % 128)
```

The message is in the form of `flag|message`. Then, there are two parts to the encryption operation performed.

### Shifting
Firstly, they have a key of length 13. Each character in the message is added by the corresponding character in the key followed by modulo 128. Since the key is shorter than the message, when we reach the end of the key we go back to the start of the key.

Say we have a message of length 8 and key of length 3.

![encrypt.png](https://raw.githubusercontent.com/dowsll/dowsll.github.io/master/_posts/writeups/tokyowesternsctf2017/mysimplecipher/encrypt.png)

### Chaining
Other than xoring with the key, each character is also added by the character before it followed by modulo 128. This starts by having a random character at the start of the encrypted message.

So, in the end we have `encrypted += chr((ord(message[i]) + ord(key[i % len(key)]) + ord(encrypted[i])) % 128)`.

## Decryption
### Chaining
First, I removed the chaining encryption by subtracting each character by its previous character followed by modulo 128 in the encrypted message, starting from the last character.

```
# s is the encrypted message
dec1 = [ord(c) for c in s]  
for i in range(len(s) - 1, 1, -1):
  dec1[i] = (dec1[i] - dec1[i-1]) % 128
```

### Shifting
Now we got that cleared, we need to find the 13 byte key to get back our original message. Since the message is in the form of `flag|key`, we can make use of the fact that there is a `|` character at the 23th position (36 - 13 = 23).

With this knowledge, we can know get the 10th character of the key, since it was used to encrypt the 23th character from `|` to whatever it is in the encrypted form.

After doing so, we now know the 10th character of the key, and since it is also encrypted in the message, we can do the same thing as above. We repeat until we recover the entire key.

```
key = [0] * 13
c = len(dec1) - 13 - 1  # our current character, we start from the position of the '|' character
key[c % 13] = (dec1[c] - ord('|')) % 128  # recover the key

for _ in range(12):
  c = (c % 13) + len(dec1) - 13   # find the position of the previously recovered character in the encrypted message
  key[c % 13] = (dec1[c] - key[(c - (len(dec1) - 13))]) % 128   # recover the key
```

Finally, we recover our message.

```
message = ''
for i in range(0, len(dec1)):
  message += chr((dec1[i] - key[i % len(key)]) % 128)

print message
```

We get `TWCTF{Crypto-is-fun!}|ENJ0YHOLIDAY!`

Full script [here](https://github.com/dowsll/dowsll.github.io/blob/master/_posts/writeups/tokyowesternsctf2017/mysimplecipher/decipher.py)

## Remarks
Actually weirdly i got `PWCTF{Crypto-is-fun!}|ENJ0YHOLIDAY!` as the decrypted message, maybe there was a mistake somewhere in my code\.\.\.