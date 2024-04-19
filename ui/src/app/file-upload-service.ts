/**
 * A service to upload files to the server
 * @author Manny Kwaning
 * @author Carl Zhao
 * @author James Nicholson
 * @author Kartik Srikumar
 * @author Veronika Post
 */

import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable, throwError } from "rxjs";
import { catchError } from "rxjs/operators";
import { ExtendedFileModel } from "./extended-file-model";

@Injectable({
    providedIn: 'root'
})
export class FileUploadService {
    constructor(private httpClient: HttpClient) { }

    uploadFiles(file: ExtendedFileModel): Observable<any> {
        return this.httpClient
            .post(file.uploadUrl, file.file, {
                observe: 'events', // observe the progress of the upload
                reportProgress: true
            })
            .pipe(catchError(error => {
                console.error('Error uploading file', error);
                return throwError(() => error);
            }));
    }
}