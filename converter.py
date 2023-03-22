import sys
import os
import tarfile
from iconv import Iconv

def euckr_to_utf8(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
        converter = Iconv('euckr', 'utf-8')
        return converter.convert(content)

def convert_and_extract_tar(tar_path, output_directory):
    with tarfile.open(tar_path, 'r') as tar:
        for member in tar.getmembers():
            euckr_filename = member.name
            utf8_filename = euckr_to_utf8(euckr_filename)

            member.name = utf8_filename
            tar.extract(member, path=output_directory)

            if member.isfile():
                file_path = os.path.join(output_directory, utf8_filename)
                utf8_content = euckr_to_utf8(file_path)
                with open(file_path, 'wb') as file:
                    file.write(utf8_content)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python converter.py input.tar output_directory")
        sys.exit(1)

    tar_path = sys.argv[1]
    output_directory = sys.argv[2]

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    convert_and_extract_tar(tar_path, output_directory)
