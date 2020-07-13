import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import { HttpClient, HttpClientModule, HttpClientXsrfModule} from '@angular/common/http';
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
import {PaginatorModule, MessageService} from 'primeng';
import {HomePatientService} from './home/home.service';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MessagesModule} from 'primeng/messages';
import {MessageModule} from 'primeng/message';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
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
    MessagesModule,
    MessageModule
  ],
  providers: [HomePatientService, MessageService],
  bootstrap: [AppComponent]
})
export class AppModule {
}
