import {Injectable} from '@angular/core';
import {HttpParams} from '@angular/common/http';
import {HttpClient} from '@angular/common/http';
import {Consts} from '../../utils/consts.util';
import {Rest} from '../../utils/rest';


@Injectable()
export class HomePatientService {
  /**
   * Util wrapper for Rest Calls
   */
  private rest: Rest;


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
}
