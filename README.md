# Steganography
A Python image manipulation app to embed messages within the RGB values of an image

# Compatibilty
This project has only been tested on a linux based machine and is not guaranteed to work on any other OS.

Moreover, during testing I found that trying to encode/decode JPEG images does not work in the way that this application intends. I believe that this is due to the compression that gets applied to the image making the RGB values shift slightly, although I have not looked into this in much detail. It may be something I will look into in the future.
