import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import { HttpClientModule, HttpClientXsrfModule} from '@angular/common/http';
import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {HomeComponent} from './home/home.component';
import {AccordionModule} from 'primeng/accordion';
import {MenuModule} from 'primeng/menu';
import {TableModule} from 'primeng/table';
import {InputTextModule} from 'primeng/inputtext';
import {ButtonModule} from 'primeng/button';
import {InputTextareaModule} from 'primeng/inputtextarea';
import {CheckboxModule} from 'primeng/checkbox';
import {DialogModule} from 'primeng/dialog';
import {PanelModule} from 'primeng/panel';
import {PaginatorModule} from 'primeng';
import {HomePatientService} from './home/home.service';
import { PagenotfoundComponent } from './pagenotfound/pagenotfound.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    PagenotfoundComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AccordionModule,
    MenuModule,
    TableModule,
    InputTextModule,
    ButtonModule,
    InputTextareaModule,
    CheckboxModule,
    DialogModule,
    PanelModule,
    HttpClientModule,
    HttpClientXsrfModule,
    PaginatorModule,
  ],
  providers: [HomePatientService],
  bootstrap: [AppComponent]
})
export class AppModule {
}
