import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { fetchAlbums, Album } from '../services/albums.service';

@Component({
  selector: 'app-albums-list',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
  <section class="container">
    <h1>Albums</h1>
    <div *ngIf="error" class="error">{{error}}</div>
    <ul *ngIf="albums?.length; else empty">
      <li *ngFor="let a of albums">
        <img *ngIf="a.cover" [src]="a.cover" width="40" height="40" style="object-fit:cover;border-radius:6px;margin-right:8px;" />
        <div class="meta">
          <a [routerLink]="['/albums', a.id]"><strong>{{a.title}}</strong></a>
          <small class="muted">released: {{ a.release_date || 'n/a' }}</small>
          <div *ngIf="a.artist_id" class="muted">
            by <a [routerLink]="['/artists', a.artist_id]">{{ a.artist_name || ('#' + a.artist_id) }}</a>
          </div>
        </div>
      </li>
    </ul>
    <ng-template #empty>
      <p>No albums yet.</p>
    </ng-template>
  </section>
  `,
  styles: [`
    .container { max-width: 720px; margin: 24px auto; padding: 0 16px; }
    ul { list-style: none; padding: 0; }
    li { display: flex; align-items: center; gap: 10px; padding: 10px 0; border-bottom: 1px solid #eee; }
    .muted { color: #666; }
    .error { color: #b00020; }
  `]
})
export class AlbumsListComponent implements OnInit {
  albums: Album[] = [];
  loading = false;
  error = '';

  async ngOnInit() {
    await this.load();
  }

  async load() {
    this.loading = true;
    this.error = '';
    try {
      this.albums = await fetchAlbums();
    } catch (e: any) {
      this.error = e?.message || 'Failed to load albums';
    } finally {
      this.loading = false;
    }
  }
}
