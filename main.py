import imghdr
import os
import pathlib
import shutil


# 拡張子のないファイルを移動させる *argsが拡張子
def move_file(current_folder, move_folder, *args):
  num = 1
  for file in pathlib.Path(current_folder).rglob('**/*'):
    if os.path.isfile(file):
      # 拡張子がついていないものだけ取得する
      if os.path.splitext(file)[1] == '':
        imagetype = imghdr.what(file)
        for arg in args:
          if imagetype == arg:
            shutil.copy(file, move_folder + file.stem + '_' + str(num))
            num += 1

# 対象のフォルダ内の拡張子がないファイルを拡張子つきにリネームする
def rename_file(folder):
  for file in pathlib.Path(folder).rglob('*'):
    imagetype = imghdr.what(file)
    if imagetype is not None:
      file.rename(folder + file.stem + '.' + imagetype)

if __name__ == '__main__':
  target_folder = '/Users/strada/Desktop/images'
  save_folder = '/Users/strada/Desktop/rename/'

  move_file(target_folder, save_folder, 'png', 'jpg','jpeg', 'gif')
  rename_file(save_folder)
