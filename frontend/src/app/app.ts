import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Snuslist } from "./snuslist/snuslist";
import { Header } from "./header/header";

@Component({
  selector: 'app-root',
  imports: [/*RouterOutlet,*/ Snuslist, Header],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('snusmanager');
}
