import glob
import imghdr
import os
import pathlib
import pprint

path_images = pathlib.Path('/Users/strada/Desktop/images')
files = list(path_images.glob('**/*'))

for file in files:
  if os.path.isfile(file):
    if os.path.basename(file)[:1] != '.':
      imagetype = imghdr.what(file)
      if imagetype == 'png' or 'jpg':
        print(file)
