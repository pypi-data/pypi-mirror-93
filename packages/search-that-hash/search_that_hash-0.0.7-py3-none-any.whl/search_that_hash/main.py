import json
from name_that_hash import runner

import click
import sys
from appdirs import *

import toml

try:
    import cracking, printing
except ModuleNotFoundError:
    from search_that_hash import cracking, printing

from loguru import logger

logger.add(
    sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO"
)

logger.remove()

@click.command()
@click.option("--timeout", type=int, help="Choose timeout time in second", default=1)
@click.option("--text", "-t", type=str, help="Crack a single hash")
@click.option(
    "--offline",
    "-o",
    is_flag=True,
    default=False,
    type=bool,
    help="Use offline mode. Does not search for hashes.",
)
@click.option(
    "-f",
    "--file",
    type=click.File("r"),
    required=False,
    help="The file of hashes, seperated by newlines.",
)
@click.option(
    "-w", "--wordlist", type=str, required=False, help="The wordlist."
)
@click.option(
    "--config", type=click.File("r"), required=False, help="File of config"
)
@click.option("--hashcat", is_flag=True, help="Runs Hashcat instead of John")
@click.option("--where", is_flag=True, help="Prints config file location")
@click.option("--greppable", is_flag=True, help="Used to grep")
@click.option("-b","--binary", type=str, required=False, help="Location of hashcat / john folder (if using windows)")

def main(**kwargs):

    if kwargs["where"] == True:
        print(find_appdirs_location())
        exit(0)

    config = {}

    if kwargs["config"] != None:
        try:
            config["api_kys"] = toml.loads(kwargs["config"])
        except:
            config["api_keys"] = None
    else:
        # if no config is manually provided
        # check to see if one exists at appdirs
        # if it doesn't, it'll result to None
        config["api_keys"] = read_config_file()

    if kwargs["text"] != None:
        config["hashes"] = [kwargs["text"]]
    elif kwargs["file"] != None:
        config["hashes"] = "".join(list(kwargs["file"])).split("\n")
    else:
        print("Error. No hashes were inputted. Use the help menu --help")
        exit(0)

    if kwargs["binary"]:
        config["binary"] = kwargs["binary"]
    else:
        config["binary"] = False

    config["hashes"] = create_hash_config(config)

    config["offline"] = kwargs["offline"]
    config["wordlist"] = kwargs["wordlist"]
    config["hashcat"] = kwargs["hashcat"]
    config["timeout"] = kwargs["timeout"]
    config["greppable"] = kwargs["greppable"]
    config["api"] = False

    if not kwargs["greppable"]:
        printing.Prettifier.banner()

    searcher = cracking.Searcher(config)
    results = cracking.Searcher.main(searcher)

    if kwargs["greppable"]:
        printing.Prettifier.grepable_print(results)

    exit(0)

def return_as_json(hashes):

    config = {}

    config["offline"] = False
    config["api_keys"] = False
    config["wordlist"] = False
    config["hashcat"] = False
    config["timeout"] = 1
    config["greppable"] = True
    config["hashes"] = hashes
    config["binary"] = False
    config["hashes"] = create_hash_config(config)
    config["api"] = False

    searcher = cracking.Searcher(config)

    return json.dumps(cracking.Searcher.main(searcher))

def return_as_fast_json(hashes):

    config = {}

    config["offline"] = False
    config["api_keys"] = False
    config["wordlist"] = False
    config["hashcat"] = False
    config["timeout"] = 1
    config["greppable"] = False
    config["hashes"] = hashes
    config["binary"] = False
    config["hashes"] = create_hash_config(config)
    config["api"] = True

    searcher = cracking.Searcher(config)

    print(cracking.Searcher.main(searcher))
        

def create_hash_config(config):
    return json.loads(runner.api_return_hashes_as_json(config["hashes"]))


def read_config_file():
    return read_and_parse_config_file(find_appdirs_location())


def find_appdirs_location():
    # TODO make this OS independent the "/" makes it Windows specific
    # print(user_config_dir("HashSearch", "Bee-san") + "/config.toml")
    return user_config_dir("HashSearch", "Bee-san") + "/config.toml"


def read_and_parse_config_file(file):
    config_to_parse = read_file(file)

    if config_to_parse == None:
        return config_to_parse
    else:
        try:
            return toml.loads(config_to_parse)
        except:
            return None

def read_file(file):
    try:
        with open(file, "r") as out:
            return out.read()
    except:
        return None
    
if __name__ == "__main__":
    main()
