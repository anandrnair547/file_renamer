import glob
import os
import re
from pathlib import Path

regex = r'^(?!\d.\d(GB|MB|KB|TB))(?P<url>(?:(?:https?|ftp):\/\/)?[\w\/\-?=%.]+\.[\w\/\-?=%.]{2,4})'

class FileManager:

    @staticmethod
    def list_files(folder_path, file_pattern):
        file_pattern = file_pattern
        files_list = FileManager.file_browser(folder_path, file_pattern)
        return files_list

    @staticmethod
    def file_browser(folder_path, file_pattern):
        """Returns a list with all files with the word/extension in it"""
        file = []
        r_file_pattern = "r'" + file_pattern + "'"
        print("file pattern", r_file_pattern)
        (_, _, filenames) = next(os.walk(folder_path))
        for f in filenames:
            # print("file:", f)
            # if file_pattern in f:
            if re.search(file_pattern, f, re.IGNORECASE):
                print("match file:", f)
                file.append(f)
        return file

    @staticmethod
    def rename_files_by_replacing_string(folder_path, files_list, replace_string="", with_string=""):
        for filename in files_list:
            new_file_name = filename.replace(replace_string, with_string)
            src = os.path.join(folder_path, filename)
            dst = os.path.join(folder_path, new_file_name)
            FileManager.rename_file(src, dst)

    @staticmethod
    def rename_file(source_name, destination_name):
        os.rename(source_name, destination_name)

    @staticmethod
    def find_urls_in_list(search_list):
        urls = set()
        for string in search_list:
            url = FileManager.find_url_in_string(string)
            print(url)
            if url is not None:
                urls.add(url)
        return urls

    @staticmethod
    def find_url_in_string(string):
        m = re.search(regex, string, re.IGNORECASE)
        url = m.group(0)
        return url
