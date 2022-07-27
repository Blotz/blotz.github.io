---
title: "Random Does Not Equal Random"
date: 2022-07-21T18:42:22+01:00
tags:
    - Software
category:
    - blog
keywords:
    - pseudo random
    - computer
    - random number generators
comments: true
draft: false
---
Random numbers are a core part of cryptography.

They are used in encryption due to the fact that it is much harder to guess a randomly generated password than it is to guess any other kind of password.
This core concept has resulted in random number generation/generators becoming an integral part of cryptography.

This would be fine if it weren't for the fact that computers suck at being random.
Computers work with exactness and precision. They were designed to.
You don't want a computer at a bank to guess how much money you own.
This is where the concept of suedo random numbers came from.

## Pseudorandom number generators PRNG

[Pseudorandom number generators](https://en.wikipedia.org/wiki/Pseudorandom_number_generator) are complicated mathematical algorithms for generating a sequence of numbers which approximate the properties of true random number generators.
These PRNGs are designed to be quick in number generation and reproducible. This means, if the initial state (the seed) is identical, then
the number generated will be identical. 
In addition, most PRNG are not reversible. This means you cant calculate the starting state from the output of the generator.

This, of course, means that a pseudorandom number generator is far from similar to a true random number generator.
Of course, it does mean we can have a little fun with PRNGs.

## Hardware Random Number Generators

Some devices use a piece of hardware to [generate random numbers](https://en.wikipedia.org/wiki/Hardware_random_number_generator).
This can happen though a range of sources such as, radio noise, thermal noise, and other quantum effects.
They are considered to be true random number generators due to the fact that it is impossible to predict the noise on these systems.

Hardware Generators can only produce a limited number of random bits per second. They need to allow for enough time to pass such that the state of the system has changed enough. HRNG are usually used to seed PRNG which can generate numbers at a much faster rate.

### Lava Lamp wall

Companies such as Cloudflare need a large volume of random numbers for secure encryption.
In response to this issue, Cloudflare built a [wall of lava lamps](https://www.cloudflare.com/learning/ssl/lava-lamp-encryption/) which they take photos of and convert into a stream of random bits.

This works off the concept of "a lava lamp will never take the same shape twice".

## Fun with Pseudo Random Number Generators

### The meaning of life

In programming languages, you can set a "seed" for a random number generator.
The seed is the initial starting state of the random number generator.

This means you can influence the numbers of a random number generator.
For example:

```python
#!/usr/bin/env python3
import random

random.seed(36)  # Setting out initial state

the_meaning_of_life = random.randint(0,100)  # This will always generate the same value
print("The meaning of life is", the_meaning_of_life)
```

Feel free to run this program on your own computer to work out the meaning of life! :smile:

#### How to calculate the seed

This simple program is quite easy to run. However, calculating the seed value was much harder.
Because the python random number generator isn't reversible, we need to brute force the state.
While this is simple to program, it takes exponentially longer to crack (based on the complexity of your output).

For the above example, you can crack it using this small program:

```python
#!/usr/bin/env python3
import random
from itertools import count

for n in count():  # This count up from 0 in steps of 1. eg n will be 0, 1, 2, 3, 4 ...

    random.seed(n)  # Set the seed to out "guess"

    # Check if out guess is correct
    if random.randint(0, 100) == 42:
        # If it is, we print the guess and stop the code
        print("The seed is", n)
        break  # This line stops the loop from continuing
```

This program guesses the seed and then checks its own guess.
This is a very slow process as the seed for 42 can be anywhere possible value.

### Cracking digits of pi

The more specific the number you are looking for, the longer your program will take for calculating the seed.
The following program tries to find the seed which results in the digits of pi.

```python
#!/usr/bin/env python3
import random
from itertools import count

length: int = -1  # The longest stretch of pi we have discovered
pi = [3,1,4,1,5,9,2,6,5,3,5,8,9,7,9]  # pi up to 15 digits

for n in count():
    random.seed(n)
    
    # Loop though our values of pi
    for index, digit in enumerate(pi):
        num = random.randint(0, 9)

        # If the number generated isn't a digit of pi, we exit this loop
        if num != digit:
            break
        
        # If the number generated is longer than our longest sequence, we print the value and save its length
        if index > length:
            length = index
            print(f"Seed: {n} Length: {length + 1}")
    else:
        # This only runs once we have looped though all values of pi
        # It exits the outer loop and lets the program finish
        break
```

This simple program could take years to finish. I ran this program for 45 mins and only found a sequence of length 8 (74759033). Please leave in the comments if you find a longer sequence, I'm interested to see!

The program takes exponentially longer to calculating sequences of pi.
It clearly shows the exponential time increase for brute forcing longer and longer sequences of pi.

It also shows how you can find sequences of numbers in pseudo random number generators

### Sending "Secret" messages

One final fun program you can do with random numbers is you can send secret messages using it!
You can convert characters in a message into a series of seeds which you can send to your friends.

These messages would appear as random numbers to all who dont know how to read them!
Decrypting the message would be as simple as setting the seed and generating the numbers. Then converting to a character.

Here is a small program for generating these secret messages

```python
#!/usr/bin/env python3
import random
from itertools import count

secret_message = input("Enter a secret message: ")

message_list = list(secret_message)  # Convert message into a list of characters

for character in message_list:  # Looping though each character in the message

    character_number = ord(character)  # We convert the ascii character into its number

    for n in count():  # We start to brute force the seed for each character
        random.seed(n)

        if random.randint(0, 127) == character_number:  # 0, 127 is the range of ascii characters
            print(n, end=" ")  # Print the seed of the character
            break  # We break out of the loop once we find the seed
```

The program calculates the seed for each character and prints it.

Try and create a program for decrypting these programmes!
Here is a secret message for you to decrypt!

`84 41 9 88 95 12 205 40 95 88 9 88 144 95 132 136 387 205 144 81 88 152 95 1 81 44 132 11 1 95 132 261 95 387 12 81 44 205 261 107 95 132 81 11 95 41 95 227 40 261 95 88 41 11 81 88 144 95 88 99 99 108`

I wish you lots of luck cracking my secret message!

Also, please leave feedback in the comments!
I'm always looking to improve my writing!
