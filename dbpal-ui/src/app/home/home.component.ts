import {Component, OnInit} from '@angular/core';
import {HomePatientService} from './home.service';
import {Patient} from './patients.model';
import {Message} from 'primeng//api';
import {MessageService} from 'primeng/api';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  sqlResponse: string;

  sqlResponsePreprocessor: string;

  translatedSqlResponse: string;

  filter: string;

  /**
   * Contains the rows of the tables
   */
  patients: Patient[] = [];

  constructor(private homePatientService: HomePatientService,
    private messageService: MessageService) {
  }

  ngOnInit(): void {
  }


  /**
   * After the successful completion of the rest call
   * Sets the table values with the page that is retrieved
   * from the Rest
   * @param response
   */
  mapResult(response) {
    this.patients = [];
    this.sqlResponse = '';
    this.sqlResponsePreprocessor = '';
    this.translatedSqlResponse = '';

    if (response && response.result !== 0) {
      this.patients = response.patients;
      this.sqlResponse = response.sqlResponse;
      this.sqlResponsePreprocessor = response.sqlResponsePreprocessor;
      this.translatedSqlResponse = response.translatedSqlResponse;
    }
  }

  searchPatientsResultsMock() {
    let input= this.filter;
    if(input){
      this.homePatientService.getPatientsDataMock(input).subscribe((response) => {
        this.mapResult(response);
      },
        (error) => {
          this.messageService.add({severity:'danger', summary:'Service Message', detail:'The patients\' data could not be loaded.'});
          console.log(error);
        }
      );
    }
    else {
      this.messageService.add({severity:'danger', summary:'Validation Error', detail:'Please check all required fields, format and length.'});

    }
  }
}
