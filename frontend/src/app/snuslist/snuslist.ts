import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatGridListModule } from '@angular/material/grid-list';
import { Backend } from '../../services/backend';

@Component({
  selector: 'app-snuslist',
  imports: [MatCardModule, MatButtonModule, MatGridListModule],
  templateUrl: './snuslist.html',
  styleUrl: './snuslist.css',
})
export class Snuslist {
  snus: any = [];

  constructor(private service: Backend ) { }

  ngOnInit() {
    this.service.getSnus()
      .subscribe(response => {
        this.snus = response;
      });
  }
}
