import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {Ng2PageScrollModule} from 'ng2-page-scroll';
import { AppComponent } from './app.component';
import { ChartsModule } from 'ng2-charts';
@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    ChartsModule,
    Ng2PageScrollModule.forRoot(),
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
