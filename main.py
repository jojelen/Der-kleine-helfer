#!/usr/bin/python3.7

import argparse

# Der kleine Helfer
from helfer.cookbook import CookBook


parser = argparse.ArgumentParser(
    description="Creates recipes and shopping lists from Hellofresh recipe data"
)
parser.add_argument(
    "-v", "--verbose", help="increase output verbosity", action="store_true"
)
parser.add_argument(
    "-c", "--count", type=int, default=4, help="Number of recipes to print."
)
parser.add_argument(
    "-r", "--random", action="store_true", help="Sends it immediately without asking."
)


def choose_recipes(num):
    cb = CookBook("config.ini")

    # Propose random recipes.
    while True:
        randRecipes = cb.get_rand_recipes_ids(num)

        print(
            "\n{} random {} from Der kleine helfer:".format(
                num, "recipes" if num > 1 else "recipe"
            )
        )
        for idx, i in enumerate(randRecipes):
            print("{}.) {}".format(idx + 1, cb.get_recipe_title(i)))

        print("\nSend in email (e) Print recipes (p) New recipes (n)")
        choice = input("Choice: ")
        if choice == "n":
            continue
        elif choice == "e":
            cb.send_recipes(randRecipes)
        elif choice == "p":
            for i in randRecipes:
                cb.print_recipe(i)
        break


def send_recipes(num):
    cb = CookBook("config.ini")
    randRecipes = cb.get_rand_recipes_ids(num)

    print(
        "\n{} random {} from Der kleine helfer:".format(
            num, "recipes" if num > 1 else "recipe"
        )
    )
    for idx, i in enumerate(randRecipes):
        print("{}.) {}".format(idx + 1, cb.get_recipe_title(i)))

    cb.send_recipes(randRecipes)


def main():
    args = parser.parse_args()

    if args.verbose:
        print(
            "Running Der kleine Helfer with verbose=true, count={}".format(args.count)
        )

    if args.random:
        send_recipes(args.count)
    else:
        choose_recipes(args.count)


if __name__ == "__main__":
    main()
