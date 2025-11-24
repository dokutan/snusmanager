from dataclasses import dataclass

@dataclass
class Snus:
    name: str = ""
    description: str = ""
    rating: int | None = None
    nicotine_g: float | None = None
    nicotine_portion: float | None = None
    portion_g: float | None = None
    weight_g: float | None = None
    portions: int | None = None
    snustype: str = "other"
    brand: str | None = None
    image: bytes | None = None
    image_mime: str | None = None
