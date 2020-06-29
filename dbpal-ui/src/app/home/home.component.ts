import {Component, OnInit} from '@angular/core';
import {HomePatientService} from './home.service';
import {Patient} from './patients.model';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  sqlResponse: string;

  filter: string;

  patient: Patient;

  /**
   * Contains the rows of the tables
   */
  patients: Patient[] = [];

  constructor(private homePatientService: HomePatientService) {
  }

  ngOnInit(): void {
  }


  /**
   * After the succesful completion of the rest call
   * Sets the table values with the page that is retrieved
   * from the Rest
   * @param response
   */
  mapResult(response) {
    this.patients = [];
    this.sqlResponse = '';
    if (response && response.result.length !== 0) {
      this.patients = response.result;
      this.sqlResponse = response.sqlResponse;
    }
  }

  searchPatientsResultsMock() {

  }

  /**
   * Function that is called when the user clicks on the button 'Filter Anwenden'
   * @param dt
   */
  searchPatientsResults(dt) {
    this.homePatientService
      .getPatientsData(this.filter)
      .then(response => this.mapResult(response))
      .catch(error => {

      });
  }
}
