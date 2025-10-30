import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterLink, RouterLinkActive, Router } from '@angular/router';
import { isAuthenticated, logout } from './services/auth.service';

@Component({
  selector: 'app-root',
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('spotilike-web');
  get auth() { return isAuthenticated(); }

  constructor(private router: Router) {}

  onLogout() {
    logout();
    this.router.navigateByUrl('/login');
  }
}
