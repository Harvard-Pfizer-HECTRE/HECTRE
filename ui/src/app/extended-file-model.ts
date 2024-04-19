export interface ExtendedFileModel {
    file: File;
    uploadUrl: string;
    uploadStatus: {
        isSuccess: boolean;
        isError: boolean;
        errorMessage: string;
        progressCount: number;
    }
}