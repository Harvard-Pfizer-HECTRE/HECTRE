from fastapi import status
from typing import Tuple


class ResponseHandler:
    @staticmethod
    def handle_upload_response(response: Tuple[bool, str]):
        """
        Handles the response from the upload_file and upload_files methods
        Args:
            response (Tuple[bool, str]): Tuple containing a boolean and a string
        Returns:
            dict: A dictionary containing a message, status, and folder
        """
        if response[0]:
            return {
                "message": "All files uploaded successfully!",
                "status": status.HTTP_200_OK,
                "folder": response[1],
            }
            # invoke hectre api here
        else:
            return {
                "message": "Some files failed to upload.",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }

    def handle_extraction_response(response: bool):
        """
        Handles the response from the extract method
        Args:
            response (bool): A boolean indicating if the extraction was successful
        returns:
            dict: A dictionary containing a message and status
        """
        if response:
            return {
                "message": "All files extracted successfully!",
                "status": status.HTTP_200_OK,
            }
        else:
            return {
                "message": "Some files failed to extract.",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
