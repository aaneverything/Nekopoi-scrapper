from neko import Hent

url = "https://nekopoi.care/shion-episode-2-subtitle-indonesia/"

hentai = Hent(url,  proxy={"http": "http://host:port"}).getto

if isinstance(hentai, Exception):
    print(f"Terjadi kesalahan: {hentai}")
else:
    print(hentai.title)  # Untuk melihat judul
    print(hentai.to_json)  # Untuk mendapatkan semua informasi dalam format JSON