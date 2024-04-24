import { Component, EventEmitter, Input, Output  } from '@angular/core';


@Component({
  selector: 'app-output',
  standalone: true,
  imports: [],
  templateUrl: './output.component.html',
  styleUrl: './output.component.css'
})
export class OutputComponent {

  @Input() currentPage: number = 1; // Ensure a default value is set
  @Output() pageChanged = new EventEmitter<number>();

  goToPage(page: number) {
    this.currentPage = page; // Update the current page
    this.pageChanged.emit(this.currentPage); // Emit the new page number
  }
  }



