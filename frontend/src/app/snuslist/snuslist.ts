import { Component, inject, OnInit } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatGridListModule } from '@angular/material/grid-list';
import { Backend } from '../../services/backend';
import { MatDialog } from '@angular/material/dialog';

import { EditSnus } from '../edit-snus/edit-snus';

@Component({
  selector: 'app-snuslist',
  imports: [MatCardModule, MatButtonModule, MatGridListModule],
  templateUrl: './snuslist.html',
  styleUrl: './snuslist.css',
})
export class Snuslist implements OnInit {
  private service = inject(Backend);

  snus: any = [];

  readonly dialog: MatDialog = inject(MatDialog);

  ngOnInit() {
    this.service.getSnus()
      .subscribe(response => {
        this.snus = response;
      });
  }

  editSnus(id: number) {
    this.dialog.open(EditSnus, {data: {action: "edit", id: id}})
  }
}
