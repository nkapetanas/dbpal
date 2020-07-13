import { Injectable } from '@angular/core';
import { HttpHeaders, HttpClient } from '@angular/common/http';
import { retry, catchError, timeout } from 'rxjs/operators';
import { throwError } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class RestApiService {

    httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'application/json'
        })
    };

    constructor(private httpClient: HttpClient) {}

    public getPatients(input: String) {
        return this.httpClient.get<any>(`$api/patients/`, this.httpOptions).pipe(
          catchError((err) => {
            console.error(err.message);
            return throwError(err.message);
          })
        );
    }

}
