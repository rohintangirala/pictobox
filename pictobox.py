import argparse
import os
import sys
import json
import shutil

from exif import Image

def is_valid_extension(ext):
    if ext == '.jpg' or ext == '.jpeg':
        return True
    return False

def path_format(main_dir, sub):
    return '{}/{}'.format(main_dir, sub)

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

def create_sorted_dirs(target_dir, sorted_image_names):
    sorted_dir = path_format(target_dir, 'sorted-images')
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

def main():
    parser = argparse.ArgumentParser(description='Sort images by device make/model')
    parser.add_argument('--dir', '-d')
    parser.add_argument('--arrange', '-a', action='store_true')
    args = parser.parse_args()

    target_dir = ''

    arrange_images = False

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

    sorted_image_names = get_sorted_image_names(target_dir)
   
    print(get_formatted_json(sorted_image_names))

    if args.arrange:
        create_sorted_dirs(target_dir, sorted_image_names)


if __name__ == '__main__':
    main()
