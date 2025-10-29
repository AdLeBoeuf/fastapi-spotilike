import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { fetchArtists, Artist } from '../services/artists.service';

@Component({
  selector: 'app-artists-list',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
  <section class="container">
    <h1>Artists</h1>
    <div *ngIf="error" class="error">{{error}}</div>
    <ul *ngIf="artists?.length; else empty">
      <li *ngFor="let a of artists">
        <img *ngIf="a.avatar" [src]="a.avatar" width="32" height="32" style="object-fit:cover;border-radius:50%;margin-right:8px;" />
        <a [routerLink]="['/artists', a.id]"><strong>{{a.name}}</strong></a>
        <span *ngIf="a.bio" style="color:#666;margin-left:6px;">— {{a.bio}}</span>
      </li>
    </ul>
    <ng-template #empty>
      <p>No artists yet.</p>
    </ng-template>
  </section>
  `,
  styles: [`
    .container { max-width: 720px; margin: 24px auto; padding: 0 16px; }
    ul { list-style: none; padding: 0; }
    li { display: flex; align-items: center; padding: 8px 0; border-bottom: 1px solid #eee; }
    .error { color: #b00020; }
  `]
})
export class ArtistsListComponent implements OnInit {
  artists: Artist[] = [];
  loading = false;
  error = '';

  async ngOnInit() {
    await this.load();
  }

  async load() {
    this.loading = true;
    this.error = '';
    try {
      this.artists = await fetchArtists();
    } catch (e: any) {
      this.error = e?.message || 'Failed to load artists';
    } finally {
      this.loading = false;
    }
  }
}
