#!/usr/bin/env python3
import argparse
from pathlib import Path
import zipfile


def unpack_zip(zip_path: str) -> Path:
    """Функция для распаковки zip-архива.

    :param zip_path: Путь до zip-архива.
    :return: Путь до директории, в которую были распакованы файлы.
    """
    zip_path = Path(zip_path)
    # По умолчанию распаковываем в подпапку с именем архива
    unpack_dir = zip_path.parent / zip_path.stem
    # Инициализируем переменную для хранения итоговой директории
    resulted_dir = unpack_dir

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        # Если все файлы в одной папке внутри архива, то распаковываем в
        # текущую директорию
        if len(set(path.split('/')[0] for path in file_list)) == 1:
            unpack_dir = zip_path.parent
            # Берем первую часть пути первого файла в списке, это будет
            # название папки
            folder_name = file_list[0].split('/')[0]
            # Пытаемся декодировать имя папки
            try:
                folder_name = folder_name.encode('cp437').decode('cp866')
            except UnicodeEncodeError:
                pass  # Если декодирование не удалось, оставляем исходное имя
            # Обновляем итоговую директорию
            resulted_dir = unpack_dir / folder_name

        # Проходим по всем файлам и папкам внутри архива
        for info in zip_ref.infolist():
            try:
                # Попытка перекодирования из 'cp437' в "cp866"
                info.filename = info.filename.encode('cp437').decode('cp866')
            except UnicodeEncodeError:
                try:
                    # Если перекодирование не удалось, оставляем исходное имя
                    info.filename = info.filename
                except UnicodeDecodeError:
                    print(
                        f"Не удалось декодировать имя файла: {info.filename}"
                    )
                    continue  # Пропускаем файл с недекодируемым именем

            zip_ref.extract(info, unpack_dir)  # Распаковываем файл

    return resulted_dir


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Распаковка zip-архива.')
    parser.add_argument('zip_path', type=str, help='Путь до zip-архива')

    args = parser.parse_args()
    unpack_dir = unpack_zip(args.zip_path)
    unpack_dir = Path(unpack_dir).resolve()
    print(f"Файлы были извлечены в директорию: {unpack_dir}")
