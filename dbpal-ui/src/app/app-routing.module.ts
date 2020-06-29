import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {HomeComponent} from './home/home.component';
import {PagenotfoundComponent} from './pagenotfound/pagenotfound.component';


const routes: Routes = [
    {
    path: '',
    component: HomeComponent,
  },
      {
        path:"**",
        component: PagenotfoundComponent,

    }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
