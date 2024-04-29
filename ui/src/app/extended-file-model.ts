export interface ExtendedFileModel {
    file: File;
    uploadUrl: string;
    folder: string;
    uploadStatus: {
        isSuccess: boolean;
        isError: boolean;
        errorMessage: string;
        progressCount: number;
    }
}