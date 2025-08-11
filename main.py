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
        log_print("error", f"Path '{source_path}' was not found.")


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
        destination_path = os.path.join(config_dict["destination_path"], output_name) + '/'
        source_path_directory = config_dict["source_list"]
        ignore_list = config_dict["ignore_list"]
    
    # copying files
    log_print("info", f"Starting the copy process to '{destination_path}'.")
    if os.path.isdir(destination_path) is False:
        os.makedirs(destination_path)
    for destination_directory, source_path_list in source_path_directory.items():
        for path in source_path_list:
            if destination_directory == "root":
                log_print("info", f"Copying '{path}'.")
                copy_item(path, destination_path, ignore_list)
            else:
                log_print("info", f"Copying to '{destination_directory}': '{path}'.")
                combined_destination_path = os.path.join(destination_path, destination_directory)
                if os.path.isdir(combined_destination_path) is False:
                    os.makedirs(combined_destination_path)
                copy_item(path, combined_destination_path, ignore_list)
    
    log_print("done", "Copied.")


if __name__ == "__main__":
    
    main()