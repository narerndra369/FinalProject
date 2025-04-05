from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os

# AES encryption and decryption
def aes_encrypt(image_path, key):
    """
    Encrypts the image using AES encryption algorithm.
    """
    # Open the image file
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    # Generate a random IV (Initialization Vector)
    iv = get_random_bytes(AES.block_size)

    # Create AES cipher object with the given key and iv
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Pad the image data to make it a multiple of block size
    padded_data = pad(image_data, AES.block_size)

    # Encrypt the padded data
    encrypted_data = cipher.encrypt(padded_data)

    # Save the encrypted image with IV prepended to the file
    encrypted_image_path = image_path + '.enc'
    with open(encrypted_image_path, 'wb') as f:
        f.write(iv + encrypted_data)  # Save IV and encrypted data
    
    return encrypted_image_path


def aes_decrypt(encrypted_image_path, key):
    """
    Decrypts the encrypted image using AES decryption algorithm.
    """
    # Read the encrypted image
    with open(encrypted_image_path, 'rb') as f:
        encrypted_data = f.read()

    # Extract the IV from the first 16 bytes of the file
    iv = encrypted_data[:AES.block_size]
    encrypted_image_data = encrypted_data[AES.block_size:]

    # Create AES cipher object with the given key and iv
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the data and unpad it
    decrypted_data = unpad(cipher.decrypt(encrypted_image_data), AES.block_size)

    # Save the decrypted image
    
    
    decrypted_image_path = encrypted_image_path.replace('.enc', '_decrypted.jpg')
    print(decrypted_image_path)
    with open(decrypted_image_path, 'wb') as f:
        f.write(decrypted_data)

    return decrypted_image_path


# # Example usage
# if __name__ == "__main__":
#     key = get_random_bytes(32)  # AES 256-bit key
#     # Encrypt the image
#     encrypted_image = aes_encrypt('i1.png_decrypted.jpg', key)
#     print(f"Encrypted Image Path: {encrypted_image}")
    

#     # Decrypt the image
#     decrypted_image = aes_decrypt(encrypted_image, key)
#     print(f"Decrypted Image Path: {decrypted_image}")
