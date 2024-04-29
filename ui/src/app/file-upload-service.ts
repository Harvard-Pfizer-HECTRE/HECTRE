/**
 * A service to upload files to the server
 * @author Manny Kwaning
 * @author Carl Zhao
 * @author James Nicholson
 * @author Kartik Srikumar
 * @author Veronika Post
 */

import { HttpClient, HttpEventType } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable, throwError } from "rxjs";
import { catchError, tap } from "rxjs/operators";
import { ExtendedFileModel } from "./extended-file-model";

@Injectable({
    providedIn: 'root'
})
export class FileUploadService {
    constructor(private httpClient: HttpClient) { }

    /**
     * Uploads a file to the server
     * @param file the file to upload
     * @returns an observable that will emit the response from the server
     */
    uploadFiles(file: ExtendedFileModel): Observable<any> {

        const formData: FormData = new FormData();
        formData.append('file', file.file);
        return this.httpClient
            .post(file.uploadUrl, formData, {
                observe: 'events', // observe the progress of the upload
                reportProgress: true,
                responseType: 'json',
            })
            .pipe(
                tap(response => {
                    if (response.type === HttpEventType.Response) {
                        console.log('response: ', response)
                        if (response.body && (response.body as { folder: string }).folder) {
                            file.folder = (response.body as { folder: string }).folder;
                            console.log('folder: ', file.folder);
                        }
                    }
                }),
                catchError(error => {
                    console.error('Error uploading file', error);
                    return throwError(() => error);
                }));
    }

    /**
     * Submits folder id and picos string to the server to extract files
     * @param folder_id 
     * @param outcomes_string 
     * @returns 
     */
    extractFiles(folder_id: string, outcomes_string: string): Observable<any> {
        const url = 'http://127.0.0.1:5000/files/extract/';
        const body = { folder_id: folder_id, outcomes_string: outcomes_string };

        console.log(`folder_id:, ${folder_id}, picos: ${outcomes_string}`);
        return this.httpClient.post(url, body, {
            reportProgress: true,
            observe: 'events',
            responseType: 'json',
            headers: { 'Content-Type': 'application/json' }
        }).pipe(
            tap(response => {
                if (response.type === HttpEventType.Response) {
                    console.log('response: ', response);
                }
            }),
            catchError(error => {
                console.error('Error extracting files', error);
                return throwError(() => error);
            })
        );
    }
}