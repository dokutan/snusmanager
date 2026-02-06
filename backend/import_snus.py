from urllib.parse import urlparse
from urllib.request import urlopen
import re

from snus import Snus

def mysnus_com(content: str) -> Snus:
    snus = Snus()
    if m := re.search(r'<span class="base" data-ui-id="page-title-wrapper" itemprop="name">([^<]+)</span></h1>', content):
        snus.name = m.group(1).strip()
    if m := re.search(r'<span class="ingredient-value">([0-9.]+) mg/Port</span>', content):
        snus.nicotine_portion = float(m.group(1))
    if m := re.search(r'<span class="ingredient-value">([0-9.]+) mg/g</span>', content):
        snus.nicotine_g = float(m.group(1))
    if m := re.search(r'Nicotine Weight</strong></span> *<span class="ingredient-value">([0-9.]+) g</span>', content):
        snus.weight_g = float(m.group(1))
    if m := re.search(r'Portions</strong></span> *<span class="ingredient-value">([0-9]+)</span>', content):
        snus.portions = int(m.group(1))
    if m := re.search(r'Brand</strong></span> *<span class="ingredient-value"><a href="[^"]*" target="[^"]*">([^<]+)</a></span>', content):
        snus.brand = m.group(1).strip()
    if m := re.search(r'"full":"(https:\\/\\/www.mysnus.com\\/media\\/mf_webp\\/png\\/media\\/catalog\\/product\\/cache\\/[^"]+\\/[^/"]+)"', content):
        image_url = m.group(1).replace("\\/", "/")
        snus.image = urlopen(image_url).read()
        snus.image_mime = "image/webp"
    return snus


def snushus_ch(content: str) -> Snus:
    snus = Snus()
    property_regex = r'''<td[^>]*><strong>([0-9.]+) mg/g</strong></td>
</tr><tr>
<td[^>]*>[^<]+</td>
<td[^>]*><strong>([0-9.]+) g</strong></td>
</tr>
<tr>
<td[^>]*>[^<]+</td>
<td[^>]*><b>[^<]+</b></td>
</tr><tr>
<td[^>]*>[^<]+</td>
<td[^>]*><b>([0-9]+)</b></td>'''
    if m := re.search('"@type": "Product",\n *"name": "([^"]+)",', content):
        snus.name = m.group(1).strip()
    if m := re.search(property_regex, content):
        snus.nicotine_g = float(m.group(1))
        snus.weight_g = float(m.group(2))
        snus.portions = int(m.group(3))
    if m := re.search('"image": \\[\n *"(https://snushus.ch/cdn/shop/files/[^"]+.png[^"]+)"', content):
        image_url = m.group(1)
        snus.image = urlopen(image_url).read()
        snus.image_mime = "image/png"
    return snus


def snusport_com(content: str) -> Snus:
    snus = Snus()
    if m := re.search(r'<h1 class="product_title entry-title">([^<]+)</h1>', content):
        snus.name = m.group(1).strip()
    if m := re.search(r'Nicotine Level: ([0-9.,]+) mg/g .([0-9.,]+) mg per pouch.<br />', content):
        snus.nicotine_g = float(m.group(1).replace(",", "."))
        snus.nicotine_portion = float(m.group(2).replace(",", "."))
    if m := re.search(r'Weight: ([0-9.,]+) grams<br />', content):
        snus.weight_g = float(m.group(1).replace(",", "."))
    if m := re.search(r'Number of pouches: ([0-9]+)<br />', content):
        snus.portions = int(m.group(1))
    if m := re.search(r'Pouch Weight: ([0-9.,]+) g<br />', content):
        snus.portion_g = float(m.group(1).replace(",", "."))
    if m := re.search('<meta property="og:image" content="(https://www.snusport.com/wp-content/uploads/[^"]+.png)" />', content):
        image_url = m.group(1)
        snus.image = urlopen(image_url).read()
        snus.image_mime = "image/png"
    return snus


def buysnus_com(content: str) -> Snus:
    snus = Snus()
    if m := re.search(r'<span class="base" data-ui-id="page-title-wrapper" itemprop="name">([^<]+)</span>', content):
        snus.name = m.group(1).strip()
    if m := re.search(r'<h3 class="porto-sicon-title">Nicotine Content</h3><p>([0-9.]+) mg/g</p>', content):
        snus.nicotine_g = float(m.group(1))
    if m := re.search(r'<span class="ingredient-value">([0-9.]+) mg/Port</span>', content):
        snus.nicotine_portion = float(m.group(1))
    if m := re.search(r'<h3 class="porto-sicon-title">Nicotine Weight</h3><p>([0-9.]+) g</p>', content):
        snus.weight_g = float(m.group(1))
    if m := re.search(r'<strong>Portions</strong></span> <span class="ingredient-value">([0-9]+)</span>', content):
        snus.portions = int(m.group(1))
    if m := re.search(r'<h2 class="product-title" itemprop="brand">([^<]+)</h2>', content):
        snus.brand = m.group(1).strip()
    if m := re.search(r'<source +itemprop="image" content="[^"]*" +type="image/webp" +srcset="([^"]+.webp)">', content):
        image_url = m.group(1)
        snus.image = urlopen(image_url).read()
        snus.image_mime = "image/webp"
    return snus


scrapers = {
    "www.mysnus.com": mysnus_com,
    "snushus.ch": snushus_ch,
    "www.snusport.com": snusport_com,
    "www.buysnus.com": buysnus_com
}


def import_snus(url: str) -> Snus:
    o = urlparse(url)
    if o.hostname in scrapers.keys():
        content = urlopen(url).read().decode("utf-8")
        return scrapers[o.hostname](content)
    else:
        raise "Unsupported URL"
