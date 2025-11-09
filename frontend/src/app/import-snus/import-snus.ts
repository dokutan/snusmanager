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
    MatDialogModule,
  ],
  templateUrl: './import-snus.html',
  styleUrl: './import-snus.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
//@Injectable({ providedIn: 'any' })
export class ImportSnus {
  url: string = "";

  constructor(private service: Backend){ }

  onSubmit() {
    console.log("ok " + this.url);
    this.service.importSnus(this.url)
  }
}
