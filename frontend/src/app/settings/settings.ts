import { Component, inject, OnInit } from '@angular/core';
import { RouterLink } from "@angular/router";
import { MatAnchor, MatIconButton } from "@angular/material/button";
import { MatList, MatListItem } from '@angular/material/list';
import { Backend } from '../../services/backend';
import { MatIcon } from '@angular/material/icon';
import { MatDialog } from '@angular/material/dialog';
import { AddLocation } from '../add-location/add-location';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-settings',
  imports: [RouterLink, MatAnchor, MatList, MatListItem, MatIconButton, MatIcon],
  templateUrl: './settings.html',
  styleUrl: './settings.css'
})
export class Settings implements OnInit {
  private service = inject(Backend);
  readonly dialog: MatDialog = inject(MatDialog);

  readonly url = environment.apiUrl;

  locations: any = [];
  selectedFile: any = null;

  ngOnInit() {
    this.service.getLocations()
      .subscribe(response => {
        this.locations = response;
      });
  }

  cropImages() {
    this.service.cropImages()
  }

  convertImages() {
    this.service.convertImages()
  }

  calculateMissing() {
    this.service.calculateMissing()
  }

  addLocation() {
    this.dialog.open(AddLocation).afterClosed().subscribe(() => {
      this.ngOnInit()
    })
  }

  exportSnus() {
    this.service.getSnusBlob().subscribe(blob => {
      const a = document.createElement('a');
      const objectUrl = URL.createObjectURL(blob);

      a.href = objectUrl;
      a.download = "snus";
      a.click();

      URL.revokeObjectURL(objectUrl);
    });
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length) return;

    const file = input.files[0];
    const reader = new FileReader();

    reader.onload = () => {
      this.selectedFile = JSON.parse(reader.result as string);
    };

    reader.readAsText(file);
  }

  importSnus() {
    if(this.selectedFile) this.service.addSnusBlob(this.selectedFile).subscribe(response => { });
  }

  deleteLocation(id: number) {
    this.service.deleteLocation(id).subscribe(() => {
      this.ngOnInit()
    })
  }
}
