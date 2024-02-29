import argparse
from pathlib import Path
import zipfile


def unpack_zip(zip_path, encoding='cp866'):
    # Определение имени архива и директории для распаковки
    zip_path = Path(zip_path)
    unpack_dir = zip_path.parent / zip_path.stem

    # Распаковка архива
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Получаем список файлов в архиве
        file_list = zip_ref.namelist()

        # Если все файлы находятся в одной папке в корне архива
        if len(set(path.split('/')[0] for path in file_list)) == 1:
            unpack_dir = zip_path.parent

        for info in zip_ref.infolist():
            info.filename = info.filename.encode('cp437').decode(encoding)
            zip_ref.extract(info, unpack_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Unpack a zip archive.')
    parser.add_argument('zip_path', type=str, help='Path to the zip archive')
    parser.add_argument('-e', '--encoding', type=str, default='cp866', 
                        help='Encoding of the file names in the zip archive. Common options are "cp437", "cp866", "cp1251", "utf-8". Default is "cp866".')

    args = parser.parse_args()
    unpack_zip(args.zip_path, args.encoding)
