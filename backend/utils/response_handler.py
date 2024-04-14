from fastapi import status


class ResponseHandler:
    @staticmethod
    def handle_upload_response(success: bool):
        if success:
            return {
                "message": "All files uploaded successfully!",
                "status": status.HTTP_200_OK,
            }
            # invoke hectre api here
        else:
            return {
                "message": "Some files failed to upload.",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
