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

    def UploadDocument(self, filePath, documentTypeId):
        fileContent = ''
        with open(filePath, "rb") as f:
            fileContent = base64.b64encode(f.read()).decode('ascii')

        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + self.accesstoken
        }

        document = {
            'TeamId':  self.teamid,
            'DocumentTypeId': documentTypeId,
            'Files': [{'FileName': os.path.basename(filePath),
                       'Content': fileContent}]
        }
        try:
            response = requests.request("POST",
                                        "https://api.capturefast.com/api/Upload/Document",
                                        headers=headers,
                                        data=json.dumps(document))

            if(response.json().get('ResultCode') != 0):
                raise Exception(response.json().get('ResultMessage'))

            return response.json().get('DocumentId')
        except:
            raise Exception("Capturefast Communication Error")

    def GetDocumentData(self, documentId, timeoutInSeconds=100):
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + self.accesstoken
        }

        jsonDoc = {}

        while(timeoutInSeconds > 0):
            timeoutInSeconds -= 5

            if(timeoutInSeconds < 0):
                raise Exception("Sorry, data is not available")
            try:
                response = requests.request("GET",
                                            "https://api.capturefast.com/api/Download/Data?documentId=" + str(documentId),
                                            headers=headers)
            except:
                raise Exception("Capturefast Communication Error")

            jsonDoc = response.json()

            resultCode = jsonDoc['ResultCode']

            if(resultCode == 0):
                break
            elif(resultCode == 100):
                continue
            else:
                time.sleep(5)
                jsonDoc = self.GetDocumentData(documentId, timeoutInSeconds)
                break

        return jsonDoc


class CaptureFast(CaptureFastBase):
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_DOC_FORMAT = "REST"

    def __init__(self, username: str = None, password: str = None, teamid: str = None):
        self.cfusername = username
        self.cfpassword = password
        self.teamid = teamid
        self._init_client()




