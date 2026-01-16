import { Component, inject, OnInit } from '@angular/core';
import { MatButtonModule, MatIconButton } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatGridListModule } from '@angular/material/grid-list';
import { Backend } from '../../services/backend';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';

import { ImportSnus } from '../import-snus/import-snus';
import { EditSnus } from '../edit-snus/edit-snus';
import { MatFormField, MatFormFieldModule, MatLabel } from "@angular/material/form-field";
import { MatSelect, MatOption, MatSelectModule } from "@angular/material/select";
import { MatIcon, MatIconModule } from "@angular/material/icon";
import { TitleCasePipe } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { RouterLink } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';

@Component({
  selector: 'app-snuslist',
  imports: [MatCardModule, MatButtonModule, MatGridListModule, MatFormField, MatLabel, MatSelect, MatOption, MatIcon, TitleCasePipe, FormsModule, MatToolbarModule, MatIconModule, MatIconButton, MatSelectModule, ReactiveFormsModule, FormsModule, MatFormFieldModule, MatInputModule, TitleCasePipe, MatDialogModule, RouterLink],
  templateUrl: './snuslist.html',
  styleUrl: './snuslist.css',
})
export class Snuslist implements OnInit {
  private service = inject(Backend);

  snus: any = [];
  locations: any = [];
  snustypes: any = [];
  searchText: any;
  searchType: any;
  searchRating: any;

  readonly dialog: MatDialog = inject(MatDialog);

  ngOnInit() {
    this.service.getSnus()
      .subscribe(response => {
        this.snus = response;
        this.snus.sort((a: any, b: any) => a.name.localeCompare(b.name))
      });
    this.service.getLocations()
      .subscribe(response => {
        this.locations = response;
      });
    this.service.getSnusTypes()
      .subscribe(response => {
        this.snustypes = response;
      });
  }

  editSnus(id: number) {
    this.dialog.open(EditSnus, { data: { action: "edit", id: id } }).afterClosed().subscribe(() => {
      this.ngOnInit()
    })
  }

  addSnus() {
    this.dialog.open(EditSnus, { data: { action: "add" } }).afterClosed().subscribe(() => {
      window.location.reload()
    })
  }

  importSnus() {
    this.dialog.open(ImportSnus).afterClosed().subscribe(() => {
      window.location.reload()
    })
  }
}
