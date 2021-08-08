import glob
import imghdr
import os
import pathlib
import pprint

# imagetype = imghdr.what('/Users/strada/Desktop/images/image1')
# print(imagetype)

path_images = pathlib.Path('/Users/strada/Desktop/images')
# print(path_images)
files = list(path_images.glob('**/*'))

# pprint.pprint(list(path_images.glob('**/*')))
# files = glob.glob('/Users/strada/Desktop/images/**/*')
for file in files:
  if os.path.isfile(file):
    if os.path.basename(file)[:1] != '.':
      imagetype = imghdr.what(file)
      if imagetype == 'png' or 'jpg':
        print(file)
