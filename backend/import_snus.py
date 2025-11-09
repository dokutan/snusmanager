from dataclasses import dataclass
from urllib.parse import urlparse
from urllib.request import urlopen
import re

@dataclass
class Snus:
    name: str = ""
    description: str = ""
    rating: int | None = None
    nicotine_g: float | None = None
    nicotine_portion: float | None = None
    portion_g: float | None = None
    snustype: str = "other"
    image: bytes | None = None


def mysnus_com(content: str) -> Snus:
    snus = Snus()
    if m := re.search(r'<span class="base" data-ui-id="page-title-wrapper" itemprop="name">([^<]+)</span></h1>', content):
        snus.name = m.group(1).strip()
    if m := re.search(r'<span class="ingredient-value">([0-9.]+) mg/Port</span>', content):
        snus.nicotine_portion = float(m.group(1))
    if m := re.search(r'<span class="ingredient-value">([0-9.]+) mg/g</span>', content):
        snus.nicotine_g = float(m.group(1))
    if m := re.search(r'"full":"(https:\\/\\/www.mysnus.com\\/media\\/mf_webp\\/png\\/media\\/catalog\\/product\\/cache\\/[^"]+\\/[^/"]+)"', content):
        image_url = m.group(1).replace("\\/", "/")
        snus.image = urlopen(image_url).read()
    return snus


scrapers = {
    "www.mysnus.com": mysnus_com
}


def import_snus(url: str) -> Snus:
    o = urlparse(url)
    if o.hostname in scrapers.keys():
        content = urlopen(url).read().decode("utf-8")
        return scrapers[o.hostname](content)
    else:
        raise "Unsupported URL"
