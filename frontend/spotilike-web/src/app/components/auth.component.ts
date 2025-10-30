import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { login, isAuthenticated } from '../services/auth.service';

@Component({
  selector: 'app-auth',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
  <section class="auth">
    <h1>Connexion</h1>
    <form (ngSubmit)="onSubmit()" #f="ngForm">
      <div class="row">
        <label>Username</label>
        <input name="username" [(ngModel)]="username" required />
      </div>
      <div class="row">
        <label>Password</label>
        <input name="password" [(ngModel)]="password" type="password" required />
      </div>
  <button type="submit">Se connecter</button>
  <a routerLink="/signup" class="link">Créer un compte</a>
      <p class="error" *ngIf="error">{{ error }}</p>
    </form>
  </section>
  `,
  styles: [`
    .auth { max-width: 360px; margin: 64px auto; padding: 24px; border: 1px solid #e0e0e0; border-radius: 12px; }
    .row { display: flex; flex-direction: column; gap: 6px; margin-bottom: 12px; }
    input { padding: 8px 10px; border: 1px solid #ccc; border-radius: 6px; }
    button { margin-right: 8px; }
    .link { background: none; border: none; color: #1976d2; cursor: pointer; text-decoration: underline; }
    .error { color: #b00020; margin-top: 8px; }
  `]
})
export class AuthComponent {
  username = '';
  password = '';
  error = '';

  constructor(private router: Router) {
    if (isAuthenticated()) this.router.navigateByUrl('/artists');
  }

  async onSubmit() {
    this.error = '';
    try {
      await login(this.username, this.password);
      this.router.navigateByUrl('/artists');
    } catch (e: any) {
      this.error = e?.message || 'Erreur';
    }
  }
}
