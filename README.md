# Stegosaurus
A Python image manipulation app to embed messages within the RGB values of an image using a technique called steganography.

Steganography is a technique in which a message can be hidden within another medium, in this case we are hiding the message within pixels, but these messages can be hidden within videos, other text, audio recordings and many more.

# Compatibilty
This project has only been tested on a linux based machine and is not guaranteed to work on any other OS.

Stegosaurus has been tested and developed to work with PNG files without any issues.

However, during testing I found that trying to encode/decode JPEG images does not work in the way that this application intends. I believe that this is due to the compression that gets applied to the image making the RGB values shift slightly, although I have not looked into this in much detail. It may be something I will try to fix in the future.
