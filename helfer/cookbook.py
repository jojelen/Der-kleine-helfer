import pandas as pd
import random
import os
import io
import sys
import shutil
from configparser import ConfigParser

import helfer.utils as utils
import helfer.email as email
from helfer.classification import categorize, ItemCategory


def print_paragraph(par, f, html):
    if html is True:
        par = "<p>{}</p>".format(par)
    print("\n{}".format(par), file=f)

def print_href(par, f, url):
    if url is not None:
        par = "<p><a href=\"{}\">{}</a></p>".format(url,par)
    print("\n{}".format(par), file=f)

def print_header(title, size, f, html):
    if html:
        title = "<h{}>{}</h{}>".format(size, title, size)
    else:
        lineChar = '-' if size > 1 else '='
        lineLength = 79
        line = lineChar*lineLength
        title = "\n{}\n{}\n{}\n".format(line, title, line)
    print(title, file=f)


def print_ingredients(ingredients, f=sys.stdout, html=False, title="Ingredients"):
    print_header(title, 2, f, html)
    previousCategory = ItemCategory.UNKNOWN
    for ing in ingredients:
        if 'category' in ing and ing['category'] != previousCategory:
            print_header(ing['category'], 4, f, html)
            previousCategory = ing['category']
        if ing['quantity'] != -1:
            print_paragraph("{}: {} {}".format(ing['name'],
                                               ing['quantity'], ing['unit']), f,
                            html)
        else:
            print_paragraph("{}".format(ing['name']), f, html)


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
    def __init__(self, configPath):
        self.cfg = ConfigParser()
        self.cfg.read(configPath)

        dataDir = self.cfg.get('run', 'datadir')
        foundJsons = utils.find("*.json", dataDir)
        if len(foundJsons) == 0:
            raise FileNotFoundError(
                "Could not find any json files in {}".format(dataDir))
        self.df = utils.merge_jsons(foundJsons)

        self.dataDir = dataDir

    def get_rand_recipes_ids(self, num):
        assert(num is not None)
        num_recipes = len(self.df)
        return random.sample(range(0, num_recipes - 1), num)

    def get_recipe_title(self, idx):
        return self.df.loc[idx, 'recept']

    def get_recipe_url(self, idx):
        return self.df.loc[idx, 'url']

    def combine_ingredients(self, idxs):
        ingredients = []
        for idx, i in enumerate(idxs):
            for ing in self.df.loc[i, 'ingredients']:
                add_ingredient(ingredients, ing)

        ingredients = sorted(ingredients, key=lambda x: x['name'])
        categorize(ingredients)
        return sorted(ingredients, key=lambda x: x['category'])

    def send_recipes(self, idxs):
        self.copy_tmp_files(idxs)

        emailContentFile = os.path.join(
            self.cfg.get('run', 'tmpdir'), 'emailcontent.html')
        with open(emailContentFile, 'wt') as f:
            self.print_recipes(idxs, f=f, html=True)

        email.send_file_as_email(self.cfg, emailContentFile)

    def print_recipes(self, idxs, f=sys.stdout, html=False):
        ingredients = self.combine_ingredients(idxs)

        num = len(idxs)
        if num > 1:
            desc = "Here are {} recipes from Der kleine Helfer:".format(num)
        else:
            desc = "Here is {} recipe from Der kleine Helfer:".format(num)

        print_paragraph(desc, f, html)
        for idx, i in enumerate(idxs):
            url = self.get_recipe_url(i) if html else None
            print_href("{}.) {}".format(idx + 1, self.get_recipe_title(i)),
                            f, url)

        print_paragraph(
            "The ingredients in each recipe are calculated for 2 portions", f, html)
        print_ingredients(ingredients, f=f, html=html, title="Grocery list")

        for i in idxs:
            self.print_recipe(i, f=f, html=html)

    def print_recipe(self, i, f=sys.stdout, html=False):
        print_header("{}:".format(self.df.loc[i, 'recept']), 1, f, html)

        ingredients = self.df.loc[i, 'ingredients']
        ingredients = sorted(ingredients, key=lambda x: x['name'])
        categorize(ingredients)
        ingredients = sorted(ingredients, key=lambda x: x['category'])
        print_ingredients(ingredients, f=f, html=html)

        print_header("Instructions:", 2, f, html)
        for i, inst in enumerate(self.df.loc[i, 'instructions']):
            print_paragraph("{}: {}".format(i+1, inst), f, html)

    def copy_tmp_files(self,  idxs):
        tmp_dir = self.cfg.get('run', 'tmpdir')
        if os.path.isdir(tmp_dir):
            for tmpFile in os.listdir(tmp_dir):
                if tmpFile.endswith(".pdf"):
                    os.remove(os.path.join(tmp_dir, tmpFile))
        else:
            os.mkdir(tmp_dir)

        for i in idxs:
            if self.df.loc[i, 'pdf'] != '':
                shutil.copyfile(os.path.join(self.dataDir, self.df.loc[i, 'pdf']), os.path.join(
                    tmp_dir, self.df.loc[i, 'pdf']))
