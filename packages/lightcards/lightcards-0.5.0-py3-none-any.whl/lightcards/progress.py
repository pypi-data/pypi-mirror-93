# Save and resume progress in lightcards
# Armaan Bhojwani 2021

import hashlib
import os
import pickle
import shutil

global dired
dired = f"{os.path.expanduser('~')}/.cache/lightcards/"


def name_gen(stra):
    hasher = hashlib.md5()
    hasher.update(str(stra).encode("utf-8"))
    return(hasher.hexdigest())


def make_dirs(dired):
    if not os.path.exists(dired):
        os.makedirs(dired)


def dump(obj, stra):
    make_dirs(dired)

    pickle.dump(obj, open(f"{dired}/{name_gen(stra)}.p", "wb"))


def dive(stra):
    file = f"{dired}/{name_gen(stra)}.p"
    make_dirs(dired)
    if os.path.exists(file):
        return pickle.load(open(file, "rb"))
    else:
        return False


def purge(stra):
    file = f"{dired}/{name_gen(stra)}/"
    if os.path.exists(file):
        shutil.rmtree(file)


def purge_all():
    if os.path.exists(dired):
        shutil.rmtree(dired)
