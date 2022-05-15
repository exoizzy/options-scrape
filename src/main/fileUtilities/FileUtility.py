import src.res
import json
import os
from datetime import date
from models.Stonk import StonkEncoder

resFP = os.path.dirname(src.res.__file__)
resdir = os.listdir(resFP)
html = 'html-files'
interJson = 'interface-json-files'
localJson = 'local-json-files'
temp = 'temp'


def saveJsonFile(pysonObj, interfaceName, filename) -> bool:
    opentype = 'w'
    filepath = os.path.join(resFP, interJson)
    filepath = os.path.join(filepath, interfaceName)

    try:
        # make sure that the dir structure exists
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        filepath = os.path.join(filepath, f'{filename}.json')
        # opentype 'w' already clears the file when it is opened.
        with open(filepath, opentype) as f:
            json.dump(pysonObj, f)
            f.close()
        return True
    except Exception as e:
        print(f'unable to create or write to JSON FILE {filepath}, error: {e}')
    return False


def readJsonFile(interface, filename) -> json:
    filepath = f'{resFP}{interJson}{interface}/{filename}.json'
    try:
        with open(filepath, 'r') as f:
            pyson = json.load(f)
            f.close()
            return pyson
    except Exception as e:
        print(f'unable to read json from {filepath}, error: {e}')


def saveHtmlFile(htmlObj, interfaceName, filename) -> bool:
    opentype = 'w'
    filepath = os.path.join(resFP, html)
    filepath = os.path.join(filepath, interfaceName)

    try:
        # make sure that the dir structure exists
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        filepath = os.path.join(filepath, f'{filename}.html')
        # opentype 'w' already clears the file when it is opened.
        with open(filepath, opentype) as f:
            json.dump(htmlObj, f)
            f.close()
        return True
    except Exception as e:
        print(f'unable to create or write to HTML FILE {filepath}, error: {e}')
    return False


def saveStonkToJsonFile(stonk, filename) -> bool:
    opentype = 'w'
    filepath = os.path.join(resFP, localJson)
    filepath = os.path.join(filepath, stonk.ticker)

    try:
        # make sure that the dir structure exists
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        filepath = os.path.join(filepath, f'{stonk.ticker}_{date.today()}_{filename}_stonk.json')
        # opentype 'w' already clears the file when it is opened.
        with open(filepath, opentype) as f:
            json.dump(stonk, f, indent=4, cls=StonkEncoder)
            f.close()
        return True
    except Exception as e:
        print(f'unable to create or write to HTML FILE {filepath}, error: {e}')
    return False
