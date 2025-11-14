import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import {
  MAT_DIALOG_DATA,
  MatDialogActions,
  MatDialogClose,
  MatDialogContent,
  MatDialogModule,
  MatDialogTitle,
} from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { Backend } from '../../services/backend';
import { Snus } from '../../snus';

@Component({
  selector: 'app-edit-snus',
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
  templateUrl: './edit-snus.html',
  styleUrl: './edit-snus.css'
})
//@Injectable({ providedIn: 'any' })
export class EditSnus implements OnInit {
  private service = inject(Backend);
  data = inject<{
    action: "add" | "edit";
    id: number | null;
}>(MAT_DIALOG_DATA);

  locations: any = [];
  snustypes: any = [];
  snus: Snus = new Snus();

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
          console.log(this.snus)
        });
    }
  }

  onDelete(id: number | null) {
    if(id) {
      this.service.deleteSnus(id);
    }
  }

  onSubmit() {
    switch (this.data.action) {
      case "add":
          this.service.addSnus(this.snus);
        break;
      case "edit":
          if(this.snus.id) this.service.updateSnus(this.snus.id, this.snus);
        break;
      default:
        break;
    }
  }
}
