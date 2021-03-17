DOG_BREEDS = []
DOG_COATS = [
    "Hairless",
    "Short",
    "Medium",
    "Long",
    "Wire",
    "Curly"
]
DOC_COLOR = [
    "Apricot / Beige",
    "Bicolor",
    "Black",
    "Brindle",
    "Brown / Chocolate",
    "Golden",
    "Gray / Blue / Silver",
    "Harlequin",
    "Merle (Blue)",
    "Merle (Red)",
    "Red / Chestnut / Orange",
    "Sable",
    "Tricolor (Brown, Black, & White)",
    "White / Cream",
    "Yellow / Tan / Blond / Fawn"
]
#
RABBIT_COATS = [
    "Short",
    "Long"
]
RABBIT_COLORS = [
    "Agouti",
    "Black",
    "Blue / Gray",
    "Brown / Chocolate",
    "Cream",
    "Lilac",
    "Orange / Red",
    "Sable",
    "Silver Marten",
    "Tan",
    "Tortoiseshell",
    "White"
]
#
BIRD_COLORS = [
    "Black",
    "Blue",
    "Brown",
    "Buff",
    "Gray",
    "Green",
    "Olive",
    "Orange",
    "Pink",
    "Purple / Violet",
    "Red",
    "Rust / Rufous",
    "Tan",
    "White",
    "Yellow"
]


def petOption(form, type):
    if type == "dog":
        form.petType.choices = [('dog', 'Dog'), ('cat', 'Cat'), ("barnyard", "Barnyard"), ('bird', 'Bird'), (
            "horse", "Horse"), ("rabbit", "Rabbit"), ("small-furry", "Small-Furry"), ("scales-fins-other", "Scales-Fins-Other")]
        form.age.choices = [("baby", "Puppy"),
                            ("young", "Young"), ("adult", "Adult"), ("senior", "Senior")]
        form.breed.choices = [("labrador-retriever", "Labrador Retriever"), (
            'golden-retriever', "Golden Retriever"), ('german-shepherd', 'German Shepherd')]
    elif type == "cat":
        form.petType.choices = [('cat', 'Cat'), ('dog', 'Dog'), ("barnyard", "Barnyard"), ('bird', 'Bird'), (
            "horse", "Horse"), ("rabbit", "Rabbit"), ("small-furry", "Small-Furry"), ("scales-fins-other", "Scales-Fins-Other")]
        form.age.choices = [("baby", "Kitten"),
                            ("young", "Young"), ("adult", "Adult"), ("senior", "Senior")]
        form.breed.choices = [('american-bobtail', 'American Bobtail'), ("persian", "Persian"),
                              ("maine-Coon", "Maine Coon"), ("bengal", "Bengal"), ('british-shorthair', 'British Shorthair'), ('persian-cat', 'Persian Cat')]
    elif type == 'rabbit':
        form.petType.choices = [('rabbit', 'Rabbit'), ('cat', 'Cat'), ('dog', 'Dog'), ("barnyard", "Barnyard"), ('bird', 'Bird'), (
            "horse", "Horse"), ("small-furry", "Small-Furry"), ("scales-fins-other", "Scales-Fins-Other")]
        form.breed.choices = [('american'), ('American'), ('american-sable', 'American Sable'), (
            'angora-rabbit', 'Angora Rabbit'), ('belgian-hare', 'Belgian Hare')]
    return form
    # form.coat = [('small', 'Small'), ('long', 'Long')]
    # form.color = [('agouti', 'Agouti'), ('black', 'Black'), ('blue-gray',
    '''                                                        'Blue/Gray'), ('brown-chocolate', 'Brown/Chocolate'), ('cream', 'Cream'), ('lilac', 'Lilac'), ('orange-red', 'Orange/Red'), ('sable', 'Sable'), ('silvermarten', "Silver Marten"), ('tan', 'Tan'), ('tortoiseshell', 'Tortoiseshell'), ('white', 'White')]
    elif type == 'small-furry':
        form.petType.choices = [("small-furry", "Small-Furry"), ('dog', 'Dog'), ('cat', 'Cat'), ("barnyard", "Barnyard"), ('bird', 'Bird'), (
            "horse", "Horse"), ("rabbit", "Rabbit"), ("scales-fins-other", "Scales-Fins-Other")]
        form.breed.choices = [('abyssinian', 'Abyssinian'), ('chinchilla', 'Chinchilla'), (
            'degu', 'Degu'), ('dwarf-hamster', 'Dwarf Hamster'), ('ferret', 'Ferret'), ('gerbil', 'Gerbil'), ('guinea-pig', 'Guinea Pig'), ('hamster', 'Hamster'), ('hedgehog', 'Hedgehog'), ('mouse', 'Mouse'), ('peruvian', 'Peruvian'), ('prairie-dog', 'Prairie Dog'), ('rat', 'Rat'),
            ('rex', 'Rex'), ('short-haired', 'Short-Haired'), ('silkie-sheltie', 'Silkie/Sheltie'), ('skunk', 'Skunk'), ('sugar-glider', 'Sugar Glider'), ('teddy', 'Teddy')]
        form.species.choices = [('chinchilla', 'Chinchilla'), ('degu', 'Degu'), ('ferret', 'Ferret'), ('gerbil', 'Gerbil'), (
            'guinea-pig', 'Guinea Pig'), ('hamster', 'Hamster'), ('hedgehog', 'Hedgehog'), ('mouse', 'Mouse'), ('prairie-dog', 'Prairie Dog'), ('rat', 'Rat'), ('skunk', 'Skunk'), ('sugar-glider', 'Sugar Glider')]
        form.coat.choices = [('hairless', 'Hairless'),
                             ('small', 'Small'), ('long', 'Long')]
        form.color.choices = [[('agouti', 'Agouti'), ('albino', 'Albino'), ('black', 'Black'), ('black-sable', 'Black Sable'), ('blue-gray',
                                                                                                                                'Blue/Gray'), ('brown-chocolate', 'Brown/Chocolate'), ('calico', 'Calico'), ('cinnamon', 'Cinnamon'), ('cream', 'Cream'), ('orange-red', 'Orange/Red'), ('sable', 'Sable'), ('tan', 'Tan'), ('tortoiseshell', 'Tortoiseshell'), ('white', 'White'), ('white-dark-eyed', 'White (Dark-Eyed')]]
    elif type == 'horse':
        form.petType.choices = [("horse", "Horse"), ('dog', 'Dog'), ('cat', 'Cat'), ("barnyard", "Barnyard"), (
            'bird', 'Bird'), ("rabbit", "Rabbit"), ("small-furry", "Small-Furry"), ("scales-fins-other", "Scales-Fins-Other")]
        form.species.choices = [('donkey', 'Donkey'), ('horse', 'Horse'), (
            'miniature-horse', 'Miniature Horse'), ('mule', 'Mule'), ('pony', 'Pony')]
        form.breed.choices = [('appaloose', 'Appaloosa'), ('arabian', 'Arabian'), ('belgian', 'Belgian'), ('clydesdale',
                                                                                                           'Clydesdale'), ('connemara', 'Connemara'), ('curly-horse', 'Curly Horse'), ('donkey', 'Donkey'), ('draft', 'Draft')]
    elif type == 'birds':
        form.petType.choices = [('bird', 'Bird'), ('dog', 'Dog'), ('cat', 'Cat'), ("barnyard", "Barnyard"), (
            "horse", "Horse"), ("rabbit", "Rabbit"), ("small-furry", "Small-Furry"), ("scales-fins-other", "Scales-Fins-Other")]
        form.species.choices = []
        form.breed.choices = []
    elif type == 'scales-fins-other':
        form.petType.choices = [("scales-fins-other", "Scales-Fins-Other"), ('dog', 'Dog'), ('cat', 'Cat'), ("barnyard", "Barnyard"), ('bird', 'Bird'), (
            "horse", "Horse"), ("rabbit", "Rabbit"), ("small-furry", "Small-Furry")]
        form.species.choices = []
        form.breed.choices = []
    elif type == 'barnyard':
        form.petType.choices = [("barnyard", "Barnyard"), ('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), (
            "horse", "Horse"), ("rabbit", "Rabbit"), ("small-furry", "Small-Furry"), ("scales-fins-other", "Scales-Fins-Other")]
        form.species.choices = []
        form.breed.choices = []
    '''


def searchOption(form, type):
    if type == "dog":
        form.type.choices = [('dog', 'Dog'), ('cat', 'Cat'), ("barnyard", "Barnyard"), ('bird', 'Bird'), (
            "horse", "Horse"), ("rabbit", "Rabbit"), ("small-furry", "Small-Furry"), ("scales-fins-other", "Scales-Fins-Other")]
        form.age.choices = [("baby", "Puppy"),
                            ("young", "Young"), ("adult", "Adult"), ("senior", "Senior")]
        form.breed.choices = [("labrador-retriever", "Labrador Retriever"), (
            'golden-retriever', "Golden Retriever"), ('german-shepherd', 'German Shepherd')]
    elif type == "cat":
        form.type.choices = [('cat', 'Cat'), ('dog', 'Dog'), ("barnyard", "Barnyard"), ('bird', 'Bird'), (
            "horse", "Horse"), ("rabbit", "Rabbit"), ("small-furry", "Small-Furry"), ("scales-fins-other", "Scales-Fins-Other")]
        form.age.choices = [("baby", "Kitten"),
                            ("young", "Young"), ("adult", "Adult"), ("senior", "Senior")]
        form.breed.choices = [('american-bobtail', 'American Bobtail'), ("persian", "Persian"),
                              ("maine-Coon", "Maine Coon"), ("bengal", "Bengal"), ('british-shorthair', 'British Shorthair'), ('persian-cat', 'Persian Cat')]

    return form
    # ('angora-rabbit', 'Angora Rabbit'), ('belgian-hare', 'Belgian Hare')]
    #form.coat = [('small', 'Small'), ('long', 'Long')]
    # form.color = [('agouti', 'Agouti'), ('black', 'Black'), ('blue-gray', 'Blue/Gray'), ('brown-chocolate', 'Brown/Chocolate'), ('cream', 'Cream'), ('lilac', 'Lilac'), ('orange-red', 'Orange/Red'), ('sable', 'Sable'), ('silvermarten', "Silver Marten"), ('tan', 'Tan'), ('tortoiseshell', 'Tortoiseshell'), ('white', 'White')]
    '''
    elif type == 'small-furry':
        form.type.choices = [("small-furry", "Small-Furry"), ('dog', 'Dog'), ('cat', 'Cat'), ("barnyard", "Barnyard"), ('bird', 'Bird'), (
            "horse", "Horse"), ("rabbit", "Rabbit"), ("scales-fins-other", "Scales-Fins-Other")]
        form.breed.choices = [('abyssinian', 'Abyssinian'), ('chinchilla', 'Chinchilla'), (
            'degu', 'Degu'), ('dwarf-hamster', 'Dwarf Hamster'), ('ferret', 'Ferret'), ('gerbil', 'Gerbil'), ('guinea-pig', 'Guinea Pig'), ('hamster', 'Hamster'), ('hedgehog', 'Hedgehog'), ('mouse', 'Mouse'), ('peruvian', 'Peruvian'), ('prairie-dog', 'Prairie Dog'), ('rat', 'Rat'),
            ('rex', 'Rex'), ('short-haired', 'Short-Haired'), ('silkie-sheltie', 'Silkie/Sheltie'), ('skunk', 'Skunk'), ('sugar-glider', 'Sugar Glider'), ('teddy', 'Teddy')]
        form.species.choices = [('chinchilla', 'Chinchilla'), ('degu', 'Degu'), ('ferret', 'Ferret'), ('gerbil', 'Gerbil'), (
            'guinea-pig', 'Guinea Pig'), ('hamster', 'Hamster'), ('hedgehog', 'Hedgehog'), ('mouse', 'Mouse'), ('prairie-dog', 'Prairie Dog'), ('rat', 'Rat'), ('skunk', 'Skunk'), ('sugar-glider', 'Sugar Glider')]
        form.coat.choices = [('hairless', 'Hairless'),
                             ('small', 'Small'), ('long', 'Long')]
        form.color.choices = [[('agouti', 'Agouti'), ('albino', 'Albino'), ('black', 'Black'), ('black-sable', 'Black Sable'), ('blue-gray',
                                                                                                                                'Blue/Gray'), ('brown-chocolate', 'Brown/Chocolate'), ('calico', 'Calico'), ('cinnamon', 'Cinnamon'), ('cream', 'Cream'), ('orange-red', 'Orange/Red'), ('sable', 'Sable'), ('tan', 'Tan'), ('tortoiseshell', 'Tortoiseshell'), ('white', 'White'), ('white-dark-eyed', 'White (Dark-Eyed')]]
    elif type == 'horse':
        form.type.choices = [("horse", "Horse"), ('dog', 'Dog'), ('cat', 'Cat'), ("barnyard", "Barnyard"), (
            'bird', 'Bird'), ("rabbit", "Rabbit"), ("small-furry", "Small-Furry"), ("scales-fins-other", "Scales-Fins-Other")]
        form.species.choices = [('donkey', 'Donkey'), ('horse', 'Horse'), (
            'miniature-horse', 'Miniature Horse'), ('mule', 'Mule'), ('pony', 'Pony')]
        form.breed.choices = [('appaloose', 'Appaloosa'), ('arabian', 'Arabian'), ('belgian', 'Belgian'), ('clydesdale',
                                                                                                           'Clydesdale'), ('connemara', 'Connemara'), ('curly-horse', 'Curly Horse'), ('donkey', 'Donkey'), ('draft', 'Draft')]
    elif type == 'birds':
        form.type.choices = [('bird', 'Bird'), ('dog', 'Dog'), ('cat', 'Cat'), ("barnyard", "Barnyard"), (
            "horse", "Horse"), ("rabbit", "Rabbit"), ("small-furry", "Small-Furry"), ("scales-fins-other", "Scales-Fins-Other")]
        form.species.choices = []
        form.breed.choices = []
    elif type == 'scales-fins-other':
        form.type.choices = [("scales-fins-other", "Scales-Fins-Other"), ('dog', 'Dog'), ('cat', 'Cat'), ("barnyard", "Barnyard"), ('bird', 'Bird'), (
            "horse", "Horse"), ("rabbit", "Rabbit"), ("small-furry", "Small-Furry")]
        form.species.choices = []
        form.breed.choices = []
    elif type == 'barnyard':
        form.type.choices = [("barnyard", "Barnyard"), ('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), (
            "horse", "Horse"), ("rabbit", "Rabbit"), ("small-furry", "Small-Furry"), ("scales-fins-other", "Scales-Fins-Other")]
        form.species.choices = []
        form.breed.choices = [] '''
