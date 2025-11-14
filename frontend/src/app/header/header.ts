import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule, MatIconButton } from '@angular/material/button';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatSelectModule } from '@angular/material/select';
import { ReactiveFormsModule } from '@angular/forms';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { Dialog } from '@angular/cdk/dialog';
import { MAT_DIALOG_DATA, MatDialog, MatDialogModule } from '@angular/material/dialog';
import { TitleCasePipe } from '@angular/common';
import { EditSnus } from '../edit-snus/edit-snus';
import { ImportSnus } from '../import-snus/import-snus';
import { Backend } from '../../services/backend';
import { AddLocation } from '../add-location/add-location';

@Component({
  selector: 'app-header',
  imports: [
    MatToolbarModule,
    MatIconModule,
    MatExpansionModule,
    MatIconButton,
    MatSelectModule,
    ReactiveFormsModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    TitleCasePipe,
    MatDialogModule
  ],
  templateUrl: './header.html',
  styleUrl: './header.css'
})
export class Header {
  locations: any = [];
  snustypes: any = [];
  searchText: any;

  readonly dialog: MatDialog = inject(MatDialog);

  constructor(private service: Backend) { }

  addSnus() {
    this.dialog.open(EditSnus, {data: {action: "add"}})
  }

  importSnus() {
    const dialogRef = this.dialog.open(ImportSnus);

    //dialogRef.afterClosed().subscribe(result => {
    //  console.log(`Dialog result: ${result}`);
    //});
  }

  addLocation() {
    this.dialog.open(AddLocation);
  }

  ngOnInit() {
    this.service.getLocations()
      .subscribe(response => {
        this.locations = response;
      });
    this.service.getSnusTypes()
      .subscribe(response => {
        this.snustypes = response;
      });
  }
}
