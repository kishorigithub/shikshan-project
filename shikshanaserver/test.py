# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 16:42:18 2024

@author: yashs
"""

from stegano import lsb
from PIL import Image
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
#Importing necessary modules
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import binascii

# Function to add a hidden text watermark to an image
def add_watermark(image_path, output_path, watermark_text):
    # Open the image
    image = Image.open(image_path)

    # Add watermark
    watermarked_image = lsb.hide(image, watermark_text)

    # Save the watermarked image
    watermarked_image.save(output_path)

# Function to retrieve the hidden text watermark from an image
def retrieve_watermark(image_path):
    # Open the watermarked image
    watermarked_image = Image.open(image_path)

    # Retrieve the watermark
    watermark_text = lsb.reveal(watermarked_image)

    return watermark_text

# RSA encryption and decryption functions
def rsa_encrypt(text, public_key):
    secret_message = bytes(text, 'utf-8')
    
    encMessage = publicKey.encrypt( secret_message ) 
    hexilify= binascii.hexlify(encMessage)
    strencry = str(hexilify.decode('UTF-8'))
    return strencry

def rsa_decrypt(cipher_text, private_key):
    str1 = cipher_text 
    convertedtobyte = bytes(str1, 'utf-8')
    public_crypter =  PKCS1_OAEP.new( key )
    decrypted_data = public_crypter.decrypt(binascii.unhexlify(convertedtobyte))
    print(decrypted_data)
    str1 = decrypted_data.decode('UTF-8') 
    print(str1)       
    return str1

key = RSA.generate(2048)

# Example usage
if __name__ == "__main__":
    # Path to the original image
    original_image_path = "a.png"

    # Path to save the watermarked image
    watermarked_image_path = "watermarked_image.png"

    # Text to be hidden as watermark
    watermark_text = "This is a hiddensdfsdf sdfkkdfds ffksdfkjsdf sdfjksdjfkjsdf"
    publicKey = PKCS1_OAEP.new( key )
    encrypted_watermark = rsa_encrypt(watermark_text, publicKey)

    # Add watermark to the image
    add_watermark(original_image_path, watermarked_image_path, encrypted_watermark)

    # Retrieve the watermark from the watermarked image
    retrieved_watermark = retrieve_watermark(watermarked_image_path)   
         
    public_crypter =  PKCS1_OAEP.new( key )
    decrypted_watermark = rsa_decrypt(retrieved_watermark, public_crypter)
    print("Retrieved Watermark:", decrypted_watermark)
