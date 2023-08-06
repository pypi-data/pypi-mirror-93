from msrest.exceptions import HttpOperationError
from commontoolsaiopslibs.utils import FileUtilities, ConfigGenerator
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import yaml
import ntpath
import os
from os.path import isfile, join
from PIL import Image, ImageOps
from io import BytesIO
import numpy as np
import random
import string
import urllib
import urllib.request
import base64
import shutil
import tempfile
import json
import traceback
import sys
from datetime import datetime
import requests
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse
from mimetypes import guess_extension, guess_type

class BlobStorageHandler(object):
    def __init__(self, connection_string):
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    def upload(self, blob_container, file_path, overwrite = False):
        file_name = ntpath.basename(file_path)
        print("file_name :",file_name)
        blob_client=self.blob_service_client.get_blob_client(container=blob_container,blob=file_name)
        with open(file_path,"rb") as data:
            blob_client.upload_blob(data, overwrite=overwrite)
    
    def delete(self,blob_container,  file_path):
        """deletes the file from the blob storage

        Arguments:
            blob_container {str} -- container (or folder) in blob storage 
            file_path {str} -- [description]
        """

        if os.path.isabs(file_path):
            file_name = ntpath.basename(file_path)
        else:
            file_name = file_path
        # Create a blob client using the local file name as the name for the blob
        blob_client = self.blob_service_client.get_blob_client(container=blob_container, blob=file_name)

        print("\Deleting from Azure Storage:\n\t" + file_name)

        # Upload the created file
        blob_client.delete_blob()
    
    def download_json_by_url(self, file_path):
        data = {}
        try:
            response = urllib.request.urlopen(file_path)
            data = json.loads(response.read())
        except HTTPError as e:
            # do something
            print('Error code: ', e.code)
        except URLError as e:
            # do something
            print('Reason: ', e.reason)

        return data
    
    def download_text_by_url(self, file_path):
        """download the file from the http link

        Arguments:
            file_path {str} -- http link

        Returns:
            str -- downloaded file content
        """
        data = None
        try:
            response = urllib.request.urlopen(file_path)
            data = response.read().decode('utf-8')
        except HTTPError as e:
            # do something
            print('Error code: ', e.code)
        except URLError as e:
            # do something
            print('Reason: ', e.reason)
        except Exception as e:
            # do something
            print('Reason: ', e)

        return data

class ImagePathListUploader(object):
    def __init__(self, blob_manager, host):
        self.blob_manager = blob_manager
        self.host = host
    
    def upload(self,files_source, blob_container_dest):
        for file_source in files_source:
            file_source_name = ntpath.basename(file_source)
            self.blob_manager.upload(blob_container_dest, file_source, overwrite = True)
            uploaded_image = "{0}/{1}/{2}".format(self.host, blob_container_dest, file_source_name)
            print("uploaded_image :", uploaded_image)

class SampedDataDataManager:
    def __init__(self, blob_manager, host, container_name,env_dir):
        self.blob_manager = blob_manager
        self.container_name = container_name
        self.env_dir = env_dir
        self.host = host
        self.sampled_data_file = "sampled_data.json"
        self.sampled_data_url = "{0}/{1}/{2}/ml_data/sampled_data/current/{3}".format(self.host,self.container_name,self.env_dir,self.sampled_data_file)
        self.ARCHIVE_SAMPLED_PATH = "{0}/{1}/ml_data/sampled_data/archive".format(self.container_name, self.env_dir)
        self.CURRENT_SAMPLED_PATH = "{0}/{1}/ml_data/sampled_data/current".format(self.container_name, self.env_dir)

    def _get_http_sampled_data(self, sampled_data):
        items = []
        for item in sampled_data:
            print("item[0]", item[0])
            print("item[1]", item[1])
            image_name = os.path.basename(item[0])
            url_file =  "{0}/{1}/{2}/ml_data/unlabeled/data/{3}".format(self.host, self.container_name, self.env_dir, image_name)
            items.append(url_file)
        return items

    def upload_data(self, sampled_data):
        sampled_data = self._get_http_sampled_data(sampled_data)
        with tempfile.TemporaryDirectory() as dir:
            sampled_data_file = os.path.join(dir,'sampled_data.json')
            with open(sampled_data_file, 'w') as outfile:
                json.dump(sampled_data, outfile)
            #blob_container = "{0}/ml_data/sampled_data/current".format(container_name)
            self.blob_manager.upload(self.CURRENT_SAMPLED_PATH, sampled_data_file, overwrite = True)
            print("file {0} uploaded".format(sampled_data_file))
    
    def get_sampled_data(self):
        data = []
        try:
            with tempfile.TemporaryDirectory() as dir:
                file_path = os.path.join(dir, self.sampled_data_file)
                r = requests.get(self.sampled_data_url, allow_redirects=True)
                open(file_path, "wb").write(r.content)
                with open(file_path) as f:
                    data = json.load(f)
        except Exception as e:
            print(e)
        
        return data
    
    def archive(self):
        try:
            with tempfile.TemporaryDirectory() as dir:
                sampled_data_path = os.path.join(dir, self.sampled_data_file)
                r = requests.get(self.sampled_data_url, allow_redirects=True)
                open(sampled_data_path, "wb").write(r.content)
                archive_name = "sampled_data_{0}{1}".format(datetime.now().strftime("%m_%d_%Y_%H_%M_%S"),".json")
                archived_file = os.path.join(dir, archive_name)
                #copy sampled file as archived file
                shutil.copyfile(sampled_data_path, archived_file)
                #upload sampled file to blob
                self.blob_manager.upload(self.ARCHIVE_SAMPLED_PATH, archived_file)
                #upload sampled file to blob
                self.blob_manager.delete(self.CURRENT_SAMPLED_PATH, sampled_data_path)
                #delete sampled file
                os.remove(archived_file)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            print(sys.exc_info()[2])
   
class AnnotatedDataManager:
    def __init__(self, blob_manager, host, container_name, env_dir):
        self.blob_manager = blob_manager
        self.host = host
        self.env_dir = env_dir
        self.container_name = container_name
        self.annotated_data_file = "annotated_data.json"
        self.annotated_data_url = "{0}/{1}/{2}/ml_data/annotated_data/current/{3}".format(self.host,self.container_name,self.env_dir,self.annotated_data_file)
        self.ARCHIVE_ANNOTATED_PATH = "{0}/{1}/ml_data/annotated_data/archive".format(self.container_name, self.env_dir)
        self.CURRENT_ANNOTATED_PATH = "{0}/{1}/ml_data/annotated_data/current".format(self.container_name, self.env_dir)
    
    def upload_data(self, annotated_data):
        with tempfile.TemporaryDirectory() as dir:
            annotated_data_file = os.path.join(dir,'annotated_data.json')
            with open(annotated_data_file, 'w') as outfile:
                json.dump(annotated_data, outfile)
            #blob_container = "{0}/ml_data/annotated_data/current".format(self.container_name)
            self.blob_manager.upload(self.CURRENT_ANNOTATED_PATH, annotated_data_file, overwrite = True)
            print("file {0} uploaded".format(annotated_data_file))

    def archive(self, working_dir):
        try:
            print("step 1")
            annotated_data_path = os.path.join(working_dir, self.annotated_data_file)
            r = requests.get(self.annotated_data_url, allow_redirects=True)
            open(annotated_data_path, "wb").write(r.content)
            print("step 2")
            archive_name = "annotated_data_{0}{1}".format(datetime.now().strftime("%m_%d_%Y_%H_%M_%S"),".json")
            archived_file = os.path.join(working_dir, archive_name)
            #copy sampled file as archived file
            shutil.copyfile(annotated_data_path, archived_file)
            print("step 3")
            #upload sampled file to blob
            self.blob_manager.upload(self.ARCHIVE_ANNOTATED_PATH, archived_file)
            #upload sampled file to blob
            self.blob_manager.delete(self.CURRENT_ANNOTATED_PATH, annotated_data_path)
            #delete sampled file
            os.remove(archived_file)
            print("step 4")
        except Exception as e:
            print(traceback.format_exc())
            print(sys.exc_info()[2])
            raise Exception(e)

class ConfigProvider:
    def __init__(self, config_path):
        self.config_path = config_path

    def _load_data(self):
        with open(self.config_path) as stream:
            data = yaml.safe_load(stream)
        return data
    
    def load(self):
        data = self._load_data()

        #AmlComputes
        self.AML_COMPUTE_BM_CLUSTER_NAME = data["Azure"]["AmlComputes"]["Benchmark"]["ClusterName"]
        self.AML_COMPUTE_BM_CLUSTER_VM_TYPE = data["Azure"]["AmlComputes"]["Benchmark"]["ClusterType"]
        self.AML_COMPUTE_PREP_CLUSTER_NAME = data["Azure"]["AmlComputes"]["DataPreparation"]["ClusterName"]
        self.AML_COMPUTE_PREP_CLUSTER_VM_TYPE = data["Azure"]["AmlComputes"]["DataPreparation"]["ClusterType"]
        self.AML_COMPUTE_DS_CLUSTER_NAME = data["Azure"]["AmlComputes"]["DataScience"]["ClusterName"]
        self.AML_COMPUTE_DS_CLUSTER_VM_TYPE = data["Azure"]["AmlComputes"]["DataScience"]["ClusterType"]
        self.AML_COMPUTE_SAMPLING_CLUSTER_NAME = data["Azure"]["AmlComputes"]["Sampling"]["ClusterName"]
        self.AML_COMPUTE_SAMPLING_CLUSTER_VM_TYPE = data["Azure"]["AmlComputes"]["Sampling"]["ClusterType"]

        self.AML_COMPUTE_CLUSTER_MIN_NODES = data["Azure"]["AmlComputes"]["ClusterMinNode"]
        self.AML_COMPUTE_CLUSTER_MAX_NODES = data["Azure"]["AmlComputes"]["ClusterMaxNode"]
        self.IDLE_SECONDS_BEFORE_SCALEDOWN = data["Azure"]["AmlComputes"]["IdleSecondes_Before_Scaledown"]

        #StorageAccount
        self.BLOB_DATASTORE_NAME = data["Azure"]["StorageAccount"]["BlobDatastoreName"]
        self.ACCOUNT_NAME = data["Azure"]["StorageAccount"]["AccountName"]
        self.CONTAINER_NAME = data["Azure"]["StorageAccount"]["ContainerName"]
        self.ENV_DIR = data["Azure"]["StorageAccount"]["EnvDir"]
        self.ACCOUNT_KEY = data["Azure"]["StorageAccount"]["AccountKey"]
        self.BLOB_STORAGE_CONNECTION_STRING = data["Azure"]["StorageAccount"]["BlobStorageConnectionString"]
        self.SERVICE_BLOB = data["Azure"]["StorageAccount"]["ServiceBlob"]
        #Azureml
        self.LOCATION = data["Azure"]["Azureml"]["Location"]
        self.RESOURCEGROUP = data["Azure"]["Azureml"]["ResourceGroup"]
        self.WORKSPACENAME = data["Azure"]["Azureml"]["WorkspaceName"]


        #ExperimentName
        self.EXPERIMENT_BM_NAME = data["Azure"]["Azureml"]["Experiments"]["Benchmark"]["Name"]
        self.EXPERIMENT_PREP_NAME = data["Azure"]["Azureml"]["Experiments"]["DataPreparation"]["Name"]
        self.EXPERIMENT_DS_NAME = data["Azure"]["Azureml"]["Experiments"]["DataScience"]["Name"]
        self.EXPERIMENT_SAMPLING_NAME = data["Azure"]["Azureml"]["Experiments"]["Sampling"]["Name"]
        
        #self.PIPELINE_NAME = data["Azure"]["Azureml"]["Pipeline"]["Name"]
        self.PIPELINE_BM_NAME = data["Azure"]["Azureml"]["Pipelines"]["Benchmark"]["Name"]
        self.PIPELINE_BM_ENDPOINT = data["Azure"]["Azureml"]["Pipelines"]["Benchmark"]["EndPoint"]
        self.PIPELINE_PREP_NAME = data["Azure"]["Azureml"]["Pipelines"]["DataPreparation"]["Name"]
        self.PIPELINE_PREP_ENDPOINT = data["Azure"]["Azureml"]["Pipelines"]["DataPreparation"]["EndPoint"]
        self.PIPELINE_DS_NAME = data["Azure"]["Azureml"]["Pipelines"]["DataScience"]["Name"]
        self.PIPELINE_DS_ENDPOINT = data["Azure"]["Azureml"]["Pipelines"]["DataScience"]["EndPoint"]
        self.PIPELINE_SAMPLING_NAME = data["Azure"]["Azureml"]["Pipelines"]["Sampling"]["Name"]
        self.PIPELINE_SAMPLING_ENDPOINT = data["Azure"]["Azureml"]["Pipelines"]["Sampling"]["EndPoint"]
        #Model
        self.MODEL_NAME = data["Azure"]["Azureml"]["Model"]["Name"]
        #Deploy
        self.DEPLOY_SERVICE_NAME = data["Azure"]["Azureml"]["Deploy"]["ServiceName"]
        self.DEPLOY_THRESHOLD =  data["Azure"]["Azureml"]["Deploy"]["ModelThreshold"]

        #ServicePrincipalAuthentication
        self.SPA_TENANTID = data["Azure"]["ServicePrincipalAuthentication"]["TenantId"]
        self.SPA_APPLICATIONID = data["Azure"]["ServicePrincipalAuthentication"]["ApplicationId"]
        self.SPA_PASSWORD = data["Azure"]["ServicePrincipalAuthentication"]["Password"]

        #Subscriptions
        self.SUBSCRIPTION_VALUE = data["Azure"]["Subscriptions"]["Value"]

class ConfigHandler:
    def get_file(self,config_path):
        """Loading config object to be used in the entire program

        Arguments:
            config_path {str} -- generated config file path

        Returns:
            ConfigProvider -- Object containing all the information in the config file
        """
        config = ConfigProvider(config_path)
        config.load()
        return config

    def generate(self, config_template, config_path):
        configGen = ConfigGenerator(config_template)

        # If it run locally, then we're going to use the config.values.txt 
        # file containing all the necessary information
        if len(sys.argv) == 1:
            configGen.by_file("../../config.values.txt",config_path)
        # If it's launched via DevOps, then the values will be pass as params
        else:
            configGen.by_args(sys.argv, config_path)
