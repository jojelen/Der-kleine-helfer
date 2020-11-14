import pandas as pd
import random
import os
import io
import sys
import shutil
import re

import helfer.utils as utils
from helfer.classification import categorize, ItemCategory


def print_ingredients(ingredients, f=sys.stdout):
    print("\nIngredients:", file=f)
    previousCategory = ItemCategory.UNKNOWN
    for ing in ingredients:
        if 'category' in ing and ing['category'] != previousCategory:
            print("\n{}\n{}\n{}\n".format('-'*20, ing['category'], '-'*20),
                  file=f)
            previousCategory = ing['category']
        if ing['quantity'] != -1:
            print("{}: {} {}".format(ing['name'],
                                     ing['quantity'], ing['unit']), file=f)
        else:
            print("{}".format(ing['name']), file=f)


def add_ingredient(ingredients, ing):
    '''
    Adds an ingredient to list.
    '''
    append_ingredient = True
    for el in ingredients:
        # TODO: Maybe one can convert between different units?
        if el['name'] == ing['name']:
            if el['unit'] == ing['unit'] and el['unit'] != -1:
                append_ingredient = False
                el['quantity'] = float(el['quantity']) + float(ing['quantity'])
            elif el['unit'] == ing['unit'] and el['unit'] == -1:
                append_ingredient = False

    if append_ingredient:
        ingredients.append(ing)


class CookBook:
    def __init__(self, dataDir):
        foundJsons = utils.find("*.json", dataDir)
        self.df = utils.merge_jsons(foundJsons)
        #f = open('/tmp/hellofresh/tmp.txt', 'wt')
        self.f = io.StringIO()
        self.dataDir = dataDir

    def get_rand_recipes_ids(self, num):
        num_recipes = len(self.df)
        return random.sample(range(0, num_recipes - 1), num)

    def print_recipes(self, randRecipes):
        ingredients = []
        for idx, i in enumerate(randRecipes):
            for ing in self.df.loc[i, 'ingredients']:
                add_ingredient(ingredients, ing)
            print("{}.) {}".format(idx + 1, self.df.loc[i, 'recept']), file=self.f)
            print("{}.) {}".format(idx + 1, self.df.loc[i, 'recept']))

        ingredients = sorted(ingredients, key=lambda x: x['name'])
        categorize(ingredients)
        ingredients = sorted(ingredients, key=lambda x: x['category'])

        num = len(randRecipes)
        if num > 1:
            print("Here are {} random recipes from Hellofresh:".format(num), file=self.f)
        else:
            print("Here is {} random recipe from Hellofresh:".format(num), file=self.f)
        print_ingredients(ingredients, f=self.f)
        print('\n\n', file=self.f)
        for i in randRecipes:
            self.print_recipe(i)

        print(self.f.getvalue())

    def print_recipe(self, i):
        print("Recept: {}:".format(self.df.loc[i, 'recept']), file=self.f)

        ingredients = self.df.loc[i, 'ingredients']
        ingredients = sorted(ingredients, key=lambda x: x['name'])
        categorize(ingredients)
        ingredients = sorted(ingredients, key=lambda x: x['category'])
        print_ingredients(ingredients, f=self.f)

        print("\nInstructions:", file=self.f)
        for i, inst in enumerate(self.df.loc[i, 'instructions']):
            print("{}: {}\n".format(i+1, inst), file=self.f)

    def copy_tmp_files(self, cfg, randRecipes):
        tmp_dir = cfg.get('run', 'tmpdir')
        if os.path.isdir(tmp_dir):
            for tmpFile in os.listdir(tmp_dir):
                if tmpFile.endswith(".pdf"):
                    os.remove(os.path.join(tmp_dir, tmpFile))
        else:
            os.mkdir(tmp_dir)

        for i in randRecipes:
            if self.df.loc[i, 'pdf'] != '':
                shutil.copyfile(os.path.join(self.dataDir, self.df.loc[i, 'pdf']), os.path.join(
                    tmp_dir, self.df.loc[i, 'pdf']))
