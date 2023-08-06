# -*- coding: utf-8 -*-
import requests
import base64
import json
import time
import ntpath
import os


class CaptureFastBase:
    accesstoken: str = None

    def _init_client(self):
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        authRequest = {
            "username": self.cfusername,
            "password": self.cfpassword,
            "grant_type": "password"
        }

        response = requests.request(
        "POST", "https://api.capturefast.com/token",
        headers=headers,
        data=authRequest
        )

        if not response.json().get('access_token'):
            raise Exception(response.json().get('error_description'))

        time.sleep(1)
        self.accesstoken = response.json().get('access_token')

    def UploadDocument(self, filepath, documenttypeid):
        """Method used to upload your documents to Capturefast.

        Args:
            filepath(str):      path of the document to be uploaded
            documenttypeid(int):        ID of the document you used in Capturefast

        Returns:
            int:   The documentId created for the uploaded document that is created by Capturefast  and you need this documentId to get the data
        """
        fileContent = ''
        with open(filepath, "rb") as f:
            fileContent = base64.b64encode(f.read()).decode('ascii')

        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + self.accesstoken
        }

        document = {
            'TeamId':  self.teamid,
            'DocumentTypeId': documenttypeid,
            'Files': [{'FileName': os.path.basename(filepath),
                       'Content': fileContent}]
        }
        try:
            response = requests.request("POST",
                                        "https://api.capturefast.com/api/Upload/Document",
                                        headers=headers,
                                        data=json.dumps(document))

            if(response.json().get('ResultCode') != 0):
                raise Exception(response.json().get('ResultMessage'))

        except Exception as ex:
            raise Exception("Capturefast Communication Error")

        return response.json().get('DocumentId')

    def GetDocumentData(self, documentid, timeoutinseconds=100):
        """Getting data of a document uploaded to Capturefat

            Args:
                documentid(int):      Documentid from UploadDocument method
                timeoutinseconds(int):        The required timeout for data retrieval depending on the time the document spends in the processing phase değeri.Default 100 second.

            Returns:
                Json:   Processing and content data of the submitted document

                {
                       "DocumentName":"",
                       "DocReferenceKey":"",
                       "DocumentId":0,
                       "TeamId":0,
                       "TemplateId":0,
                       "TemplateName":",
                       "DocumentTypeId":0,
                       "DocumentTypeName":"",
                       "CapturedUserId":0,
                       "CapturedDate":"",
                       "CapturedUser":"",
                       "VerifiedUserId":0,
                       "VerifiedDate":,
                       "VerifiedUser":,
                       "AdditionalData":,
                       "Pages":[
                          {
                             "PageId":0,
                             "PageName":"Page #1",
                             "PageOrder":1,
                             "OrginalFileName":"",
                             "Fields":[
                                {
                                   "FieldName":"",
                                   "Value":"",
                                   "ConfidenceLevel":100,
                                   "Coordinate":""
                                }
                             ]
                          }
                       ],
                       "ResultCode":0,
                       "ResultMessage":""
                }
        """
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + self.accesstoken
        }

        jsonDoc = {}

        while(timeoutinseconds > 0):
            timeoutinseconds -= 5

            if(timeoutinseconds < 0):
                raise Exception("Sorry, data is not available")

            try:
                response = requests.request("GET",
                                            "https://api.capturefast.com/api/Download/Data?documentId=" + str(documentid),
                                            headers=headers)
            except Exception as ex:
                raise Exception("Capturefast Communication Error")

            jsonDoc = response.json()

            resultCode = jsonDoc['ResultCode']

            if(resultCode == 0):
                break
            elif(resultCode == 100):
                continue
            else:
                time.sleep(5)
                jsonDoc = self.GetDocumentData(documentId, timeoutinseconds)
                break

        return jsonDoc


class CaptureFast(CaptureFastBase):
    """CaptureFast is an online document capture application.

    With the application, you can extract data from your documents and transfer
    your digitalized data to the desired environment for processing.

    To use the library, you can first create a user and create your document types by watching the video at https://www.youtube.com/watch?v=AMfOZBkK-M4.

    Args:
        username(str):      The username you create on Capturefast.
        password(str):      The password you create on Capturefast.
        teamid(str):        The team you create on Capturefast.

    Returns:

    Automatic token will be created from Capturefast, and you can send and receive your documents for capture using the UploadDocument and GetDocumentData methods.
    """
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_DOC_FORMAT = "REST"

    def __init__(self, username: str = None, password: str = None, teamid: str = None):
        self.cfusername = username
        self.cfpassword = password
        self.teamid = teamid
        self._init_client()




