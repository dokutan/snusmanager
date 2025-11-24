import { Routes } from '@angular/router';
import { Settings } from './settings/settings';
import { Snuslist } from './snuslist/snuslist';

export const routes: Routes = [{component: Settings, path: "settings"}, {component: Snuslist, path: ""}];
