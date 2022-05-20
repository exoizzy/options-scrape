import src.res
import json
import os
from datetime import date
from models.Stonk import StonkEncoder
from models.Stonk import Stonk
from types import SimpleNamespace

resFP = os.path.dirname(src.res.__file__)
resdir = os.listdir(resFP)
html = 'html-files'
interJson = 'interface-json-files'
localJson = 'local-json-files'
temp = 'temp'


def saveJsonFile(pysonObj, interfaceName, filename) -> str:
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
        return f'{filename}.json'
    except Exception as e:
        print(f'unable to create or write to JSON FILE {filepath}, error: {e}')
    return ''


def readJsonFile(interface, filename) -> json:
    filepath = f'{resFP}{interJson}{interface}/{filename}.json'
    try:
        with open(filepath, 'r') as f:
            pyson = json.load(f)
            f.close()
            return pyson
    except Exception as e:
        print(f'unable to read json from {filepath}, error: {e}')


def saveHtmlFile(htmlObj, interfaceName, filename) -> str:
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
        return f'{filename}.html'
    except Exception as e:
        print(f'unable to create or write to HTML FILE {filepath}, error: {e}')
    return ''


def saveStonkToJsonFile(stonk, filename) -> str:
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
        return f'{stonk.ticker}_{date.today()}_{filename}_stonk.json'
    except Exception as e:
        print(f'unable to create or write to HTML FILE {filepath}, error: {e}')
    return ''


def importStonkFromJsonFile(ticker, filename):
    opentype = 'r'
    fp = os.path.join(resFP, localJson)
    fp = os.path.join(fp, ticker)
    fp = os.path.join(fp, filename)

    try:
        if os.path.exists(fp):
            with open(fp, opentype) as f:
                stonk = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
                f.close()
            return stonk
        else:
            raise Exception(f'file does not exists in path: {fp}')
    except Exception as e:
        print(f'unable to read stonk from file {filename}.json with error: {e}')
