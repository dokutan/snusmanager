import { Dialog } from '@angular/cdk/dialog';
import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, Inject, inject, model, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import {
  MAT_DIALOG_DATA,
  MatDialog,
  MatDialogActions,
  MatDialogClose,
  MatDialogContent,
  MatDialogModule,
  MatDialogRef,
  MatDialogTitle,
} from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { Injectable } from "@angular/core";
import { Backend } from '../../services/backend';
import { Snus } from '../../snus';

@Component({
  selector: 'app-add-snus',
  standalone: true,
  imports: [
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    MatButtonModule,
    MatDialogTitle,
    MatDialogContent,
    MatDialogActions,
    MatDialogClose,
    MatSelectModule,
    CommonModule,
    MatDialogModule
  ],
  templateUrl: './add-snus.html',
  styleUrl: './add-snus.css'
})
//@Injectable({ providedIn: 'any' })
export class AddSnus {
  locations: any = [];
  snustypes: any = [];
  snus: Snus = new Snus();

  constructor(private service: Backend, @Inject(MAT_DIALOG_DATA) public data: {action: "add"|"edit", id: number|null}) { }

  ngOnInit() {
    this.service.getLocations()
      .subscribe(response => {
        this.locations = response;
      });
    this.service.getSnusTypes()
      .subscribe(response => {
        this.snustypes = response;
      });

    if(this.data.action == "edit" && this.data.id) {
      this.service.getSnusById(this.data.id)
        .subscribe(response => {
          this.snus = response as Snus;
        });
    }
  }

  onDelete(id: number | null) {
    if(id) {
      this.service.deleteSnus(id);
    }
  }

  onSubmit() {
    this.service.addSnus(this.snus);
  }
}
