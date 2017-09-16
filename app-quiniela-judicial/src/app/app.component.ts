import { Component, Inject, ViewChild, ElementRef , OnInit} from '@angular/core';
import { PageScrollConfig, PageScrollService, PageScrollInstance } from 'ng2-page-scroll';
import { MdDialog, MdDialogRef, MD_DIALOG_DATA } from '@angular/material';
import { DOCUMENT } from '@angular/common';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
   show1 = false;
   show2 = false;
   show3 = false;
   show4 = false;
   show5 = false;
   show6 = false;
   courts = [
     { show: false, name: 'Juzgado 1', number: 1 },
     { show: false, name: 'Juzgado 2', number: 2 },
     { show: false, name: 'Juzgado 3', number: 3 },
     { show: false, name: 'Juzgado 4', number: 4 },
     { show: false, name: 'Juzgado 5', number: 5 },
     { show: false, name: 'Juzgado 6', number: 6 },
     { show: false, name: 'Juzgado 7', number: 7 },
     { show: false, name: 'Juzgado 8', number: 8 },
     { show: false, name: 'Juzgado 9', number: 9 },
     { show: false, name: 'Juzgado 10', number: 10 },
     { show: false, name: 'Juzgado 11', number: 11 },
     { show: false, name: 'Juzgado 12', number: 12 }, 
   ] 
    constructor(private pageScrollService: PageScrollService, @Inject(DOCUMENT) private document: any, 
      public dialog: MdDialog) {
      this.initScroll();
  }


  ngOnInit() {
    this.goToHome();
    setTimeout(() => this.show1 = true, 200);
    setTimeout(() => this.show2 = true, 400);
    setTimeout(() => this.show3 = true, 600);
    setTimeout(() => this.show4 = true, 800);
    setTimeout(() => this.show5 = true, 1000);
    setTimeout(() => this.show6 = true, 1200);
  }
  initScroll() {
    PageScrollConfig.defaultEasingLogic = {
        ease: (t: number, b: number, c: number, d: number): number => {
          // easeInOutExpo easing
          if (t === 0) return b;
          if (t === d) return b + c;
          if ((t /= d / 2) < 1) return c / 2 * Math.pow(2, 10 * (t - 1)) + b;
          return c / 2 * (-Math.pow(2, -10 * --t) + 2) + b;
        }
    };
  }
   goToHome() {
    let pageScrollInstance: PageScrollInstance = PageScrollInstance.simpleInstance(this.document, `#page-1`);
     this.pageScrollService.start(pageScrollInstance);
  }
  doSmth(reachedTarget: boolean): void {
    if (reachedTarget) {
      this.courts.forEach((court, index) => {
        let time = index * 150;
        setTimeout(() => court.show = true, time);
      });
    }
   }
   openDialog(court): void {
    let dialogRef = this.dialog.open(DialogOverviewExampleDialog, {
      data: { court: court }
    });
  }
}


@Component({
  selector: 'dialog-overview-example-dialog',
  template: `
    <div>
      <div style="font-weight: bold;text-align: center;font-size: 24px;">{{data.court.name}}</div>
      <img src="assets/images/grafico-{{data.court.number}}.png" style="width: 100%;">
    </div>
  `,
})
export class DialogOverviewExampleDialog {

  constructor(
    public dialogRef: MdDialogRef<DialogOverviewExampleDialog>,
    @Inject(MD_DIALOG_DATA) public data: any) { 
  }
  onNoClick(): void {
    this.dialogRef.close();
  }
}