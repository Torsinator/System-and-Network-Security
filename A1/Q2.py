# SENG2050 A1
# Coded by: Tors Webster c3376513
# 02/08/2024

import random
from Crypto.Util import Counter
from Crypto.Cipher import AES
import math
import json
from base64 import b64decode

# Set seed for reproducability
random.seed(0)

def convertStringToBytes(string: str) -> bytes:
    """Converts a string type to bytes

    Args:
        string (str): String to be converted

    Returns:
        bytes: Bytes object corresponding to the utf-8 encoding of the string
    """
    string_bytes = string.encode("utf-8")
    return string_bytes

def generateKey(student_num: str, key_length: int) -> bytes:
    """Generates key

    Args:
        student_num (str): Student number in accordance with spec
        key_length (int): Length of key in bits

    Returns:
        str: A key in bytes consisting of key_length bits
    """
    # Convert student number to bytes
    output_key = bytes.fromhex(student_num)
    remaining_length = key_length - (len(output_key) * 8)
    # Generate a random integer to cover the remaining bits
    remaining_integer = random.randint(0, (2 ** remaining_length) - 1)
    # Convert the random integer to bytes
    remaining_bytes = remaining_integer.to_bytes(math.ceil(remaining_length / 8), "big")
    output_key += remaining_bytes # using + on bytes appends them
    return output_key

def main():
    # Part a:
    # Create a plaintext, each char is 8 bits so a 512 bit string must have 64 chars
    plaintext = "This is a secret message that will showcase AES operation modes."
    assert(len(plaintext) == 64)
    plaintext_bytes = convertStringToBytes(plaintext)
    print("Entire Plaintext: {}".format(plaintext_bytes.hex()))
    print(hex(2 ** 512 - 1))

    # Create a key of 256 bits
    student_num = "c3376513"
    key_length = 256
    key = generateKey(student_num, key_length)
    assert(len(key) * 8 == key_length)
    print("Key: {}".format(key.hex()))
    print("Key: {}".format(hex(int.from_bytes(key, "big"))))

    # Part b Create an IV
    nonce = b"111111111111111"

    # Create a counter object
    # ctr = Counter.new(512, initial_value=int.from_bytes(nonce, byteorder='big'))

    # Create AES cipher in ECB mode
    aes_ecb = AES.new(key, AES.MODE_ECB)

    # Need to split the plaintext into blocks. 128 bits = 16 bytes in each block I believe?
    # for each block:

    # Encrypt the counter value to generate keystream
    keystream = aes_ecb.encrypt(nonce)

    print(len(keystream))

    # XOR keystream with plaintext to get ciphertext
    ciphertext = bytes([_a ^ _b for _a, _b in zip(plaintext_bytes, keystream)])

    # increment the nonce

    print("Ciphertext:", ciphertext.hex())

    # We assume that the key was securely shared beforehand
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    pt = cipher.decrypt(ciphertext)
    print("The message was: ", pt)



if __name__ == "__main__":
    main()
