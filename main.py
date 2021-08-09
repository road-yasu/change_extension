import imghdr
import os
import pathlib
import shutil

import PySimpleGUI as sg

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
            destination_file_path = os.path.join(move_folder, file.stem + '_' + str(num))
            shutil.copy(file, destination_file_path)
            num += 1
  if num < 2:
    return False

# 対象フォルダ内の拡張子がないファイルを拡張子付きに変更する
def rename_file(folder):
  for file in pathlib.Path(folder).rglob('*'):
    imagetype = imghdr.what(file)
    if imagetype is not None:
      rename_file = os.path.join(folder, file.stem + '.' + imagetype)
      file.rename(rename_file)

if __name__ == '__main__':

  layout = [
    [sg.Text('対象フォルダ'), sg.InputText(key='-current_folder-', enable_events=True),sg.FolderBrowse('選択', target='-current_folder-')],
    [sg.Text('保存フォルダ'), sg.InputText(key='-save_folder-', enable_events=True),sg.FolderBrowse('選択', target='-save_folder-')],
    [sg.Button('実行'),sg.Button('終了')]
  ]
  window = sg.Window('拡張子追加', layout)

  while True:
    event, values = window.read()
    if event is sg.WIN_CLOSED or event == '終了':
      break
    elif event == '実行':
      target_folder = values['-current_folder-']
      save_folder = values['-save_folder-']

      if move_file(target_folder, save_folder, 'png', 'jpg','jpeg', 'gif') == False:
        show_message ='拡張子を追加するファイルがありませんでした'
        sg.popup(show_message)

      rename_file(save_folder)
  window.close()
