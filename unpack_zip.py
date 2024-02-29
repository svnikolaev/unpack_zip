import argparse
from pathlib import Path
import zipfile


def unpack_zip(zip_path, encoding='cp866'):
    zip_path = Path(zip_path)
    unpack_dir = zip_path.parent / zip_path.stem

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        if len(set(path.split('/')[0] for path in file_list)) == 1:
            unpack_dir = zip_path.parent

        for info in zip_ref.infolist():
            try:
                # Попытка перекодирования из 'cp437' в целевую кодировку
                info.filename = info.filename.encode('cp437').decode(encoding)
            except UnicodeEncodeError:
                try:
                    # Если перекодирование не удалось
                    info.filename = info.filename
                except UnicodeDecodeError:
                    print(f"Cannot decode filename: {info.filename}")
                    continue  # Пропускаем файл с недекодируемым именем

            zip_ref.extract(info, unpack_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Unpack a zip archive.')
    parser.add_argument('zip_path', type=str, help='Path to the zip archive')
    parser.add_argument('-e', '--encoding', type=str, default='cp866', 
                        help='Encoding of the file names in the zip archive. Common options are "cp437", "cp866", "cp1251", "utf-8". Default is "cp866".')

    args = parser.parse_args()
    unpack_zip(args.zip_path, args.encoding)
