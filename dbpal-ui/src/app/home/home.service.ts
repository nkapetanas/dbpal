import {Injectable} from '@angular/core';
import {HttpParams, HttpHeaders} from '@angular/common/http';
import {HttpClient} from '@angular/common/http';
import {Consts} from '../../utils/consts.util';
import {Rest} from '../../utils/rest';
import { catchError } from 'rxjs/operators';
import { throwError } from 'rxjs';


@Injectable()
export class HomePatientService {
  /**
   * Util wrapper for Rest Calls
   */
  private rest: Rest;

  httpOptions = {
    headers: new HttpHeaders({
        'Content-Type': 'application/json'
    })
  };

  constructor(private http: HttpClient) {
    this.rest = new Rest(http);
  }

  getPatientsData(pageParam: string): Promise<string> {
    // Define the Query Parameters for the request
    let params: HttpParams = new HttpParams();

    if (pageParam !== null) {
      params = params.set(
        'patientQuestion',
        encodeURIComponent(pageParam)
      );
    }

    return this.rest.getWithParamsAsJson(Consts.PATIENTS_TABLE, params);
  }

  public getPetientsDataMock(input: String) {
    return this.http.get<any>(`https://localhost:8080/api/patients`).pipe(
      catchError((err) => {
        console.error(err.message);
        return throwError(err.message);
      })
    );
  }
}
