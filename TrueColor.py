'''
Image Embedding
August 2020
'''

''' 3rd Party Library '''

'''
Image Orientation

         |
         |
y (rows) |
         |
         |     
         -----------------------------
                     x (columns)
'''
''' Image Embedding
March 2023
'''

''' Import necessary libraries '''
from PIL import Image

''' Define constants '''
RED   = 0
GREEN = 1
BLUE  = 2

''' Open image file and get basic information '''
img = Image.open('monalisa.bmp')
x, y = img.size
pix = img.load()

''' Read in code book '''
codebook = {}
with open('CodeBook.txt', 'r') as f:
    for line in f:
        key, val = line.strip().split(maxsplit=1) # Split at most once to get key and value
        codebook[key] = val

''' Message to hide '''
message = 'Hello, World!'

''' Convert message to binary '''
bin_message = ''.join(format(ord(char), '08b') for char in message)

''' Check if message will fit in the image '''
if len(bin_message) > (3 * x * y):
    print("Message too long to embed.")
else:
    ''' Embed message in the image '''
    bin_message += '0' * (3 * x * y - len(bin_message))   # Pad message with zeros
    message_idx = 0
    for row in range(y):
        for col in range(x):
            pixel = list(pix[col, row])   # Pixel values
            if message_idx < len(bin_message):
                # Modify the least significant bit of each color channel
                pixel[RED] = (pixel[RED] & 0xFE) | int(bin_message[message_idx])
                message_idx += 1
            if message_idx < len(bin_message):
                pixel[GREEN] = (pixel[GREEN] & 0xFE) | int(bin_message[message_idx])
                message_idx += 1
            if message_idx < len(bin_message):
                pixel[BLUE] = (pixel[BLUE] & 0xFE) | int(bin_message[message_idx])
                message_idx += 1
            pix[col, row] = tuple(pixel)   # Update pixel values in image

    ''' Save the modified image '''
    img.save('embedded.bmp')
    print("Message embedded successfully.")

    ''' Print code book for reference '''
    print("Code book:")
    for key, val in codebook.items():
        print(key, "-", val)

    
