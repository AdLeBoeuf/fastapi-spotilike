import { Routes } from '@angular/router';
import { ArtistsListComponent } from './components/artists-list.component';
import { AlbumsListComponent } from './components/albums-list.component';
import { AlbumDetailComponent } from './components/album-detail.component';
import { ArtistDetailComponent } from './components/artist-detail.component';
import { SongsListComponent } from './components/songs-list.component';

export const routes: Routes = [
	{ path: '', redirectTo: 'artists', pathMatch: 'full' },
	{ path: 'artists', component: ArtistsListComponent },
	{ path: 'artists/:id', component: ArtistDetailComponent },
	{ path: 'albums', component: AlbumsListComponent },
	{ path: 'albums/:id', component: AlbumDetailComponent },
    { path: 'songs', component: SongsListComponent },
];
