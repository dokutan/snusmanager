import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Snus } from '../snus';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class Backend {
  private httpClient = inject(HttpClient);

  private readonly url = environment.apiUrl;
  
  getLocations(){
    return this.httpClient.get(this.url + "locations");
  }

  addLocation(location: string){
    return this.httpClient.post(this.url + "locations/" + location, "").subscribe(_response => { });
  }

  deleteLocation(id: number){
    return this.httpClient.delete(this.url + "locations/" + id);
  }

  getSnus(){
    return this.httpClient.get(this.url + "snus");
  }

  getSnusById(id: number){
    return this.httpClient.get(this.url + "snus/" + id);
  }

  getSnusTypes(){
    return this.httpClient.get(this.url + "snustypes");
  }

  addSnus(snus: Snus){
    //this.httpClient.post(this.url + "snus/from_url", {"url": url});
    this.httpClient.post(this.url + "snus", snus).subscribe(response => {
      // console.log(response);
    });
  }

  updateSnus(id: number, snus: Snus){
    this.httpClient.patch(this.url + "snus/" + id, snus).subscribe(_response => { });
  }

  importSnus(url: string){
    console.log("import: " + url);
    //this.httpClient.post(this.url + "snus/from_url", {"url": url});
    this.httpClient.post(this.url + "snus/from_url", {"url": url}).subscribe(response => {
      console.log(response);
    });
  }

  deleteSnus(id: number){
    this.httpClient.delete(this.url + "snus/" + id).subscribe(_response => { });
  }

  cropImages(){
    this.httpClient.post(this.url + "crop_images", null).subscribe(_response => { });
  }

  calculateMissing(){
    this.httpClient.post(this.url + "calculate_missing", null).subscribe(_response => { });
  }
}
