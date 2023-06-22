import os
import stat

import requests as req
from aqt import mw
from aqt.operations import QueryOp

from .const import EXPECTED_BINARIES, ADDON_PATH, DICT_DIR, USER_PATH, USER_DICT_PATH, BIN_PATH, BASE_URL_BINARIES, \
    BINS_PATH
from aqt.utils import showWarning
import subprocess
import pickle
from functools import partial

import webbrowser


def runAsync(op, *args, success=None, with_progress=False, progress_label="Loading..."):
    if success is None:
        def nothing(*args):
            return
        success = nothing
    op = QueryOp(parent=mw, op=op, success=success, )
    if with_progress:
        op.with_progress(label=progress_label).run_in_background()
        return
    op.run_in_background()


def compileUserDictionaries(*args):
    for dic in os.listdir(USER_DICT_PATH):
        if dic.endswith((".dic", ".txt")):
            compileUserDictionary(dic.split(".")[0])


def compileUserDictionary(name, *args):
    base = os.path.join(USER_DICT_PATH, name)
    tmp_files = []
    if os.path.isfile(base + ".txt"):
        with open(base + ".txt", "rbU") as f:
            line_count = sum(1 for _ in f)
        with open(base + ".txt", 'r') as in_file, open(base + ".dic", 'w') as out_file:
            out_file.write(str(line_count) + "\n")
            for line in in_file:
                out_file.write(line)
            tmp_files.append(out_file.name)
    if not os.path.isfile(base + ".dic"):
        return
    if not os.path.isfile(base + ".aff"):
        unique_chars = set()
        with open(base + ".dic", 'r') as file:
            for line in file:
                for char in line:
                    unique_chars.add(char)
        content = f"SET UTF-8\nTRY {''.join(unique_chars)}\n"
        with open(base + ".aff", 'w') as file:
            file.write("".join(content))
            tmp_files.append(file.name)
    compileBDIC(USER_DICT_PATH, name, remove=False)
    for f in tmp_files:
        os.remove(f)


def checkConversionBinaries():
    def check(*args):
        if any([not os.path.isfile(os.path.join(BINS_PATH, b)) for b in EXPECTED_BINARIES]):
            missing = [b for b in EXPECTED_BINARIES if not os.path.isfile(os.path.join(BINS_PATH, b))]
            repo = download(BASE_URL_BINARIES).json()
            for m in missing:
                ditem = next(item for item in repo if item['name'] == m)
                downloadToFile(ditem['download_url'], BINS_PATH, m)
    runAsync(check, with_progress=True, progress_label="Spell checker:\nDownloading binaries for .bdic conversion...")


def compileBDIC(path, name, remove=False):
    command = [BIN_PATH, os.path.join(path, name)]
    mode = os.stat(BIN_PATH).st_mode
    mode |= (mode & 0o444) >> 2  # copy R bits to X
    os.chmod(BIN_PATH, mode)
    res = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if res.returncode != 0:
        showWarning(f"Dictionary {name} seems to be broken. Process output: {res.stdout}")
        return -1
    if remove:
        ex = [".dic", ".aff"]
        for e in ex:
            os.remove(os.path.join(path, name + e))
    os.rename(os.path.join(path, name + ".bdic"), os.path.join(DICT_DIR, name + ".bdic"))


def download(url):
    try:
        res = req.get(url)
    except ConnectionError as error:
        showWarning(
            "Internet connection failed. Files could not be downloaded. Please ensure you have an "
            f"internet connection and reopen Anki. Error: {error}")
        return None
    if res.status_code != 200:
        showWarning(f"Access to {url} failed. Status code: {res.status_code}. Please try again later.")
    return res


def openPath(path):
    webbrowser.open(f'file://{path}')


def downloadToFile(url, loc, name):
    res = download(url)
    if res is None:
        return None
    saveMkdir(loc)
    save_path = os.path.join(loc, name)
    saveWrite(save_path, res.content)

    return save_path


def setUserData(name, data):
    path = os.path.join(USER_PATH, name + ".pck")
    try:
        with open(path, "w+b") as f:
            pck = pickle.dumps(data)
            f.write(pck)
    except IOError as err:
        showWarning(f"Could not write user files, check permissions. Error: {err}")


def getUserData(name, default=None):
    if default is None:
        default = []
    path = os.path.join(USER_PATH, name + ".pck")
    if not os.path.isfile(path):
        return default
    try:
        with open(path, "rb") as f:
            pck = f.read()
            return pickle.loads(pck)
    except IOError as err:
        showWarning(f"Could not read user files, check permissions. Error: {err}")
        return default


def saveMkdir(path):
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as error:
        showWarning(f"Can't create data folder, check permissions. Error: {error}")


def saveWrite(path, content, mode="w+b"):
    try:
        with open(path, mode) as f:
            f.write(content)
    except IOError as error:
        showWarning(f"Could not write content to disk. Error: {error}")
