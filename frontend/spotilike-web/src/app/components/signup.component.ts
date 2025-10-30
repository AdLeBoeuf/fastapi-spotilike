import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { signup } from '../services/auth.service';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
  <section class="auth">
    <h1>Créer un compte</h1>
    <form (ngSubmit)="onSubmit()" #f="ngForm">
      <div class="row">
        <label>Username</label>
        <input name="username" [(ngModel)]="username" required />
      </div>
      <div class="row">
        <label>Email</label>
        <input name="email" [(ngModel)]="email" type="email" required />
      </div>
      <div class="row">
        <label>Password</label>
        <input name="password" [(ngModel)]="password" type="password" required />
      </div>
      <button type="submit">Créer mon compte</button>
      <a routerLink="/login" class="link">J'ai déjà un compte</a>
      <p class="error" *ngIf="error">{{ error }}</p>
    </form>
  </section>
  `,
  styles: [`
    .auth { max-width: 360px; margin: 64px auto; padding: 24px; border: 1px solid #e0e0e0; border-radius: 12px; }
    .row { display: flex; flex-direction: column; gap: 6px; margin-bottom: 12px; }
    input { padding: 8px 10px; border: 1px solid #ccc; border-radius: 6px; }
    button { margin-right: 8px; }
    .link { margin-left: 8px; color: #1976d2; text-decoration: underline; cursor: pointer; }
    .error { color: #b00020; margin-top: 8px; }
  `]
})
export class SignupComponent {
  username = '';
  email = '';
  password = '';
  error = '';

  constructor(private router: Router) {}

  async onSubmit() {
    this.error = '';
    try {
      await signup(this.username, this.email, this.password);
      // Connecte l'utilisateur automatiquement et redirige
      this.router.navigateByUrl('/artists');
    } catch (e: any) {
      this.error = e?.message || 'Erreur';
    }
  }
}
