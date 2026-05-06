import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogActions, MatDialogClose, MatDialogContent, MatDialogModule, MatDialogTitle, } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatSnackBar } from '@angular/material/snack-bar';
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
export class ImportSnus {
  private service = inject(Backend);
  readonly snackBar: MatSnackBar = inject(MatSnackBar);

  url = "";

  onSubmit() {
    this.service.importSnus(this.url).subscribe(response => {
      if(response.ok)
        this.snackBar.open('Imported snus', undefined, {duration: 500});
      else
        this.snackBar.open('Failed to import Snus', undefined, {duration: 500});
    })
  }
}
