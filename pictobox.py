#!/usr/bin/env python3

import argparse
import os
import sys
import json
import shutil

from exif import Image

def get_args():
    parser = argparse.ArgumentParser(description='Sort images by device make/model')
    parser.add_argument('--dir', '-d', help='path to target directory with images')
    parser.add_argument('--arrange', '-a', action='store_true', help='create a new directory with sorted images')
    parser.add_argument('--sorted', '-s', help='specify a custom name for the directory with sorted images (default = "sorted-images")')
    parser.add_argument('--output', '-o', help='specify the name of an output file to which to write JSON output')
    
    return parser.parse_args()

def is_valid_extension(ext):
    if ext == '.jpg' or ext == '.jpeg':
        return True
    
    return False

def path_format(main_dir, sub):
    return '{}/{}'.format(main_dir, sub).replace('//', '/')

def get_sorted_image_names(target_dir):
    makes_models = {}
    
    for item in os.listdir(target_dir):
        ext = os.path.splitext(item)[-1].lower()

        if is_valid_extension(ext):
            with open(path_format(target_dir, item), 'rb') as image_file:
                current_image = Image(image_file)
            
            if 'make' in dir(current_image):
                make_model = '{}-{}'.format(current_image.make, current_image.model).replace(' ', '-')
                
                if make_model in makes_models:
                    makes_models[make_model].append(item)
                else:
                    makes_models[make_model] = [item]
            elif 'Unknown' in makes_models:
                makes_models['Unknown'].append(item)
            else:
                makes_models['Unknown'] = [item]
    
    return makes_models

def get_formatted_json(dict):
    return json.dumps(dict, indent=4)

def prompt_yes_no():
    answer = str(input('This program will copy files and create directories. Are you sure you want to continue? (y/n): '))
    
    if answer[0].lower() == 'y':
        return True

    return False

def create_sorted_dirs(target_dir, sorted_image_names, sorted_dir_name):
    sorted_dir = path_format(target_dir, sorted_dir_name)
    if os.path.exists(sorted_dir):
        shutil.rmtree(sorted_dir)
    os.mkdir(sorted_dir)

    for make_model in sorted_image_names:
        os.mkdir(path_format(sorted_dir, make_model))

        image = sorted_image_names[make_model]
        dest_dir = path_format(sorted_dir, make_model)

        src_file = path_format(target_dir, image[0])
        dest_file = path_format(dest_dir, image[0])
        shutil.copyfile(src_file, dest_file)
    
    print('\nDirectory "{}" with sorted images was created'.format(sorted_dir))

def main():
    target_dir = ''
    output_file = ''
    sorted_dir_name = 'sorted-images'
    arrange_images = False

    args = get_args()

    if args.arrange:
        yes_no = prompt_yes_no()
        
        if not yes_no:
            sys.exit(1)

    if args.dir is not None:
        if os.path.exists(args.dir) and os.path.isdir(args.dir):
            target_dir = args.dir
        elif os.path.isfile(args.dir):
            print('Path is not a directory')
            sys.exit(1)
        else:
            print('Not a valid path')
            sys.exit(1)
    else:
        target_dir = os.getcwd()

    if args.sorted is not None:
        sorted_dir_name = args.sorted

    if args.output is not None:
        output_file = args.output

    sorted_image_names = get_sorted_image_names(target_dir)
   
    formatted_json = get_formatted_json(sorted_image_names)

    if output_file != '':
        output_file_path = path_format(target_dir, output_file)

        with open(output_file_path, 'w') as write_file:
            write_file.write(formatted_json)
        
        write_file.close()

        print('\nOutput was written to file "{}"'.format(output_file_path))
    else:
        if len(sorted_image_names) > 0:
            print('\n' + formatted_json)

    if args.arrange:
        create_sorted_dirs(target_dir, sorted_image_names, sorted_dir_name)

if __name__ == '__main__':
    main()
