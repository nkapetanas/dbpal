import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Consts} from '../../utils/consts.util';
import {Rest} from '../../utils/rest';
import { catchError } from 'rxjs/operators';
import { throwError } from 'rxjs';
import {Patient} from "./patients.model";
import {CombinedModel} from "./patients.model";


@Injectable()
export class HomePatientService {
  /**
   * Util wrapper for Rest Calls
   */
  private rest: Rest;


  constructor(private http: HttpClient) {
    this.rest = new Rest(http);
  }

  public getPatientsDataMock(input: string) {
    // return this.http.get<any>(Consts.API_REL_PATH + Consts.PATIENTS_TABLE_COMBINED, {
    return this.http.get<any>('http://localhost:8080/', {
      params: {
        searchInput: input
      }}).pipe(
      catchError((err) => {
        console.error(err.message);
        return throwError(err.message);
      })
    );
  }
}
