/**
 * This component is the main component of the file upload application.
 * @author Manny Kwaning
 * @author Carl Zhao
 * @author James Nicholson
 * @author Kartik Srikumar
 * @author Veronika Post
 */

import { Component } from '@angular/core';
import { forkJoin, of } from 'rxjs';
import {
  HttpEventType
} from '@angular/common/http';
import { catchError, tap } from 'rxjs/operators';
import { ExtendedFileModel } from './extended-file-model';
import { FileUploadService } from './file-upload-service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'HECTRE File Upload';

  filesToUploadList: ExtendedFileModel[] = [];

  constructor(private fileUploadService: FileUploadService) { }

  addFiles(event: Event) {
    this.filesToUploadList = [];
    const { target } = event;
    const filesList = (target as HTMLInputElement).files;
    if (!filesList) return;
    this.costructFilesUploadList(filesList);
  }

  uploadFiles(): void {
    const requestsList = this.contructRequestsChain();
    this.executeFileUpload(requestsList);
  }

  private contructRequestsChain(): any {
    return this.filesToUploadList.map((file, index) => {
      return this.fileUploadService.uploadFiles(file).pipe(
        tap(event => {
          if (event.type === HttpEventType.UploadProgress) {
            this.filesToUploadList[index].uploadStatus.progressCount = Math.round((100 * event.loaded) / event.total);
          }
        }),
        catchError(error => {
          return of({ isError: true, index, error });
        })
      );
    });
  }

  private executeFileUpload(requestChain: any[]): void {
    forkJoin([requestChain]).subscribe((response: any) => {
      response.forEach((file: { isError: any, index: number; error: { statusText: string; }; }) => {
        if (file.isError) {
          this.filesToUploadList[file.index].uploadStatus.isError = true;
          this.filesToUploadList[file.index].uploadStatus.errorMessage = file.error.statusText;
        } else {
          this.filesToUploadList[file.index].uploadStatus.isSuccess = true;
        }
      });
    })
  }

  private costructFilesUploadList(filesList: FileList): void {
    Array.from(filesList).forEach((file: File, index: number) => {
      const newFile: ExtendedFileModel = {
        file: file,
        uploadUrl: (index % 2 === 0) ? 'http://127.0.0.1:5000/files/upload/upload_files' : '',
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
