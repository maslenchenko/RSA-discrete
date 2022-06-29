## RSA cryptosystem implementation in Python3


There are four modules: client.py, server.py, cryptography_funcs.py, and hash_message.py.


The whole RSA algorithm is implemented in the cryptography_funcs.py module, which contains the following functions:

### is_prime(num) <br />
checks whether the number is prime or not

### gcd(a, b) <br />
returns gcd of two numbers

### coprime(a, b) <br />
checks whether two numbers are coprime

### euclidean(e, k) <br />
implementation of the extended Euclidean algorithm

### generate_keys() <br />
generates public and secret keys

### encode(message, e, n) <br />
encodes a message, returns a string which consists of encoded blocks, blocks' length, and amount of fictitious characters

### decode(encoded, d, n, N2, fict_nums) <br />
decodes message


Hash_message.py implements the hash function, which is further going to be used in client.py and server.py.

## How does the program work:

![image](https://user-images.githubusercontent.com/91615687/166122066-3ed8a356-5f7b-47c9-9b22-8e17efd06ca5.png)
*the program was tested with up to seven terminals

The alphabet used in the program includes ASCII symbols from 32 to 122, which means that only English letters can be used.

There are several options for how to send a message:
1) if the user wants to send the message to all users, he should just write down the text
2) if the user wants to send the message to a certain user or users, here is an example - user1 user2 user3|text or just user|text
3) if the user writes down among receivers his own name, he will not receive the message 
4) if the user writes down a non-existent username, he will receive a notification

![image](https://user-images.githubusercontent.com/91615687/166122385-893049ad-a5a9-48c4-b0cb-bf2a001c167d.png)

## Message integrity

Hash_message.py module contains only one function - to_hash(message). It is used before encoding the message and after decoding it. In case the message was incorrectly decoded, a notification will occur.

