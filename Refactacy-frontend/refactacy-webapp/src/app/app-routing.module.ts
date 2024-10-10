import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MainPageComponent } from './main-page/main-page.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { LearnMoreComponent } from './learn-more/learn-more.component';
import { DocumentationPageComponent } from './documentation-page/documentation-page.component';

const routes: Routes = [
  { path: '', redirectTo: '/main', pathMatch: 'full' }, // Rotta predefinita
  { path: 'main', component: MainPageComponent },       // Rotta per il main-page
  { path: 'doc', component: DocumentationPageComponent }       // Rotta per la documentazione
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
