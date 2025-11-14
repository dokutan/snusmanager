import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogActions, MatDialogClose, MatDialogContent, MatDialogModule, MatDialogTitle, } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
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

  url = "";

  onSubmit() {
    this.service.importSnus(this.url)
  }
}
