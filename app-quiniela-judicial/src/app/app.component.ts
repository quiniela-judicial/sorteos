import { Component, Inject, ViewChild, ElementRef , OnInit} from '@angular/core';
import { DOCUMENT} from '@angular/common';
import { PageScrollConfig, PageScrollService, PageScrollInstance } from 'ng2-page-scroll';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  
})
export class AppComponent implements OnInit {
  @ViewChild('container')
   private container: ElementRef;
   show1 = false;
   show2 = false;
   show3 = false;
   show4 = false;
   show5 = false;
   show6 = false;
  constructor(private pageScrollService: PageScrollService, @Inject(DOCUMENT) private document: any) {
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
  ngOnInit() {
    setTimeout(() => {
      this.show1 = true;
    }, 100)
    setTimeout(() => {
      this.show2 = true;
    }, 500)
    setTimeout(() => {
      this.show3 = true;
    }, 700)
    setTimeout(() => {
      this.show4 = true;
    }, 2300)
    setTimeout(() => {
      this.show5 = true;
    }, 2600)
     setTimeout(() => {
      this.show6 = true;
    }, 3000)

  }
  goToPage(page) {
    console.log(page);
    let pageScrollInstance: PageScrollInstance = PageScrollInstance.simpleInstance(this.document, `#${page}`);
     this.pageScrollService.start(pageScrollInstance);
  }
  doSmth(reachedTarget: boolean): void {
    console.log(reachedTarget);
    if (reachedTarget) {

        console.log('Yeah, we reached our destination');
    } else {
        console.log('Ohoh, something interrupted us');
    }
  }
    public barChartOptions:any = {
    scaleShowVerticalLines: false,
    responsive: true
  };
  public barChartLabels:string[] = ['2006', '2007', '2008', '2009', '2010', '2011', '2012'];
  public barChartType:string = 'bar';
  public barChartLegend:boolean = true;
 
  public barChartData:any[] = [
    {data: [65, 59, 80, 81, 56, 55, 40], label: 'Series A'},
    {data: [28, 48, 40, 19, 86, 27, 90], label: 'Series B'}
  ];
 
  // events
  public chartClicked(e:any):void {
    console.log(e);
  }
 
  public chartHovered(e:any):void {
    console.log(e);
  }
 
  public randomize():void {
    // Only Change 3 values
    let data = [
      Math.round(Math.random() * 100),
      59,
      80,
      (Math.random() * 100),
      56,
      (Math.random() * 100),
      40];
    let clone = JSON.parse(JSON.stringify(this.barChartData));
    clone[0].data = data;
    this.barChartData = clone;
    /**
     * (My guess), for Angular to recognize the change in the dataset
     * it has to change the dataset variable directly,
     * so one way around it, is to clone the data, change it and then
     * assign it;
     */
  }
}
