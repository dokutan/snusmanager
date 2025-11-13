import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Snus } from '../snus';

@Injectable({
  providedIn: 'root'
})
export class Backend {
  private url = 'http://127.0.0.1:5000/api/';
   
  constructor(private httpClient: HttpClient) { }
  
  getLocations(){
    return this.httpClient.get(this.url + "locations");
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
      console.log(response);
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
}
