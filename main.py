import sys
import os
import hashlib
from collections import defaultdict

args = sys.argv


def check_dir(argument):
    if len(argument) != 2:
        print('Directory is not specified')
        return


def get_file_type():
    file_type = input('Enter file format type:\n')
    return file_type


def get_extension(file):
    file_name, extension = os.path.splitext(file)
    return extension.lower()


def compare_extensions(extension, file):
    if extension == get_extension(file):
        return True


def get_files(argument):
    file_dict = defaultdict(list)
    file_ext = get_file_type()
    for root, dirs, files in os.walk(argument[1], topdown=True):
        for file in files:
            if not file_ext:
                full_file = os.path.join(root, file)
                file_size = os.path.getsize(full_file)
                file_dict[file_size].append(full_file)
            elif compare_extensions(file_ext, file):
                full_file = os.path.join(root, file)
                file_size = os.path.getsize(full_file)
                file_dict[file_size].append(full_file)
    return file_dict


def get_sort_order():
    input_options = [1, 2]
    sort_order = int((input('Size sorting options:\n'
                            '1. Descending\n'
                            '2. Ascending\n')))
    while sort_order not in input_options:
        print('Wrong option')
        sort_order = int(input('Size sorting options:\n'
                               '1. Descending\n'
                               '2. Ascending\n'))
    if sort_order == 1:
        return True
    elif sort_order == 2:
        return False
    else:
        return True


def print_files(file, sort):
    for key in sorted(file.keys(), reverse=sort):
        print(key, ' bytes')
        for v in file[key]:
            print(v)


def check_duplicates():
    options = ['yes', 'no']
    a = str
    while a not in options:
        a = input('check for duplicates?\n')
    if a == 'yes':
        return True
    else:
        return False


def get_hashed_dict(files, sort):
    size_dict = {}
    for size in sorted(files.keys(), reverse=sort):
        file_hash_dict = {}
        if len(files[size]) > 1:
            size_dict[size] = None
            for file_path in files[size]:
                f = open(file_path, 'r', encoding='unicode_escape')
                file_hash = hashlib.md5(f.read().encode()).hexdigest()
                f.close()
                if file_hash in file_hash_dict.keys():
                    file_hash_dict[file_hash].append(file_path)
                else:
                    file_hash_dict[file_hash] = [file_path]
            # remove non-duplicates from file_hash_dict
            to_del = []
            for hash_index in file_hash_dict.keys():
                if len(file_hash_dict[hash_index]) < 2:
                    to_del.append(hash_index)
            for hash_index in to_del:
                del (file_hash_dict[hash_index])
            size_dict[size] = file_hash_dict
    return size_dict


def get_hashed_output(hashed_dict, sort):
    hashed_output = {}
    count = 1
    for size in sorted(hashed_dict.keys(), reverse=sort):
        print(f'{size} bytes')
        for hash_value in hashed_dict[size].keys():
            print(f'Hash: {hash_value}')
            for file_path in hashed_dict.get(size).get(hash_value):
                if os.path.exists(file_path):
                    hashed_output[count] = file_path
                    print(f'{count}. {hashed_output[count]}')
                    count += 1
    return hashed_output


def ask_to_delete():
    options = ['yes', 'no']
    a = input('Delete files?\n')
    while a not in options:
        print('Wrong option')
        a = input('Delete files?\n')
    return a


def get_num_delete(to_del_opt):
    while True:
        correct_input = True
        a = input('Enter file number to delete:\n')
        to_del = a.split(' ')
        for i in to_del:
            if i.isdigit() and int(i) in to_del_opt.keys():
                continue
            else:
                print('Wrong format')
                correct_input = False
                break
        if correct_input:
            return to_del


def delete_files(del_opt, lst):
    freed_space = 0
    for i in lst:
        file_del = del_opt[int(i)]
        freed_space = freed_space + os.path.getsize(file_del)
        os.remove(file_del)
        # print(file_del)
        # print(os.path.getsize(file_del))
    print(f'Total freed up space: {freed_space} bytes')
    return


def main():
    check_dir(args)
    files = get_files(args)
    sort = (get_sort_order())
    print_files(files, sort)
    if check_duplicates():
        hashed_files = get_hashed_dict(files, sort)
        del_options = get_hashed_output(hashed_files, sort)
        if ask_to_delete():
            files_to_del = get_num_delete(del_options)
            delete_files(del_options, files_to_del)


main()
