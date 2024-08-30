# This script is used to separate the Dataverse API methods from our main Jupyter notebook code to simplify the code that users see
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("package-name")
except PackageNotFoundError:
    # package is not installed
    pass

# @title Here we create a main working object (DvMod) so our configuration and database connections can more easily integrate. Also separating the code from the notebooks makes the notebook easier to read and manage.
import curlify
import json
import logging
import requests
import io
import hashlib
import os

# @title By placing all of our Python function within a class object, it makes it much easier for information to be used across functions without needing to explicitly passing them into each function (instead we pass the entire Worker object into the functions so each function can do what it needs with the object)
class ObjDvApi:
    # @param objConfig (we initialize this object with our notebook configuration)
    def __init__(self,objConfig):
        self.eventLogger()
        self.objConfig = objConfig
        self.strDATAVERSE_PARENT_COLLECTION = self.objConfig["strDvApi_PARENT_COLLECTION"]
        self.strDATAVERSE_DOMAIN = self.objConfig["strDvApi_DOMAIN"]
        self.strDATAVERSE_API_TOKEN = self.objConfig["strDvApi_TOKEN"]
        self.logger.info("Finished ObjDvApi init")


    # @title We will pull the logging settings from our Worker class so there is no need to add them in this script
    def eventLogger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel('INFO')
        
    
    # @title Create a new Dataverse collection (which is the same thing as creating a new Dataverse)
    def createCollection(self):
        self.logger.info("start createCollection")
        strApiEndpoint = '%s/api/dataverses/%s' % (self.strDATAVERSE_DOMAIN, self.strDATAVERSE_PARENT_COLLECTION)
        self.logger.info('making request: %s' % strApiEndpoint)
        objHeaders = {
            "Content-Type": "application/json",
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        r = requests.request("POST", strApiEndpoint, json=self.objConfig["objDvApi_COLLECTION_START"], headers=objHeaders) # it is nice I can simply send the JSON object without the need to create a separate JSON file
        self.printResponseInfo(r)
        self.logger.info("end createCollection")
        

    # @title View a new Dataverse collection based on the collection alias
    def viewCollection(self):
        self.logger.info("start viewCollection")
        strApiEndpoint = '%s/api/dataverses/%s' % (self.strDATAVERSE_DOMAIN, self.objConfig["objDvApi_COLLECTION_START"]["alias"])
        self.logger.info('making request: %s' % strApiEndpoint)
        objHeaders = {
            "Content-Type": "application/json",
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        r = requests.request("GET", strApiEndpoint, headers=objHeaders)
        self.printResponseInfo(r)
        self.logger.info("end viewCollection")
        

    # @title Delete a new Dataverse collection based on the collection alias
    def deleteCollection(self):
        self.logger.info("start deleteCollection")
        strApiEndpoint = '%s/api/dataverses/%s' % (self.strDATAVERSE_DOMAIN, self.objConfig["objDvApi_COLLECTION_START"]["alias"])
        self.logger.info('making request: %s' % strApiEndpoint)
        objHeaders = {
            "Content-Type": "application/json",
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        r = requests.request("DELETE", strApiEndpoint, headers=objHeaders)
        self.printResponseInfo(r)
        self.logger.info("end deleteCollection")
        

    # @title Get Dataverse collection contents based on the collection alias
    def getCollectionContents(self):
        self.logger.info("start getCollectionContents")
        strApiEndpoint = '%s/api/dataverses/%s/contents' % (self.strDATAVERSE_DOMAIN, self.objConfig["objDvApi_COLLECTION_START"]["alias"])
        self.logger.info('making request: %s' % strApiEndpoint)
        objHeaders = {
            "Content-Type": "application/json",
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        r = requests.request("GET", strApiEndpoint, headers=objHeaders)
        self.logger.info("end getCollectionContents")
        return r
        
        
    # @title List Dataverse collection contents based on the collection alias
    def viewCollectionContents(self):
        self.logger.info("start viewCollectionContents")
        r = self.getCollectionContents()
        self.printResponseInfo(r)
        self.logger.info("end viewCollectionContents")

    
    # @title Create a new dataset
    def createDataset(self):
        self.logger.info("start createDataset")
        strApiEndpoint = '%s/api/dataverses/%s/datasets' % (self.strDATAVERSE_DOMAIN, self.objConfig["objDvApi_COLLECTION_START"]["alias"])
        self.logger.info('making request: %s' % strApiEndpoint)
        objHeaders = {
            "Content-Type": "application/json",
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        r = requests.request("POST", strApiEndpoint, json=self.objConfig["objDvApi_DATASET_INIT"], headers=objHeaders)  # creates a dataset using the information from our objDvApi_DATASET_INIT configuration object
        self.printResponseInfo(r)
        return r
        self.logger.info("end createDataset")


    # @title Delete a dataset draft
    def deleteDatasetDraft(self, strDatasetId):
        self.logger.info("start deleteDatasetDraft")
        strApiEndpoint = '%s/api/datasets/%s/versions/:draft' % (self.strDATAVERSE_DOMAIN, strDatasetId)
        self.logger.info('making request: %s' % strApiEndpoint)
        objHeaders = {
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        r = requests.request("DELETE", strApiEndpoint, headers=objHeaders)
        self.printResponseInfo(r)
        self.logger.info("end deleteDatasetDraft")

    
    # @title Get dataset file details
    def getDatasetFiles(self, strDatasetId, strVersion):
        self.logger.info("start viewDatasetFiles")
        strApiEndpoint = '%s/api/datasets/%s/versions/%s/files' % (self.strDATAVERSE_DOMAIN, strDatasetId, strVersion)
        self.logger.info('making request: %s' % strApiEndpoint)
        objHeaders = {
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        r = requests.request("GET", strApiEndpoint, headers=objHeaders)
        self.printResponseInfo(r)
        if (r.status_code!=200):
            raise RuntimeError("***ERROR: The dataset information could not be retrieved***")
        self.logger.info("end viewDatasetFiles")
        return r


    # @title Publish a dataset draft
    def publishDatasetDraft(self, objDatasetMeta, strType):
        self.logger.info("start publishDatasetDraft")
        # first we will check if our collection is published
        r = self.getCollectionContents()
        blnCollectionNotPublished = True
        if "json" in dir(r):
            jsonR = r.json()
            for objDataset in jsonR["data"]:
                if "publicationDate" in objDataset:
                    blnCollectionNotPublished = False # the cllectiong seems to published
                    
        # ========= publish the collection if needed
        if blnCollectionNotPublished:
            strApiEndpoint = '%s/api/dataverses/%s/actions/:publish' % (self.strDATAVERSE_DOMAIN, objDatasetMeta["dv_alias"])
            self.logger.info('making request: %s' % strApiEndpoint)
            objHeaders = {
                "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
            }
            r = requests.request("POST", strApiEndpoint, headers=objHeaders)
            self.printResponseInfo(r)
            self.logger.info(curlify.to_curl(r.request))
            if (r.status_code!=200):
                raise RuntimeError("***ERROR: The Dataverse collection could not be published***")
        # ========= end publishing the collection if needed

        # ========= publish the dataset
        strApiEndpoint = '%s/api/datasets/:persistentId/actions/:publish?persistentId=%s&type=%s' % (self.strDATAVERSE_DOMAIN, objDatasetMeta["strDvUrlPersistentId"], strType)
        self.logger.info('making request: %s' % strApiEndpoint)
        objHeaders = {
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        r = requests.request("POST", strApiEndpoint, headers=objHeaders)
        self.printResponseInfo(r)
        self.logger.info(curlify.to_curl(r.request))
        self.logger.info("end publishDatasetDraft")
        if (r.status_code!=200):
            raise RuntimeError("***ERROR: The dataset could not be published***")


    # @title Request the dataset contents from the Dataverse so we can compare with what we have locally
    def getDvDatasetContents(self,objFile):
        # use the requests module from Python to make a simple request to the Dataverse to check the contents
        url = self.strDATAVERSE_DOMAIN+"/api/datasets/:persistentId/versions/:latest?persistentId="+objFile["strDvUrlPersistentId"]
        headers = {
            "Content-Type": "application/json",
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        r = requests.request("GET", url, headers=headers)
        if "json" in dir(r):
            self.dictDatasetContents = r.json()    # convert the response to a dict
        else:
            raise RuntimeError("***ERROR: Could not retrieve the dataset contents***")
        
    
    # @title Add a new file to a dataset (or replace an existing one)
    # @arguments objFile=JSON object defining the file for upload
    def addDatasetFile(self, objFile):
        self.getDvDatasetContents(objFile)
        objFileReturn = self.checkFileForUpload(objFile["strFileName"], os.path.join(objFile["strUploadPath"],objFile["strFileName"]))  # check that we are ready for upload
        self.logger.info(objFileReturn)
        # --------------------------------------------------
        # Using a "jsonData" parameter, add optional description + file tags
        # --------------------------------------------------
        params = dict(description=objFile["strDataDescription"],
                    directoryLabel=objFile["strDirectoryLabel"],
                    fileName=objFile["strFileName"],
                    categories=objFile["lstCatgories"])
        self.logger.info("addDatasetFile: "+objFile["strFileName"]+" "+str(params))
        params_as_json_string = json.dumps(params)
        payload = dict(jsonData=params_as_json_string)
        if (objFileReturn["blnFileExists"]==False): # if the file does not already exist in the dataset we upload it using the 'add' API endpoint
            strApiEndpoint = '%s/api/datasets/:persistentId/add?persistentId=%s' % (self.strDATAVERSE_DOMAIN, objFile["strDvUrlPersistentId"])
            # self.logger.info(objFile)
        elif (objFileReturn["blnMd5Match"]==True): # we want to update the file metadata
            strApiEndpoint = '%s/api/files/%s/metadata' % (self.strDATAVERSE_DOMAIN, objFileReturn["dataFile"]["id"])
        else:  # we have an existing file and the MD5 checksum does not match, we need to replace the file
            strApiEndpoint = '%s/api/files/%s/replace' % (self.strDATAVERSE_DOMAIN, objFileReturn["dataFile"]["id"])

        fileobj = open(os.path.join(objFile["strUploadPath"],objFile["strFileName"]), 'rb')  # read the file
        objFilePost = {'file': (objFile["strFileName"], fileobj)}   # we have the new file object to save to the Dataverse
        objHeaders = {
            "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        }
        self.logger.info('making request: %s' % strApiEndpoint)
        if (objFileReturn["blnMd5Match"]==True and objFileReturn["blnFileExists"]==True): # we handle a metadata only update differently
            objfileData = {'jsonData': (None, params_as_json_string)}  # we have to set up the metadata as file data for this API endpoint
            r = requests.request("POST", strApiEndpoint, files=objfileData, headers=objHeaders)
        else: # update or add new file
            r = requests.request("POST", strApiEndpoint, data=payload, files=objFilePost, headers=objHeaders)
        self.logger.info(curlify.to_curl(r.request))
        self.printResponseInfo(r)
        self.logger.info("--end uploadFileToDv--")


    # @title Delete files we no longer want to use in a new version of the dataset
    # @arguments strNewFileList="the list name in the configuration to use for defining the files we want in the dataset"
    def removeUnusedFiles(self, strNewFileList):
        self.logger.info("start removeUnusedFiles")
        # compare the files we want with the files currently in the dataset draft and remove the old files we no longer need
        print(strNewFileList)
        self.getDatasetFiles()
        # self.removeFile()
        self.logger.info("end removeUnusedFiles")

    
    # @title Delete a draft file (using SWORD API https://guides.dataverse.org/en/5.13/api/sword.html#delete-a-file-by-database-id)
    def removeFile(self, strFileId):
        self.logger.info("start removeFile")
        strApiEndpoint = '%s/dvn/api/data-deposit/v1.1/swordv2/edit-media/file/%s' % (self.strDATAVERSE_DOMAIN, strFileId)
        # strApiEndpoint = '%s/api/files/%s' % (self.strDATAVERSE_DOMAIN, strFileId)  # this does not work in v5.13
        self.logger.info('making request: %s' % strApiEndpoint)
        # objHeaders = {
        #     "X-Dataverse-Key": self.strDATAVERSE_API_TOKEN
        # }
        r = requests.request("DELETE", strApiEndpoint, auth=(self.strDATAVERSE_API_TOKEN, ''))
        self.logger.info(curlify.to_curl(r.request))
        # r = requests.request("DELETE", strApiEndpoint, headers=objHeaders) # this is for the Native API
        self.printResponseInfo(r)
        if (r.status_code!=204):
            raise RuntimeError("***ERROR: The file could not be deleted***")
        self.logger.info("end removeFile")
        
        
    # @title General purpose method for printing response properties for testing
    # @argument r=response object from a requests.request()
    def printResponseInfo(self,r):
        self.logger.info('-' * 40) # simple delineation so we know when this method is called in our output 
        self.logger.info("response status="+str(r.status_code))
        self.logger.info("headers="+str(r.headers))
        if "json" in dir(r):  # if we have response JSON function then log it
            self.logger.info("json="+str(r.json()))
        

    # @title Check that we have changes to a file before we try uploading to the Dataverse
    # @param File name, a description we will use to describe the file in the Dataverse
    # @return objFileReturn (existing file object)
    def checkFileForUpload(self, strFileName, strFilePath):
        # check for an existing file in the Dataverse
        objFileReturn={"blnFileExists":False, "blnMd5Match":True}  # assumptions for our files
        strExistingMd5=''
        # self.logger.info(len(self.dictDatasetContents['data']['files']))
        for dvFile in self.dictDatasetContents['data']['files']: # loop through the files in the dataset to find the one we want to replace
            strExistingMd5 = dvFile['dataFile']['md5']
            if 'originalFileName' in dvFile['dataFile']:    # NOTE: some files are unique in the Dataverse in that they are not labeled the same way due to the original format switched to tab delimited format, so we need to check for an `originalFileName` element
                if (dvFile['dataFile']['originalFileName']==strFileName):
                    objFileReturn=dvFile
                    objFileReturn["blnFileExists"]=True
                    break
            else:
                if (dvFile['label']==strFileName):     # check files other than files converted to tab delimited in the Dataverse
                    objFileReturn=dvFile
                    objFileReturn["blnFileExists"]=True
                    break
        if (objFileReturn["blnFileExists"]==True): # if the file we are wanting to upload currently exists in the the Dataverse dataset, we check the MD5 checksum of both files and only upload if the MD5 differs
            newFileMd5 = self.md5(strFilePath)
            self.logger.info("MD5 are local "+newFileMd5+" and dataset "+strExistingMd5)
            if (newFileMd5==strExistingMd5):
                self.logger.info("MD5 hashes match on "+strFileName+" so do not upload new file")
                self.blnUploadFile=False
                objFileReturn["blnMd5Match"] = True
            else:
                self.logger.info("Something has changed with the file so we can upload a new version of the file to the Dataverse"+newFileMd5+"=="+strExistingMd5)
                objFileReturn["blnMd5Match"] = False
        return objFileReturn


    # @title Generates an MD5 hash for a given file (used to check against files being uploaded to prevent duplicate file uploads)
    # @argument Path to file being checked
    def md5(self, fileToCheck):
        hash_md5 = hashlib.md5()
        with open(fileToCheck, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
