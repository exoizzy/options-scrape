import requests
from datetime import date
import json
from fileUtilities import FileUtility
from bs4 import BeautifulSoup
import models

# interface support values
interfaceName = 'YahooFinanceInterface'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/39.0.2171.95 Safari/537.36'}

url_base = "https://finance.yahoo.com/quote/"
url_options = "/options?"
url_p = "p="
url_date = "date="
url_and = "&"
url_straddle_true = "&straddle=true"

json_start = 'root.App.main ='
start_len = len(json_start)
json_end = ';\n}(this));'

# yfin options json values
call = 'call'
put = 'put'
strike = '.strike'
price = '.lastPrice'
oi = '.openInterest'
iv = '.impliedVolatility'
contTicker = '.contractSymbol'
exp = '.expiration'
vol = '.volume'
bid = '.bid'
ask = '.ask'
raw = 'raw'
fmt = 'fmt'
# yfin json values
meta = 'meta'
expirationDates = 'expirationDates'
quote = 'quote'
regMktTime = 'regularMarketTime'
regMktPrice = 'regularMarketPrice'
yrHigh = 'fiftyTwoWeekHigh'
yrLow = 'fiftyTwoWeekLow'
dayHigh = 'regularMarketDayHigh'
dayLow = 'regularMarketDayLow'
strikes = 'strikes'
contracts = 'contracts'
straddles = 'straddles'


class YahooFinanceInterface:
    fileName = ''
    ticker: str = 'SPY'
    expiryRange = None

    def __init__(self, ticker, expRange=None):
        print(f"Yahoo Finance interface loaded for ticker: {ticker}\n")
        self.ticker = ticker
        self.fileName = f'{interfaceName}_{date.today()}_{self.ticker}'
        self.expiryRange = expRange

    def build_url(self, dateint: int = None):
        return url_base + self.ticker \
               + url_options + ((url_date + str(dateint) + url_and) if dateint is not None else "") \
               + url_p + self.ticker + url_straddle_true

    def get_day_html(self, dateint: int = None):
        url = self.build_url(dateint)
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                # print(f"html for url : {url} has been fetched successfully\n")
                datestr = f'_{dateint}' if dateint is not None else ""
                FileUtility.saveHtmlFile(r.text, interfaceName, f'{self.fileName}{datestr}_rawHtmlScrape')
                return BeautifulSoup(r.text, 'html.parser')
            print(f"Failed to get html for url : {url}\n returned status code: {r.status_code} - {r.text}\n\n")
        except Exception as e:
            print(f"ERROR: failed to get data from {url} with error - {e}\n aborting...\n")
            return None

    def get_options_json_from_html(self, soup: BeautifulSoup, dateint: int = None):
        # print("Grabbing options data from html...\n")
        scripts = soup.find_all(name='script')
        appMain = ''
        for scr in scripts:
            if 'root.App.main' in scr.text:
                appMain = scr.text

        if appMain != '':
            rootind = appMain.find(json_start)
            rootind += start_len
            rootend = appMain.find(json_end)
            # print('Options data found successfully\n')
            jsonstr = appMain[rootind:rootend]
            jsonObj = json.loads(jsonstr)
            try:
                # remove all values not necessary for processing to reduce memory consumption/storage use
                jsonObj = jsonObj['context']['dispatcher']['stores']['OptionContractsStore']
                datestr = f'_{dateint}' if dateint is not None else ""
                FileUtility.saveJsonFile(jsonObj, interfaceName, f'{self.fileName}{datestr}_rawOptionsJson')
                return jsonObj
            except KeyError as ke:
                print(f'KeyError: {ke} while getting options json for {dateint}')
        print('Options data could not be found\n')
        FileUtility.saveHtmlFile(soup.text, interfaceName, f'{self.fileName}_ERROR-OPTIONS-DATA-NOT-FOUND')
        return {}

    def get_options_json(self, dateint=None):
        html = self.get_day_html(dateint)
        if html is not None:
            optConStore = self.get_options_json_from_html(html, dateint)
            return optConStore

    def get_options_from_day(self, contracts) -> []:
        optionsArr = []
        yfinStrad = contracts[straddles]

        for strad in yfinStrad:
            for opt in [call, put]:
                try:
                    strk = strad[opt + strike][raw]
                    pr = strad[opt + price][raw]
                    intr = strad[opt + oi][raw]
                    impl = strad[opt + iv][raw]
                    volu = strad[opt + vol][raw]
                    expir = strad[opt + exp][raw]
                    b = strad[opt + bid][raw] if opt + bid in strad else None
                    a = strad[opt + ask][raw] if opt + bid in strad else None
                    tick = strad[opt + contTicker]
                    option = models.Option(tick, strk, expir, intr, volu, impl, opt[0], self.ticker, pr, b, a)
                    optionsArr.append(option)
                except KeyError as ke:
                    # we dont really need to do anything here, no data available for the contract
                    pass

        return optionsArr

    def get_all_options(self, contracts, expDates) -> []:
        optionsArr = self.get_options_from_day(contracts)

        for dateint in expDates:
            optJson = self.get_options_json(dateint)[contracts]
            optionsArr.extend(self.get_options_from_day(optJson))

        return optionsArr

    def get_stonk(self):
        yhigh, ylow, dhigh, dlow = None, None, None, None

        optConStore: dict = self.get_options_json()

        if optConStore is not None and optConStore != {}:
            yfinQuote = optConStore[meta][quote]
            expDates = optConStore[meta][expirationDates]
            yfinStrikes = optConStore[meta][strikes]

            currentPrice = yfinQuote[regMktPrice]
            lastOpen = yfinQuote[regMktTime]

            try:
                yhigh = yfinQuote[yrHigh]
                ylow = yfinQuote[yrLow]
                dhigh = yfinQuote[dayHigh]
                dlow = yfinQuote[dayLow]
            except KeyError as ke:
                print(f'unable to populate {ke} for {self.ticker}')

            stonk = models.Stonk(self.ticker, currentPrice, lastOpen, yhigh, ylow, dhigh, dlow)
            stonk.expDates = expDates
            stonk.strikes = yfinStrikes
            stonk.options = self.get_all_options(optConStore[contracts], expDates)


