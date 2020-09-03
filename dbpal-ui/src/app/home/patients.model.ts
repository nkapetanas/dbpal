export class Patient {
  /**
   * Value of the column id
   */
  id: string;

  /**
   * Value of the column first_name
   */
  first_name: string;

  /**
   * Value of the column last_name
   */
  last_name: string;

  /**
   * Value of the column diagnosis
   */
  diagnosis: string;

  /**
   * Value of the column gender
   */
  gender: string;

  /**
   * Value of the column length_of_stay
   */
  length_of_stay: string;
  /**
   * Value of the column age
   */
  age: string;
}

export class CombinedModel {

  result: Patient[];
  sqlResponse: string;
  sqlResponsePreprocessor: string;
  translatedSqlResponse: string;
}
