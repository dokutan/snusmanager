export class LocationAmount {
  id: number | undefined;
  amount: number | undefined;
  constructor(id: number, amount: number){
    this.id = id;
    this.amount = amount;
  }
}

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
    locations: LocationAmount[] = [];
    thumbnail_base64: string | null = null;
    thumbnail_mime: string | null = null;
}
