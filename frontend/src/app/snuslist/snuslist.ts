import { Component, inject } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatGridListModule } from '@angular/material/grid-list';
import { Backend } from '../../services/backend';
import { MAT_DIALOG_DATA, MatDialog, MatDialogModule } from '@angular/material/dialog';

import { AddSnus } from '../add-snus/add-snus';

@Component({
  selector: 'app-snuslist',
  imports: [MatCardModule, MatButtonModule, MatGridListModule],
  templateUrl: './snuslist.html',
  styleUrl: './snuslist.css',
})
export class Snuslist {
  snus: any = [];

  readonly dialog: MatDialog = inject(MatDialog);

  constructor(private service: Backend ) { }

  ngOnInit() {
    this.service.getSnus()
      .subscribe(response => {
        this.snus = response;
      });
  }

  editSnus(id: number) {
    this.dialog.open(AddSnus, {data: {action: "edit", id: id}})
  }
}
