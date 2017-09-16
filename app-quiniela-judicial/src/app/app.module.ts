import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppComponent, DialogOverviewExampleDialog } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { Ng2PageScrollModule } from 'ng2-page-scroll';
import { MdDialogModule } from '@angular/material';

@NgModule({
  declarations: [
    AppComponent,
    DialogOverviewExampleDialog,
  ],
  imports: [
    BrowserModule,
    Ng2PageScrollModule,
    MdDialogModule,
    BrowserAnimationsModule,
  ],
  entryComponents: [
    DialogOverviewExampleDialog,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
