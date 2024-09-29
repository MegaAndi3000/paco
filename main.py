import os
import sys
import time
import json
import shutil


def copy_item(source_path: str, destination_path: str, ignore_list: list):
    """Copies a file or directory to a given directory.

    Args:
        source_path (str): path to the source directory/file
        destination_path (str): path to the destination directory
        ignore_list (str[]): list of patterns, which are to be ignored when copying
    """

    ignore_patterns = shutil.ignore_patterns(*ignore_list)
    if source_path[-1] in ['/', '\\']:
        shutil.copytree(source_path, destination_path, ignore=ignore_patterns)
    else:
        shutil.copy2(source_path, destination_path)


def main():

    main_dir = os.path.dirname(__file__)
    config_path = os.path.join(main_dir, "config.json")
    
    # reading command line arguments
    for index, arg in enumerate(sys.argv):
        if arg in ["-c", "--config"]:
            if len(sys.argv) > index + 1:
                config_path = sys.argv[index + 1]
            else:
                print("-c: config path expected.")
    
    # reading config file
    with open(config_path, "r") as file:
        config_dict = json.load(file)
    destination_path = config_dict["destination_path"] + f"{int(time.time())}/"
    source_path_list = config_dict["source_list"]
    ignore_list = config_dict["ignore_list"]
    
    # copying files
    for source_path in source_path_list:
        copy_item(source_path, destination_path, ignore_list)


if __name__ == "__main__":
    
    main()