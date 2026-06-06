from urllib.parse import urlparse
import urllib.request
import re
import magic
from extruct import extract

from snus import Snus


def urlopen(url):
    "Custom urlopen with different default user agent."
    req = urllib.request.Request(url, headers={"User-Agent": ""})
    return urllib.request.urlopen(req)


def get_json_ld_product(content: str) -> Snus:
    "Get the basic information about a snus from embedded schema.org json-ld product data."
    data = extract(content)
    snus = Snus()

    for product in data.get("json-ld", []):
        if product.get("@type") == "Product" and not isinstance(product, list):
            snus.name = product.get("name", "")
            snus.description = product.get("description", "")
            if "brand" in product.keys() and "name" in product["brand"].keys():
                snus.brand = product["brand"]["name"]
            image_url = product.get("image", None)
            if isinstance(image_url, str):
                snus.image = urlopen(image_url).read()
                snus.image_mime = magic.from_buffer(snus.image, mime=True)
            break

    return snus



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
    if m := re.search(r'<source +content="[^"]*" +type="image/webp" +srcset="([^"]+.webp)">', content):
        image_url = m.group(1)
        snus.image = urlopen(image_url).read()
        snus.image_mime = "image/webp"
    return snus


def swedishmatch_se(content: str) -> Snus:
    snus = get_json_ld_product(content)
    if m := re.search(r'Nettovikt/dosa</td><td[^>]*>([0-9.,]+) *g', content):
        snus.weight_g = float(m.group(1).replace(",", "."))
    if m := re.search(r'Antal prillor/dosa</td><td[^>]*>([0-9]+) *st', content):
        snus.portions = int(m.group(1))
    return snus


def skruf_se(content: str) -> Snus:
    snus = Snus()
    if m := re.search(r'<title>([^<]+)-', content):
        snus.name = m.group(1).strip()
    if m := re.search(r'Nikotinhalt mg/g:</span><strong class="fact-item__value">([0-9.,]+) +mg/g', content):
        snus.nicotine_g = float(m.group(1).replace(",", "."))
    if m := re.search(r'Nikotinhalt / påse:</span><strong class="fact-item__value">([0-9.,]+) +mg/portion', content):
        snus.nicotine_portion = float(m.group(1).replace(",", "."))
    if m := re.search(r'Vikt dosa:</span><strong class="fact-item__value">([0-9.,]+) +g', content):
        snus.weight_g = float(m.group(1).replace(",", "."))
    if m := re.search(r'<strong class="fact-item__value">([0-9]+) +st', content):
        snus.portions = int(m.group(1))
    if m := re.search(r'Vikt prilla:</span><strong class="fact-item__value">([0-9.,]+) +g', content):
        snus.portion_g = float(m.group(1).replace(",", "."))
    if m := re.search(r'<h1 class="product-article__title">([^<]+)<br>', content):
        snus.brand = m.group(1).strip()
    if m := re.search(r'src="([^"]+.webp)" class="product-article__video-image"', content):
        image_url = m.group(1)
        snus.image = urlopen(image_url).read()
        snus.image_mime = "image/webp"
    return snus


scrapers = {
    "www.mysnus.com": mysnus_com,
    "snushus.ch": snushus_ch,
    "www.snusport.com": snusport_com,
    "www.buysnus.com": buysnus_com,
    "www.swedishmatch.se": swedishmatch_se,
    "skruf.se": skruf_se,
}


def import_snus(url: str) -> Snus:
    o = urlparse(url)
    if o.hostname in scrapers.keys():
        content = urlopen(url).read().decode("utf-8")
        return scrapers[o.hostname](content)
    else:
        raise "Unsupported URL"
