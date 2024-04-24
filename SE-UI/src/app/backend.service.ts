import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable, Subject, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BackendService {

  private responseSubject = new Subject<any>();

  constructor(private http: HttpClient) {}

  getProblemsByPage(page: number): Observable<any> {
    // This will be adjusted based on the actual endpoint and response format
    return this.http.get(`http://127.0.0.1:5000/problems?page=${page}`);
  }

  // sendInput(input: string):void {
  //   // Replace the URL with your backend endpoint

  //    this.http.post<string>('http://127.0.0.1:5000/api/modified', { data: input }).subscribe(
  //     response => {
  //       this.responseSubject.next(response);
  //     },
  //     error => {
  //       console.error('Error contacting backend', error);
  //     }
  //   );
  // }

  // sendInput2(input: string):void {
  //   // Replace the URL with your backend endpoint

  //    this.http.post<string>('http://127.0.0.1:5000/api/direct', { data: input }).subscribe(
  //     response => {
  //       this.responseSubject.next(response);
  //     },
  //     error => {
  //       console.error('Error contacting backend', error);
  //     }
  //   );
  // }


  // getData(): Observable<any> {
  //   return this.responseSubject.asObservable();
  // }
}

