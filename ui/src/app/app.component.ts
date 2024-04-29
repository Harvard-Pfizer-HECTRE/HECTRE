/**
 * This component is the main component of the file upload application.
 * @author Manny Kwaning
 * @author Carl Zhao
 * @author James Nicholson
 * @author Kartik Srikumar
 * @author Veronika Post
 */

import { Component } from '@angular/core';
import { Observable, forkJoin, of } from 'rxjs';
import {
  HttpEventType,
  HttpResponse
} from '@angular/common/http';
import { catchError, tap } from 'rxjs/operators';
import { ExtendedFileModel } from './extended-file-model';
import { FileUploadService } from './file-upload-service';
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})

export class AppComponent {

  /**
   * @param form - form group for the file upload component
   */
  form: FormGroup;

  /**
   * @param title - title of the file upload component
   */
  title = 'HECTRE File Upload';

  /**
   * @param filesToUploadList - list of files to upload
   */
  filesToUploadList: ExtendedFileModel[] = [];

  /**
   * @param isUploadComplete - boolean to check if the upload is complete
   */
  isUploadComplete: boolean = false;

  /**
   * @param extractionProgress - progress of the extraction
   */
  extractionProgress: number = 0;

  /**
   * @param extractionErrorMessage - error message for the extraction
   */
  extractionErrorMessage: string = '';

  constructor(private fileUploadService: FileUploadService, private fb: FormBuilder) {
    this.form = this.fb.group({
      picosString: ['']
    });
  }

  /**
   * Add files to the file upload list
   * @param event 
   * @returns 
   */
  addFiles(event: Event) {
    this.filesToUploadList = [];
    const { target } = event;
    const filesList = (target as HTMLInputElement).files;
    if (!filesList) return;
    this.costructFilesUploadList(filesList);
  }

  /**
   * Upload files to the server
   */
  uploadFiles(): void {
    const requestsList = this.contructRequestsChain();
    this.executeFileUpload(requestsList);
  }

  /**
   * Clear files from the file upload list
   */
  clearFiles(): void {
    this.filesToUploadList = [];
    const fileInput = document.getElementById('formFileMultiple') as HTMLInputElement;
    fileInput.value = '';
  }

  /**
   * Extract files
   */
  extractFiles(): void {
    console.log('Extracting files');
    const picos_string = this.form.get('picosString')?.value;
    console.log('Picos string: ', picos_string);
    const folder_id = this.filesToUploadList[0].folder;
    this.fileUploadService.extractFiles(folder_id, picos_string).subscribe({
      next: event => {
        if (event.type === HttpEventType.UploadProgress) {
          this.extractionProgress = Math.round((100 * event.loaded) / event.total);
        } else if (event instanceof HttpResponse) {
          console.log('Extraction complete');
        }
      },
      error: error => {
        this.extractionErrorMessage = error.statusText;
        console.error('Error extracting files', error.message);
      }
    });
  }

  /**
   * Construct a chain of requests to upload files
   * @returns any
   */
  private contructRequestsChain(): any {
    return this.filesToUploadList.map((file, index) => {
      return this.fileUploadService.uploadFiles(file).pipe(
        tap((event) => {
          if (event.type === HttpEventType.UploadProgress) {
            this.filesToUploadList[index].uploadStatus.progressCount = Math.round((100 * event.loaded) / event.total);
          }
        }),
        catchError((error) => {
          return of({ isError: true, index, error });
        })
      );
    });
  }

  /**
   * Execute the file upload
   * @param requestChain 
   */
  private executeFileUpload(requestChain: Observable<any>[]): void {
    forkJoin(requestChain).subscribe((response: any) => {
      response.forEach((file: { isError: any, index: number; error: { statusText: string; }; }) => {
        if (file.isError) {
          this.filesToUploadList[file.index].uploadStatus.isError = true;
          this.filesToUploadList[file.index].uploadStatus.errorMessage = file.error.statusText;
        }
      });
    })
    this.isUploadComplete = true;
  }

  /**
   * Construct a list of files to upload
   * @param filesList 
   */
  private costructFilesUploadList(filesList: FileList): void {
    Array.from(filesList).forEach((file: File, index: number) => {
      const newFile: ExtendedFileModel = {
        file: file,
        uploadUrl: 'http://127.0.0.1:5000/files/upload_file',
        folder: '',
        uploadStatus: {
          isSuccess: false,
          isError: false,
          errorMessage: '',
          progressCount: 0
        },
      };
      this.filesToUploadList.push(newFile);
    });
  }
}
