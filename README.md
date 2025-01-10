# Generic Gallery Downloader
Python script to download images linked by thumbnails on a webpage. Only works on galleries where the thumbnail directly links to the full image.

Due to the generic nature of the downloader, links to each gallery page need to be manually provided.

## Features:

It fakes being a browser.
It will re-download an image if it was corrupted. Some galleries sometimes throw corrupted images for some reason.
It will prepend images with a hash generated from the URL, so you don't need to worry about filename collisions.

Make sure you count all the images to make sure you got them all. Some galleries will throw an advertisement link instead of the image, so you should run the downloader again until you have all the images. It will skip over images already downloaded.

All code was generated by GPT4. I only skimmed through the code myself, but I use it and it seems to work great.

## Dependencies:
```
py -m pip install requests
py -m pip install beautifulsoup4
py -m pip install Pillow
```
