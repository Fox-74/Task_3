import click
import eyed3
import os
import shutil
#--------------------------------------
#Чтение параметров из командной строки
#--------------------------------------
@click.command()
@click.option('-s', '--src-dir', default='.', help='Исходная директория.', show_default=True)
@click.option('-d', '--dst-dir', default='.', help='Целевая дириктория.', show_default=True)
#----------------------------------------------------------------------------------------------
#Функция сортировки
def sorter(src_dir, dst_dir):
    """Программа - сортировщик музыкальных файлов"""
    while True:
        if os.path.isdir(src_dir): # Проверка ресурса
            try:
                it = os.scandir(src_dir)
            except PermissionError as e:
                print(str(e))
                print('Введите другую директорию или "q" для выхода.')
                src_dir = input('-> ')
                if src_dir == 'q':
                    break
            else:
                with it: #Проверка файлов в дириктории
                    for entry in it:
                        if not entry.name.startswith('.') and entry.is_file() \
                                and entry.name.lower().endswith('.mp3'):
                            try:
                                audiofile = eyed3.load(entry)
                                if not audiofile.tag.title:
                                    title = entry.name
                                else:
                                    title = audiofile.tag.title.replace('/', ':')
                                if not audiofile.tag.artist or not audiofile.tag.album:
                                    print(f'Файл не имеет достаточно ID3 тегов: {entry.name}')
                                    continue
                                else:
                                    artist = audiofile.tag.artist.replace('/', ':')
                                    album = audiofile.tag.album.replace('/', ':')
                                audiofile.tag.save()
                            except AttributeError as e:
                                print(f'Ошибка файла: {entry.name}')
                            except PermissionError as e:
                                print(f'Недостаточно прав для записи: {entry.name}')
                                continue
                            else:
                                new_file_name = f'{title} - {artist} - {album}.mp3'
                                if os.path.exists(os.path.join(dst_dir, artist, album)):
                                    shutil.move(os.path.join(src_dir, entry.name),
                                                os.path.join(dst_dir, artist, album, new_file_name))
                                else:
                                    try:
                                        os.makedirs(os.path.join(dst_dir, artist, album))
                                    except PermissionError as e:
                                        print(str(e))
                                        print('Введите путь к другой директории назначения или "q" для выхода.')
                                        dst_dir = input('-> ')
                                        if dst_dir == 'q':
                                            break
                                    else:
                                        shutil.move(os.path.join(src_dir, entry.name),
                                                    os.path.join(dst_dir, artist, album, new_file_name))
                                print(f'{os.path.join(src_dir, entry.name)} '
                                      f'-> {os.path.join(dst_dir, artist, album, new_file_name)}')
                print('Done.')
                break
        else:
            print('Целевая директория не найдена.')
            print('Введите путь к другой директории назначения или "q" для выхода.')
            src_dir = input('-> ')
            if src_dir == 'q':
                break
if __name__ == '__main__':
    sorter()