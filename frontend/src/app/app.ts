import { Component, signal } from '@angular/core';
import { Snuslist } from "./snuslist/snuslist";
import { Header } from "./header/header";

@Component({
  selector: 'app-root',
  imports: [Snuslist, Header],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('snusmanager');
}
