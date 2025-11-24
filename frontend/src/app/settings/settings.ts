import { Component, inject, OnInit } from '@angular/core';
import { RouterLink } from "@angular/router";
import { MatAnchor, MatIconButton } from "@angular/material/button";
import { MatList, MatListItem } from '@angular/material/list';
import { Backend } from '../../services/backend';
import { MatIcon } from '@angular/material/icon';
import { MatDialog } from '@angular/material/dialog';
import { AddLocation } from '../add-location/add-location';

@Component({
  selector: 'app-settings',
  imports: [RouterLink, MatAnchor, MatList, MatListItem, MatIconButton, MatIcon],
  templateUrl: './settings.html',
  styleUrl: './settings.css'
})
export class Settings implements OnInit {
  private service = inject(Backend);
  readonly dialog: MatDialog = inject(MatDialog);

  locations: any = [];

  ngOnInit() {
    this.service.getLocations()
      .subscribe(response => {
        this.locations = response;
      });
  }

  cropImages() {
    this.service.cropImages()
  }

  calculateMissing() {
    this.service.calculateMissing()
  }

  addLocation() {
    this.dialog.open(AddLocation).afterClosed().subscribe(() => {
      this.ngOnInit()
    })
  }

  deleteLocation(id: number) {
    this.service.deleteLocation(id).subscribe(() => {
      this.ngOnInit()
    })
  }
}
