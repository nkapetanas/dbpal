import {HttpHeaders, HttpResponse, HttpParams} from '@angular/common/http';
import {Consts} from './consts.util';
import {HttpClient} from '@angular/common/http';

/**
 * Wrapper class for performing http requests to the REST API
 */
export class Rest {
  /**
   * HttpClient
   */
  private http: HttpClient;

  /**
   * Constructor for the util class
   * @param http
   */
  constructor(http: HttpClient) {
    this.http = http;
  }

  /**
   * GET REQUEST
   * @param resource
   */
  get(resource: string) {
    return this.http
      .get(Consts.API_REL_PATH + resource + '?' + new Date().toString(), {
        headers: this.getHeaders()
      })
      .toPromise()
      .then(response => response as any)
      .catch(err => {
        return Promise.reject(err.error || 'Server error');
      });
  }

  /**
   *
   * @param resource
   */
  getAsJson(resource: string) {
    return this.http
      .get(Consts.API_REL_PATH + resource + '?' + new Date().toString(), {
        headers: this.getHeaders(),
        withCredentials: true
      })
      .toPromise()
      .then(response => response as any)
      .catch(err => {
        return Promise.reject(err.error || 'Server error');
      });
  }

  getWithParamsAsJson(resource: string, params: any) {
    return this.http
      .get(Consts.API_REL_PATH + resource + '?' + new Date().toString(), {
        headers: this.getHeaders(),
        params,
        withCredentials: false
      })
      .toPromise()
      .then(response => response as any)
      .catch(err => {
        return Promise.reject(err.error || 'Server error');
      });
  }

  getHeaders(): HttpHeaders {
    const headers = new HttpHeaders()
      .set('Content-Type', 'application/json')
      .set('Accept-Language', 'el-GR,el;q=0.9,en-GB;q=0.8,en;q=0.7');
    return headers;
  }
}
