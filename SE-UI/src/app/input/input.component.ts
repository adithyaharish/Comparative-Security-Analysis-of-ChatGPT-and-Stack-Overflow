import { Component, Input, SimpleChanges,EventEmitter} from '@angular/core';
import { BackendService } from '../backend.service';
import { FormsModule } from '@angular/forms';
import { OutputComponent } from '../output/output.component';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common'; 
import { MatDialog } from '@angular/material/dialog';
import { MyDialogComponent } from '../my-dialog/my-dialog.component';
import { AnalysisComponent } from '../analysis/analysis.component';

@Component({
  selector: 'app-input',
  standalone: true,
  imports: [OutputComponent,FormsModule,CommonModule],
  templateUrl: './input.component.html',
  styleUrl: './input.component.css'
})
export class InputComponent {

  id: any;
  leftJson: any;
  rightJson: any;
  currentPage: number = 1;
  backendMessage: string = '';
  AnalysisMessage: string = '';
  backendTitle: string = '';
  loading: boolean = false;

  constructor(private backendService: BackendService, public dialog: MatDialog) {}

  ngOnInit() {
    this.loading = true;
    this.fetchProblems(this.currentPage);
  }

  onPageChanged(page: number) {
    this.fetchProblems(page);
  }

 fetchProblems(page: number) {
  this.loading = true;
  console.log(this.loading)
  this.currentPage = page; 
    this.backendService.getProblemsByPage(page).subscribe({
      next: (data) => {
        // Assuming the service returns an object with two properties: left and right
        this.id=data.id,
        this.leftJson = data.left;
        this.rightJson = data.right;
        this.backendTitle = data.title;
        this.backendMessage = data.body;
        this.AnalysisMessage = data.analysis;

        this.loading = false;
        console.log(this.loading)
      },
      error: (err) => {
      console.error('Error fetching problems: ', err);
      this.loading = false;
    }
    });
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(MyDialogComponent, {
      width: '700px',
      height: '500px',
      position: { 
        top: '50px', // Position it a little at the top
        left: 'calc(50% - 250px)' // Center it horizontally
      },
      data: {content: this.backendMessage}
    });
  
    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }

  getAnalysis(): void {
    const dialogRef = this.dialog.open(AnalysisComponent, {
      width: '700px',
      height: '500px',
      position: { 
        top: '70px', // Position it a little at the top
        left: 'calc(50% - 250px)' // Center it horizontally
      },
      data: {content: this.AnalysisMessage}
    });
  
    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }
  
}