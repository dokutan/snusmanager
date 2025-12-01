export class Snus {
    id: number | null = null;
    name = "";
    description = "";
    rating: number | string | null = null ;
    nicotine_g: number | null = null;
    nicotine_portion: number | null = null;
    portion_g: number | null = null;
    weight_g: number | null = null;
    portions: number | null = null;
    type = "";
    brand: string | null = null;
    locations: Map<number | string, number | string> = new Map<number | string, number | string>();
    thumbnail_base64: string | null = null;
    thumbnail_mime: string | null = null;
}
