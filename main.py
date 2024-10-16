import os
import sys
import time
import json
import shutil


def log_print(type:str, message:str):
    """Prints out a formatted log message. Available types are error, info and done.

    Args:
        type (str): The type of message. Available: error, info, done 
        message (str): The message, which is printed out
    """
    
    bold = "\033[1m"
    red = "\033[31m"
    green = "\033[32m"
    cyan = "\033[36m"
    white = "\033[37m"
    reset = "\033[0m"
    string_list = {"error": f"[{red}ERROR{white}]",
                   "info": f"[{cyan}INFO{white}]",
                   "done": f"[{green}DONE{white}]"}
    
    print(f"{bold}{string_list[type]}{reset}", message)


def copy_item(source_path: str, destination_path: str, ignore_list: list):
    """Copies a file or directory to a given directory.

    Args:
        source_path (str): path to the source directory/file
        destination_path (str): path to the destination directory
        ignore_list (str[]): list of patterns, which are to be ignored when copying
    """

    ignore_patterns = shutil.ignore_patterns(*ignore_list)
    if os.path.isdir(source_path):
        shutil.copytree(source_path, destination_path, ignore=ignore_patterns)
    elif os.path.isfile(source_path):
        shutil.copy2(source_path, destination_path)
    else:
        log_print("error", f"Path '{source_path}' was not found.")


def main():

    main_dir = os.path.dirname(__file__)
    config_path = os.path.join(main_dir, "config.json")
    output_name = str(int(time.time()))
    
    # reading command line arguments
    for index, arg in enumerate(sys.argv):
        if arg in ["-c", "--config"]:
            if len(sys.argv) > index + 1 and sys.argv[index + 1][0] != '-':
                config_path = sys.argv[index + 1]
            else:
                log_print("error", "-c: config path expected. Fallback to 'config.json'.")
        elif arg in ["-n", "--name"]:
            if len(sys.argv) > index + 1 and sys.argv[index + 1][0] != '-':
                output_name = sys.argv[index + 1]
            else:
                log_print("error", f"-n: name of output directory expected. Fallback to '{output_name}'.")
    
    # reading config file
    if os.path.isfile(config_path) is False:
        log_print("error", f"Config file '{config_path}' not found.")
        return
    else:
        log_print("info", "Reading config file.")
        with open(config_path, "r") as file:
            config_dict = json.load(file)
        destination_path = os.path.join(config_dict["destination_path"], output_name)
        source_path_directory = config_dict["source_list"]
        ignore_list = config_dict["ignore_list"]
    
    # copying files
    log_print("info", "Starting the copy process.")
    for destination_directory, source_path_list in source_path_directory.items():
        for path in source_path_list:
            if destination_directory == "root":
                copy_item(path, destination_path, ignore_list)
            else:
                combined_destination_path = os.path.join(destination_path, destination_directory)
                os.makedirs(combined_destination_path)
                copy_item(path, combined_destination_path, ignore_list)
    
    log_print("done", "Copied.")


if __name__ == "__main__":
    
    main()