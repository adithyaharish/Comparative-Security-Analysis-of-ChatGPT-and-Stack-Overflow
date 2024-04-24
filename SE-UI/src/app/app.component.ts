import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {InputComponent} from './input/input.component'
import { OutputComponent } from './output/output.component';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonToggleModule } from '@angular/material/button-toggle';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet,InputComponent, OutputComponent,MatFormFieldModule,MatInputModule, MatButtonToggleModule,],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'gptUI';
  selectedEndpoint: string = 'endpoint1'; // Default value

  onToggleChange(): void {
    // No need to manually handle the change as [(value)] is already two-way binding the property.
  }
}
