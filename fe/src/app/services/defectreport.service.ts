import { Injectable } from '@angular/core';
import { Observable, from } from 'rxjs';
import { retry, catchError, map } from 'rxjs/operators';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { livisConfig } from "../../config/constants";
import { HerrorService } from "./herror.service"
import { StorageService } from '../helpers/storage.service';

const environment = "development";
const environmentConfig = livisConfig[environment];
const baseUrl = environmentConfig.BASE_URL;
let httpOptions = {};

@Injectable({
  providedIn: 'root'
})
export class DefectreportService {

  constructor(private http: HttpClient, private hErrorService: HerrorService, private storageService: StorageService) {
    if (this.storageService.getUserDetails() && this.storageService.getUserDetails().token) {
      const token = this.storageService.getUserDetails().token;
      httpOptions = {
        headers: {
          Authorization: `Token ${token}`,
        },
      };
    }
  }

  getDefectReport(report_filter): Observable<any> {
    return this.http.post<any>(baseUrl + 'get_mega_report/', JSON.stringify(report_filter))
      .pipe(map(data => {
        return data;
      }), catchError(this.hErrorService.handleError.bind(this))
      );

  }

  getMasterDefectList(): Observable<any> {
    return this.http.get<{}>(baseUrl + 'cataler/get_master_defect_list/', {})
      .pipe(map(data => {
        return data;
      }), catchError(this.hErrorService.handleError.bind(this))
      );
  }

  getMasterFeatureList(): Observable<any> {
    return this.http.get<{}>(baseUrl + 'cataler/get_master_feature_list/', {})
      .pipe(map(data => {
        return data;
      }), catchError(this.hErrorService.handleError.bind(this))
      );
  }

  addRemark(payload): Observable<any> {
    return this.http
      .post<any>(
        baseUrl + 'reports/edit_remark/',
        payload,
        httpOptions
      )
      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
  }

  updateFlagStatus(payload): Observable<any> {
    return this.http
      .post<any>(
        baseUrl + 'reports/set_flag/',
        payload,
        httpOptions
      )
      .pipe(
        map((data) => {
          return data;
        }),
        catchError(this.hErrorService.handleError.bind(this))
      );
  }


}
