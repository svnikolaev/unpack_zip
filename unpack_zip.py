import argparse
from pathlib import Path
import zipfile


def unpack_zip(zip_path: str) -> None:
    """
    Функция для распаковки zip-архива.
    :param zip_path: Путь до zip-архива.
    """
    zip_path = Path(zip_path)
    unpack_dir = zip_path.parent / zip_path.stem

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        # Если все файлы в одной папке внутри архива, то распаковываем в текущую директорию
        if len(set(path.split('/')[0] for path in file_list)) == 1:
            unpack_dir = zip_path.parent

        for info in zip_ref.infolist():
            try:
                # Попытка перекодирования из 'cp437' в "cp866"
                info.filename = info.filename.encode('cp437').decode('cp866')
            except UnicodeEncodeError:
                try:
                    # Если перекодирование не удалось, оставляем исходное имя файла
                    info.filename = info.filename
                except UnicodeDecodeError:
                    print(f"Не удалось декодировать имя файла: {info.filename}")
                    continue  # Пропускаем файл с недекодируемым именем

            zip_ref.extract(info, unpack_dir)  # Распаковываем файл


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Распаковка zip-архива.')
    parser.add_argument('zip_path', type=str, help='Путь до zip-архива')

    args = parser.parse_args()
    unpack_zip(args.zip_path)
