from enum import Enum

# Description of each ItemCategory.
categoryDescription = {
    "UNKNOWN": "Övrigt",
    "GREEN": "Grönt",
    "DAIRY": "Mjölk/ost",
    "BREAD": "Bröd",
    "MEAT": "Kött/fisk",
    "BASIC": "Basvaror",
    "CARBS": "kolhydrater",
}
# Keywords to search for when categorizing.
categoryKeywords = {
    "GREEN": [
        "lök",
        "paprika",
        "gurka",
        "tomat",
        "sallad",
        "potatis",
        "zucchini",
        "frukt",
        "äppel",
        "apelsin",
        "aubergine",
        "ananas",
        "basilika",
        "koriander",
        "broccoli",
        "pumpa",
        "nötter",
        "citron",
        "äpple",
        "dill",
        "timjan",
        "tranbär",
        "kål",
        "bönor",
        "frön",
        "salvia",
        "linser",
        "spenat",
        "rosmarin",
        "svamp",
        "champinjon",
        "lime",
        "morot",
        "kikärt",
        "morötter",
        "persilja",
        "melon",
        "portabello",
        "oregano",
        "päron",
        "rucola",
        "dragon",
        "selleri",
        "rädisor",
        "majs",
        "mynta",
        "ingefära",
        "mango",
        "portabello",
        "avokado",
        "chili",
        "rödbet",
        "palsternack",
    ],
    "BREAD": ["bröd", "baguette", "ciabatta", "brioche"],
    "DAIRY": ["mjölk", "ost"],
    "MEAT": [
        "kött",
        "kyckling",
        "fläsk",
        "korv",
        "sej",
        "lax",
        "räk",
        "torsk",
        "färs",
        "bacon",
    ],
    "UNKNOWN": ["sataysås", "buljong", "chili flakes", "mix", "honung", "dukkah"],
    "BASIC": ["*"],
    "CARBS": [
        "pasta",
        "ris",
        "nudlar",
        "spaghetti",
        "couscous",
        "penne",
        "bulgur",
        "lasagne",
        "quinoa",
        "mjöl",
        "pommes",
        "tagliatelle",
        "tortilla",
        "deg",
    ],
}


class ItemCategory(Enum):
    UNKNOWN = 99
    BASIC = 98
    BREAD = 2
    MEAT = 5
    DAIRY = 3
    GREEN = 1
    CARBS = 4

    def __str__(self):
        return categoryDescription[self.name]

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


def categorize(ingredients):
    """
    Adds an ItemCategory to every ingredient in the given list.
    """
    for ing in ingredients:
        foundCategory = False
        for category in ItemCategory:
            if category.name not in categoryKeywords:
                continue
            for keyword in categoryKeywords[category.name]:
                if keyword in ing["name"].lower():
                    ing["category"] = category
                    foundCategory = True
                    break
            if foundCategory:
                break
        if foundCategory is False:
            ing["category"] = ItemCategory.UNKNOWN
