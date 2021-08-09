import imghdr
import os
import pathlib
import shutil

import PySimpleGUI as sg


# 拡張子のないファイルを移動させる *argsが拡張子
def move_file(current_folder, move_folder, *args):
  show_message = ''
  # ファイル数が多い場合は処理を終了する
  if len(list(pathlib.Path(current_folder).rglob('**/*'))) > 100:
    show_message = '処理するファイル数が多すぎます。フォルダを指定し直してください'
    return show_message

  # 拡張子がついていない、引数で指定した拡張子のものだけ取得する
  for file in pathlib.Path(current_folder).rglob('**/*'):
    if os.path.isfile(file):
      if os.path.splitext(file)[1] == '':
        imagetype = imghdr.what(file)
        for arg in args:
          if imagetype == arg:
            file_path = os.path.join(move_folder, file.stem)
            move_file_path = duplicate_name(file_path)
            shutil.copy(file, move_file_path)
            file_list.append(move_file_path)
  if len(file_list) == 0:
    show_message = '拡張子を追加するファイルがありませんでした'
  return show_message

# 対象フォルダ内の拡張子がないファイルを拡張子付きに変更する
def rename_file(folder):
  show_message = ''
  count = 0
  for file in pathlib.Path(folder).rglob('*'):
    # 移動したファイル以外は処理しない
    if str(file) not in file_list:
      continue
    imagetype = imghdr.what(file)
    if imagetype is not None:
      rename_file = os.path.join(folder, file.stem + '.' + imagetype)
      rename_file = duplicate_name(rename_file)
      file.rename(rename_file)
      count += 1

  if count == len(file_list):
    show_message = f'{count} 件 処理しました'
  else:
    show_message = f'{count} / {len(file_list)} 件 処理しました'
  return show_message

# 重複ファイルをリネームする。引数はフルパス
def duplicate_name(file_path):
  if os.path.exists(file_path):
    name, ext = os.path.splitext(file_path)
    i = 1
    while True:
      new_name = f'{name}{i}{ext}'
      if not os.path.exists(new_name):
        return new_name
      i += 1
  else:
    return file_path

# フォルダが正しく選択されているかチェックする
def check_folder(folder_path1, folder_path2):
    show_message = ''
    if folder_path1 == folder_path2:
      show_message ='2つフォルダは別の場所を指定してください'
    if not os.path.exists(folder_path1):
      show_message =f'{folder_path1}が存在しません'
    if not os.path.exists(folder_path2):
      show_message =f'{folder_path2}が存在しません'
    return show_message

# リストに入っているファイルを削除する
def remove_file(file_path_list):
  if len(file_path_list) == 0:
    return False
  
  for file in file_path_list:
    os.remove(file)
  
  file_path_list.clear()

if __name__ == '__main__':

  layout = [
    [sg.Text('変換したいファイルがあるフォルダを選択してください。サブフォルダも対象です', font=('小塚ゴシック',16))],
    [sg.InputText(key='-current_folder-', enable_events=True, font=('小塚ゴシック',16)),sg.FolderBrowse('選択', target='-current_folder-', font=('小塚ゴシック',16))],
    [sg.Text('')],
    [sg.Text('変換したファイルを保存するフォルダを選択してください', font=('小塚ゴシック',16))],
    [sg.InputText(key='-save_folder-', enable_events=True, font=('小塚ゴシック',16)),sg.FolderBrowse('選択', target='-save_folder-', font=('小塚ゴシック',16))],
    [sg.Button('実行', font=('小塚ゴシック',16)),sg.Button('終了', font=('小塚ゴシック',16))]
  ]
  window = sg.Window('拡張子追加', layout)

  while True:
    file_list = []
    event, values = window.read()
    if event is sg.WIN_CLOSED or event == '終了':
      break
    elif event == '実行':
      target_folder = values['-current_folder-']
      save_folder = values['-save_folder-']

      # 指定フォルダのチェック
      message = check_folder(target_folder, save_folder)
      if message != '':
        sg.popup(message, font=('小塚ゴシック',16))
        continue

      # ファイルを保存先に移動
      message = move_file(target_folder, save_folder, 
                          'png', 'jpg','jpeg', 'gif')
      if message != '':
        sg.popup(message, font=('小塚ゴシック',16))
        continue
      
      if len(file_list) == 0:
        sg.popup('拡張子を追加するファイルがありません', font=('小塚ゴシック',16))
        continue

      # ファイルに拡張子を付ける
      message = rename_file(save_folder)
      sg.popup(message, font=('小塚ゴシック',16))

  window.close()
