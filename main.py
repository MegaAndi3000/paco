import os
import sys
import time
import json
import shutil


ERROR_STRING = "\033[1m[\033[31mERROR\033[37m]\033[0m"
DONE_STRING = "\033[1m[\033[32mDONE\033[37m]\033[0m"
INFO_STRING = "\033[1m[\033[36mINFO\033[37m]\033[0m"


def set_string_length(string:str, length:int):
    """Extends or shortens a given string to a given length.

    Args:
        string (str): string, which is to be edited
        length (int): the resulting length

    Returns:
        str: edited string with given length
    """
    
    if len(string) > length:
        new_string = string[:length]
    else:
        new_string = string + " " * (length - len(string))    
    
    return new_string


def copy_item(source_path: str, destination_path: str, ignore_list: list):
    """Copies a file or directory to a given directory.

    Args:
        source_path (str): path to the source directory/file
        destination_path (str): path to the destination directory
        ignore_list (str[]): list of patterns, which are to be ignored when copying
    """

    ignore_patterns = shutil.ignore_patterns(*ignore_list)
    if os.path.isdir(source_path):
        destination_path = os.path.join(destination_path, os.path.basename(source_path))
        shutil.copytree(source_path, destination_path, ignore=ignore_patterns)
    elif os.path.isfile(source_path):
        shutil.copy2(source_path, destination_path)
    else:
        print(f"{ERROR_STRING} Path '{source_path}' was not found.")


def main():

    main_dir = os.path.dirname(sys.argv[0])
    config_path = os.path.join(main_dir, "config.json")
    output_name = str(int(time.time()))
    
    # reading command line arguments
    for index, arg in enumerate(sys.argv):
        if arg in ["-h", "--help"]:
            print("Arguments:")
            arguments = {
                "config": "Specifies the path to the configuration file. By default the path './config.json' is used.",
                "help": "Displays this message.",
                "name": "Specifies the name of the destination folder (not the path!). By default the name is set to the current unix timestamp."
            }
            for argument, description in arguments.items():
                print(f"{set_string_length(f'-{argument[0]}, --{argument}', 16)} - {description}")
            return
        elif arg in ["-c", "--config"]:
            if len(sys.argv) > index + 1 and sys.argv[index + 1][0] != '-':
                config_path = sys.argv[index + 1]
            else:
                exit(f"{ERROR_STRING} -c: config path expected.")
        elif arg in ["-n", "--name"]:
            if len(sys.argv) > index + 1 and sys.argv[index + 1][0] != '-':
                output_name = sys.argv[index + 1]
            else:
                exit(f"{ERROR_STRING} -n: name of output directory expected.")
    
    # reading config file
    if os.path.isfile(config_path) is False:
        exit(f"{ERROR_STRING} Config file '{config_path}' not found.")
    else:
        print(f"{INFO_STRING} Reading config file.")
        with open(config_path, "r") as file:
            config_dict = json.load(file)
        destination_path = os.path.join(config_dict["destination_path"], output_name) + '/'
        source_path_directory = config_dict["source_list"]
        ignore_list = config_dict["ignore_list"]
        shortcuts = config_dict["shortcuts"]
    
    # copying files
    print(f"{INFO_STRING} Starting the copy process to '{destination_path}'.")
    if os.path.isdir(destination_path) is False:
        os.makedirs(destination_path)
    for destination_directory, source_path_list in source_path_directory.items():
        for path in source_path_list:
            for short, full in shortcuts.items():
                path = path.replace(short, full)
            if destination_directory == "root":
                print(f"{INFO_STRING} Copying '{path}'.")
                copy_item(path, destination_path, ignore_list)
            else:
                print(f"{INFO_STRING} Copying to '{destination_directory}': '{path}'.")
                combined_destination_path = os.path.join(destination_path, destination_directory)
                if os.path.isdir(combined_destination_path) is False:
                    os.makedirs(combined_destination_path)
                copy_item(path, combined_destination_path, ignore_list)
    
    print(f"{DONE_STRING} Copied.")


if __name__ == "__main__":
    
    main()