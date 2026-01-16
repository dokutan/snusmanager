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
import { Snus, LocationAmount } from '../../snus';

class Location {
  id: number | undefined;
  name: string | undefined;
  constructor(id: number, name: string){
    this.id = id;
    this.name = name;
  }
}

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

  locations: Location[] = [];
  snustypes: any = [];
  snus: Snus = new Snus();
  counts: any = [];

  ngOnInit() {
    this.service.getLocations()
      .subscribe(response => {
        this.locations = response as Location[];
      });
    this.service.getSnusTypes()
      .subscribe(response => {
        this.snustypes = response;
      });

    this.snus.type = "other";

    if (this.data.action == "edit" && this.data.id) {
      this.service.getSnusById(this.data.id)
        .subscribe(response => {
          this.snus = response as Snus;
          this.snus.locations.forEach((l) => {
            if(l.id) this.counts[l.id] = l.amount;
          })
        });
    }
  }

  onDelete(id: number | null) {
    if (id) {
      this.service.deleteSnus(id);
    }
  }

  onSubmit() {
    // set snus.locations from counts
    this.snus.locations = []
    this.locations.forEach((l) => {
      if(l.id && this.counts[l.id] !== undefined && this.counts[l.id] !== null){
        this.snus.locations.push(new LocationAmount(l.id, this.counts[l.id]))
      }
    })

    switch (this.data.action) {
      case "add":
        this.service.addSnus(this.snus);
        break;
      case "edit":
        if (this.snus.id) this.service.updateSnus(this.snus.id, this.snus);
        break;
      default:
        break;
    }
  }

  onFileSelected() {
    const inputNode: any = document.querySelector('#file');

    if (typeof (FileReader) !== 'undefined') {
      const reader = new FileReader();

      reader.onload = (e: any) => {
        const array = Uint16Array.from(new Uint8Array(e.target.result));
        const binaryString = new TextDecoder("UTF-16").decode(array);
        this.snus.thumbnail_base64 = btoa(binaryString);
        this.snus.thumbnail_mime = inputNode.files[0].type;
      };

      reader.readAsArrayBuffer(inputNode.files[0]);
    }
  }

}
