from bs4 import BeautifulSoup as bs
from re import search
from requests import Session
from typing import Union
from poi import PoiInfo
from utils import Texto
import certifi
import time

class Hent(Session):

    def __init__(self, url: Union[str], proxy: Union[dict]={}, delay: int=5) -> None:
        """
        Scrap Hentai from nekopoi.care
        :url: String
        :proxy: Dict
        :e.g:
        from nekopoi import Hent
        hentai = Hent("https://nekopoi.care/torokase-orgasm-the-animation-episode-1-subtitle-indonesia/").getto
        hentai.to_json
        """
        super().__init__()
        if proxy:
            self.proxies = proxy
        self.url = url
        self.text = Texto()
        self.delay = delay
        self.verify = False
        self.verify = certifi.where()
        self.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    @property
    def getto(self) -> PoiInfo:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.get(self.url)
                time.sleep(self.delay)
                parse = bs(self.get(self.url).text, "html.parser")
                print(f"Status Code: {response.status_code}")
                print(f"Content: {response.text[:500]}...")
                poi = PoiInfo()
                info = parse.find("div", {"class": "contentpost"})
                if info is None:
                    print("Tidak dapat menemukan div dengan class 'contentpost'")
                    return Exception("Struktur HTML telah berubah")
                oppai = info.select("p[class=\"separator\"]")
                poi.title = self.text.tsplit(info.img.get("title"))
                poi.thumbnail = info.img.get("srcset").split()[-2]
                poi.synopsis = oppai[0].b.next.next.next.text.strip()
                poi.genre = [g.strip() for g in oppai[1].b.next_sibling.split(",")]
                poi.producers = oppai[3].b.next_sibling.lstrip(": ")
                poi.duration = oppai[4].b.next_sibling
                if (vidbin := search("https://videobin.co/.+?.html", parse.prettify())):
                    if (res := search("https://.+?/.+?.mp4", self.get(vidbin.group()).text)):
                        poi.stream = res.group().split("\"")[-1]
                poi.download = {}
                for x in parse.select("div[class=\"liner\"]"):
                    poi.download[self.text.reso(x.div.text)] = {}
                    for y in x.select("a"):
                        poi.download[self.text.reso(x.div.text)].update({y.text.lower(): y.get("href")})
                return poi
            except ConnectionError as e:
                if attempt < max_retries - 1:
                    print(f"Connection error, retrying... (Attempt {attempt + 1})")
                    time.sleep(5)  # tunggu 5 detik sebelum mencoba lagi
                else:
                    print(f"Error detail: {e}")
                    return Exception(f"Connection error after {max_retries} attempts: {e}")
            except Exception as e:
                print(e)
                return Exception("Maybe url invalid")

class Jav(Session):

    def __init__(self, url: Union[str], proxy: Union[dict]={}) -> None:
        """
        Scrap Jav from nekopoi.care
        :url: String
        :Proxy: Dict
        :e.g:
        from nekopoi import Jav
        jav = Jav("https://nekopoi.care/ipx-700-jav-miu-shiramine-a-super-luxury-mens-beauty-treatment-salon-that-makes-beautiful-legs-glamorous-testicles/").getto
        jav.to_json
        """
        super().__init__()
        if proxy:
            self.proxies = proxy
        self.url = url
        self.text = Texto()

    @property
    def getto(self) -> PoiInfo:
        try:
            parse = bs(self.get(self.url).text, "html.parser")
            jav = PoiInfo()
            info = parse.find("div", {"class": "contentpost"})
            oppai = info.select("p")
            jav.title = self.text.tsplit(info.img.get("title"))
            jav.thumbnail = info.img.get("srcset").split()[-2]
            jav.movie_id = oppai[0 if len(oppai) == 6 else 1].text.split(":")[1].strip()
            jav.producers = oppai[1 if len(oppai) == 6 else 2].text.split(":")[1].strip()
            jav.artist = oppai[2 if len(oppai) == 6 else 3].text.split(":")[1].strip()
            genres = oppai[3].text.split(":")[1].strip().split(",") if len(oppai) == 6 else oppai[4].text.split(":")[1].strip(".").split(",")
            jav.genre = [g.strip() for g in genres]
            jav.duration = oppai[4 if len(oppai) == 6 else 5].text.split(":")[1].strip()
            if (vidbin := search("https://videobin.co/.+?.html", parse.prettify())):
                if (res := search("https://.+?/.+?.mp4", self.get(vidbin.group()).text)):
                    jav.stream = res.group().split("\"")[-1]
            jav.download = {}
            for x in parse.select("div[class=\"liner\"]"):
                jav.download[self.text.reso(x.div.text)] = {}
                for y in x.select("a"):
                    jav.download[self.text.reso(x.div.text)].update({y.text.lower(): y.get("href")})
            return jav
        except Exception as e:
            print(e)
            return Exception("Maybe url invalid")

class ThreeD(Session):

    def __init__(self, url: Union[str], proxy: Union[dict]={}) -> None:
        """
        Scrap 3D hentai from nekopoi.care
        :url: String
        :proxy: Dict
        :e.g:
        from nekopoi import ThreeD
        tridi = ThreeD("https://nekopoi.care/3d-hentai-hige-wo-soru-fucked-sayu-ogiwara/").getto
        tridi.to_json
        """
        super().__init__()
        if proxy:
            self.proxies = proxy
        self.url = url
        self.text = Texto()

    @property
    def getto(self) -> PoiInfo:
        try:
            parse = bs(self.get(self.url).text, "html.parser")
            tridi = PoiInfo()
            info = parse.find("div", {"class": "contentpost"})
            oppai = info.select("p")
            tridi.title = self.text.tsplit(info.img.get("title"))
            tridi.thumbnail = info.img.get("srcset").split()[-2]
            tridi.duration = oppai[-2].text.split(":")[1].strip()
            tridi.genre = [g.strip() for g in oppai[-3].text.split(":")[1].strip(".").split(",")]
            if (vidbin := search("https://videobin.co/.+?.html", parse.prettify())):
                if (res := search("https://.+?/.+?.mp4", self.get(vidbin.group()).text)):
                    tridi.stream = res.group().split("\"")[-1]
            tridi.download = {}
            for x in parse.select("div[class=\"liner\"]"):
                tridi.download[self.text.reso(x.div.text)] = {}
                for y in x.select("a"):
                    tridi.download[self.text.reso(x.div.text)].update({y.text.lower(): y.get("href")})
            return tridi
        except Exception as e:
            print(e)
            return Exception("Maybe url invalid")
        
