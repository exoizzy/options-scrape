import requests
from datetime import date
import json
from fileUtilities import FileUtility
from bs4 import BeautifulSoup
import models


class YahooFinanceInterface:
    interfaceName = 'YahooFinanceInterface'
    fileName = ''
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

    ticker: str = 'SPY'

    # yfin json values
    strike = '.strike'
    price = '.lastPrice'
    oi = '.openInterest'
    iv = '.impliedVolatility'
    contTicker = '.contractSymbol'
    exp = '.expiration'
    vol = '.volume'
    raw = 'raw'
    fmt = 'fmt'

    def __init__(self, ticker):
        self.interfaceName = self.__class__.__name__
        print(f"Yahoo Finance interface loaded for ticker: {ticker}\n")
        self.ticker = ticker
        self.fileName = f'{self.interfaceName}_{date.today()}_{self.ticker}'

    def build_url(self, dateint: int = None):
        return self.url_base + self.ticker \
               + self.url_options + ((self.url_date + str(dateint) + self.url_and) if dateint is not None else "") \
               + self.url_p + self.ticker + self.url_straddle_true

    def get_day_html(self, dateint: int = None):
        url = self.build_url(dateint)
        try:
            r = requests.get(url, headers=self.headers)
            if r.status_code == 200:
                # print(f"html for url : {url} has been fetched successfully\n")
                datestr = f'_{dateint}' if dateint is not None else ""
                FileUtility.saveHtmlFile(r.text, self.interfaceName, f'{self.fileName}{datestr}_rawHtmlScrape')
                return BeautifulSoup(r.text, 'html.parser')
            print(f"Failed to get html for url : {url}\n returned status code: {r.status_code} - {r.text}\n\n")
        except Exception as e:
            print(f"ERROR: failed to get data from {url} with error - {e}\n aborting...\n")
            return None

    def get_options_json_from_html(self, soup: BeautifulSoup, dateint: int = None):
        print("Grabbing options data from html...\n")
        scripts = soup.find_all(name='script')
        appMain = ''
        for scr in scripts:
            if 'root.App.main' in scr.text:
                appMain = scr.text

        if appMain != '':
            rootind = appMain.find(self.json_start)
            rootind += self.start_len
            rootend = appMain.find(self.json_end)
            print('Options data found successfully\n')
            jsonstr = appMain[rootind:rootend]
            jsonObj = json.loads(jsonstr)
            # remove all values not necessary for processing to reduce memory consumption/storage use
            jsonObj = jsonObj['context']['dispatcher']['stores']['OptionContractsStore']
            datestr = f'_{dateint}' if dateint is not None else ""
            FileUtility.saveJsonFile(jsonObj, self.interfaceName, f'{self.fileName}{datestr}_rawOptionsJson')
            return jsonObj
        print('Options data could not be found\n')
        FileUtility.saveHtmlFile(soup.text, self.interfaceName, f'{self.fileName}_ERROR-OPTIONS-DATA-NOT-FOUND')
        return appMain

    def get_future_dates(self, optionsStorePyson) -> []:
        return optionsStorePyson['meta']['expirationDates']

    def map_toStraddleArray(self, optionsStorePyson: json):
        ce = 0
        pe = 0
        contracts = optionsStorePyson['contracts']
        straddles = contracts['straddles']
        lStraddles = []

        for strad in straddles:
            callerrFlag = False
            call = None
            callexp = None
            try:
                callstrike = strad[f'call{self.strike}'][self.raw]
                callprice = strad[f'call{self.price}'][self.raw]
                calloi = strad[f'call{self.oi}'][self.raw]
                calliv = strad[f'call{self.iv}'][self.raw]
                callvol = strad[f'call{self.vol}'][self.raw]
                callticker = strad[f'call{self.contTicker}']
                cdate = strad[f'call{self.exp}'][self.fmt]
                copdt = models.OptDate(int(cdate[:4]), int(cdate[5:7]), int(cdate[8:]))
                callexp = strad[f'call{self.exp}'][self.raw]
                call = models.Option(callticker, self.ticker, callexp, 'c', callstrike, callvol, calloi, calliv,
                                     callprice, copdt)
            except KeyError as ke:
                ce = ce + 1
                callerrFlag = True

            put = None
            try:
                putstrike = strad[f'put{self.strike}'][self.raw]
                putprice = strad[f'put{self.price}'][self.raw]
                putoi = strad[f'put{self.oi}'][self.raw]
                putiv = strad[f'put{self.iv}'][self.raw]
                putticker = strad[f'put{self.contTicker}']
                putvol = strad[f'put{self.vol}'][self.raw]
                pdate = strad[f'put{self.exp}'][self.fmt]
                popdt = models.OptDate(int(pdate[:4]), int(pdate[5:7]), int(pdate[8:]))
                putexp = strad[f'put{self.exp}'][self.raw]
                put = models.Option(putticker, self.ticker, putexp, 'p', putstrike, putvol, putoi, putiv, putprice,
                                    popdt)
                if callerrFlag:
                    call = models.Option(None, self.ticker, putexp, 'c', putstrike, 0, 0, 0, 0, popdt)
            except KeyError as ke:
                pe = pe + 1
                if not callerrFlag:
                    put = models.Option(None, self.ticker, callexp, 'p', callstrike, 0, 0, 0, 0, copdt)

            if not callerrFlag and put is not None:
                lStraddle = models.Straddle(strad['strike'][self.raw], callexp, call, put)
                lStraddles.append(lStraddle)

        print(f'call errors: {ce}, put errors: {pe}')
        return lStraddles

    def get_all_options_available(self, pyson, expDates):
        # assumes pyson contains the first available days options data (default yfin url)
        # maybe want to datesarr.sort() here? idk i feel like that might cause issues but idfk
        d0straddles = self.map_toStraddleArray(pyson)
        allStraddles = [models.DaysOptions(expDates[0], d0straddles)]

        # TODO: comment this out to get only todays options data, uncomment for all available data
        for dateint in expDates[1:]:
            html = self.get_day_html(dateint)
            if html is not None:
                pyson = self.get_options_json_from_html(html, dateint)
                straddles = self.map_toStraddleArray(pyson)
                allStraddles.append(models.DaysOptions(dateint, straddles))

        return allStraddles

    def get_stonk(self):
        html = self.get_day_html()
        if html is not None:
            pyson: dict = self.get_options_json_from_html(html)
            quote = pyson['meta']['quote']
            currentPrice = quote['regularMarketPrice']
            lastopen = quote['regularMarketTime']
            expDates: [int] = self.get_future_dates(pyson)
            options = self.get_all_options_available(pyson, expDates)
            stonk = models.Stonk(self.ticker, currentPrice, options, expDates, lastopen)

            return stonk

        return None
