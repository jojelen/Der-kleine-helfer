#!/usr/bin/python3

import argparse
import os
import io
import sys
from configparser import ConfigParser

# Der kleine Helfer
from helfer.cookbook import CookBook
import helfer.email as email

cfg = ConfigParser()
cfg.read('config.ini')

dataDir = "/mnt/sda2/camus/github/hellofresh/data"

parser = argparse.ArgumentParser(
    description='Creates recipes and shopping lists from Hellofresh recipe data')
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("mode", type=str,
                    help="Choose what to perform (rand, debug).")
parser.add_argument("-c", "--count", type=int,
                    help="Number of recipes to print.")


def print_random_recipes(num):
    cb = CookBook(dataDir)

    randRecipes = cb.get_rand_recipes_ids(num)
    cb.print_recipes(randRecipes)
    cb.copy_tmp_files(cfg,  randRecipes)

def print_debug():
    pass


def main():
    args = parser.parse_args()

    if args.verbose:
        print("Running {} with verbose=true".format(args.mode))

    if args.mode == "rand":
        print_random_recipes(args.count)
    elif args.mode == "debug":
        print_debug()
    else:
        SystemExit("ERROR: Not a valid mode.")


if __name__ == "__main__":
    main()
