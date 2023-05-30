from PIL import Image
import random
from scipy.stats import entropy
import matplotlib.pyplot as plt
from collections import Counter
import math

def TRNG(numOfBits):

    plik = 'image01.jpg'
    image = Image.open(plik)
    allpix=list(image.getdata())
    sekwencje=''
    Sekwencjebitowe=[]

    def create_bit_sequence(rgb_channels):
        Sekwencjebitowe = []
        for r, g, b in rgb_channels:
            for val in (r, g, b):
                if val >= 2 and val <= 253:
                    # Extract the last bit of the channel value and append it to the bit sequence
                    Sekwencjebitowe.append(val & 1)
        return Sekwencjebitowe

    Sekwencjebitowe = create_bit_sequence(allpix)
    Sekwencjebitowe=Sekwencjebitowe[:numOfBits]
    random.shuffle(Sekwencjebitowe) #makes better the entropy
    # Join the bit sequence into a string
    bit_string = ''.join(str(bit) for bit in Sekwencjebitowe)

    # Pad the bit string with zeros to ensure it has a length divisible by bits_per_value
    padded_bit_string = bit_string.ljust((len(bit_string) + numOfBits - 1) // numOfBits * numOfBits, '0')

    # Convert the padded bit string to decimal number
    decimal_value = int(padded_bit_string, 2)

    return decimal_value


#a function to check if a number is prime
def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

#a function to generate a random prime number
def generate_prime(bits):
    while True:
        num = TRNG(bits)
        if is_prime(num):
            return num


#step 1:  Generate two random prime numbers p and q with a specified number of bits
bits = 15  # Specify the desired number of bits for p and q
p = generate_prime(bits)
q = generate_prime(bits)

#Step 2: Compute n and phi values
n = p * q
phi = (p - 1) * (q - 1)

#Step 3: Find a random e value that is coprime with phi
while True:
    e = random.randrange(2, phi)
    if math.gcd(e, phi) == 1:
        break

#Step 4: Calculate the modular multiplicative inverse of e modulo phi (find d)
d = pow(e, -1, phi)

def encrypt(message, e, n):
    return pow(message, e, n)

def decrypt(ciphertext, d, n):
    return pow(ciphertext, d, n)

message = 42  # The message to be encrypted

ciphertext = encrypt(message, e, n)
plaintext = decrypt(ciphertext, d, n)

print("Original message:", message)
print("Ciphertext:", ciphertext)
print("Decrypted message:", plaintext)