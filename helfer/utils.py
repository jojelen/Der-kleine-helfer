import os
import fnmatch
import pandas as pd
import json
import re


def find(pattern, path):
    """
    Returns a list of files in path that matches the pattern.
    """
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def merge_jsons(jsons):
    """
    Merges a list of json files (paths) into a pandas dataframe.
    """
    if len(jsons) == 0:
        SystemExit("ERROR: No jsons to merge.")

    dfs = []
    for f in jsons:
        dfs.append(pd.read_json(f))
    df = pd.concat(dfs, ignore_index=True, verify_integrity=True)
    df.drop_duplicates(subset=["recept"], inplace=True)
    df["recept"] = df["recept"].apply(lambda x: re.sub(" Recept$", "", x))

    return df.reset_index(drop=True)
