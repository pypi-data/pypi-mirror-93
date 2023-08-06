import csv
import pickle
from commontoolsaiopslibs.utils import FileUtilities, ConfigGenerator
import os
import pandas as pd
import ntpath
import requests
import json
import torch
import asyncio
import urllib, json
import urllib.request
from urllib.error import URLError, HTTPError
from os import listdir
from os.path import isfile, join
import shutil
import yaml
import sys
import numpy as np
import joblib
from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
import seaborn as sns
import matplotlib.pyplot as plt
import yaml
import uuid
import string
import random
import threading
from threading import Thread
import glob
import re
import logging
import time
import xml.etree.ElementTree as ET
from functools import wraps
sns.set(color_codes=True)

class CsvUtilities:

    @staticmethod
    def to_dict_by_id(unlabeled_data):
        result = {}
        for item in unlabeled_data:
            result[item[0]] = item
        return result
    
    @staticmethod
    def load_data(filepath,already_labeled = {}, skip_already_labeled=False):
        # csv format: [ID, TEXT, LABEL, SAMPLING_STRATEGY, CONFIDENCE]
        if  not filepath:
            raise Exception("filepath param mus be provided")

        with open(filepath, 'r') as csvfile:
            data = []
            reader = csv.reader(csvfile)
            for row in reader:
                
                if len(row) == 0:
                    continue

                # Create the five columns for the observations that are not already
                # labeled. Because those labeled, already contain the 5 columns
                if skip_already_labeled and row[0] in already_labeled:
                    continue
                    
                if len(row) < 3:
                    row.append("") # add empty col for LABEL to add later
                if len(row) < 4:
                    row.append("") # add empty col for SAMPLING_STRATEGY to add later        
                if len(row) < 5:
                    row.append(0) # add empty col for CONFIDENCE to add later         
                data.append(row)

                # Add to the list already labeled those observations already labeled
                # when loading the script.
                # For saving logs.
                label = str(row[2])
                if row[2] != "":
                    textid = row[0]
                    already_labeled[textid] = label

        csvfile.close()
        return data
    
    # allows add data to csv file
    @staticmethod
    def append_data(filepath, data):
        with open(filepath, 'a', errors='replace') as csvfile:
            for list in data:
                csvfile.write(str(list).replace("['","").replace("', '",",").replace("', ",",").replace("']","").replace("]","")+"\n")
                    
            #writer = csv.writer(csvfile)
            #writer.writerows(data)
        csvfile.close()
    
    # Used to write a csv when it has not yet been initialized?
    @staticmethod
    def write_data(filepath, data):
        with open(filepath, 'w', errors='replace') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
        csvfile.close()

    @staticmethod
    def transform_to_local_format(data):

        temp_name = "temp_file_" + time.strftime("%Y%m%d-%H%M%S") + ".csv"

        if isinstance(data, pd.DataFrame):
            data.to_csv(temp_name, header=False)
        else:
            FileUtilities.create_file_with_content(temp_name, data)

        #load data in local format
        result = CsvUtilities.load_data(temp_name)

        #delete temp file
        os.remove(temp_name)
        
        return result
      
class FileNameProvider:

    @staticmethod
    def get_features_index_file(model_path):
        return os.path.join(model_path,"features_index.pickle")
    
    @staticmethod
    def get_model_candidate_name(model_path):
        return os.path.join(model_path, "outputs/model_candidate.mdl")
    
    @staticmethod
    def get_model_to_publish_name(model_path):
        return os.path.join(model_path, "outputs/model_to_publish.mdl")

    @staticmethod
    def get_model_to_be_validated_name(model_path):
        return os.path.join(model_path, "outputs/model_to_be_validated.mdl")
    
    @staticmethod
    def get_validated_model_name(model_path):
        return os.path.join(model_path, "outputs/validated_model.mdl")

    @staticmethod
    def get_outputs_folder(model_path):
        return os.path.join(model_path, "outputs")

class DataTransformer:
    @staticmethod
    def arr_to_dataframe(array, cols, index_col):
        """Transformation of an array to a dataframe

        Arguments:
            array {array} -- array containing the data to be transformed
            cols {array} -- names of the columns that must be in the dataframe
            index_col {str} -- column that will represent the dataframe index

        Returns:
            DataFrame -- pandas's dataframe contain data
        """
        arr = np.array(array)
        
        df = pd.DataFrame(data=arr, columns=cols)
        df = df.set_index(index_col)
        return df

class FeaturesHandler:
    """
    FeaturesHandler's role is to create a large dictionary containing 
    the words and their number of occurrences (Bag-of-words). 
    It is this dictionary that we will use as features. 
    """
    def create_features(self,unlabeled_data, minword = 3):
        """This method allows to create the Bag-of-words which will be used as Features
        
            Arguments:
                unlabeled_data {str} -- variable that contains unlabeled data
                minword {int} -- minimum number of occurrences per word of bag-of-words
            
            returns:
                feature_index {int} -- variable that contains Bag-of-words for all data (unlabeled + traning)
        """
        feature_index = {}

        if (unlabeled_data is None) | (unlabeled_data is "") :
            raise Exception("unlabeled data cannot be empty") 

        total_training_words = {}
        for item in unlabeled_data:
            text = item[1]
            for word in text.split():
                if word not in total_training_words:
                    total_training_words[word] = 1
                else:
                    total_training_words[word] += 1

        for item in unlabeled_data:
            text = item[1]
            for word in text.split():
                if word not in feature_index and total_training_words[word] >= minword:
                    feature_index[word] = len(feature_index)

        return feature_index
    
    def make_feature_vector(self, features, feature_index):
        """[summary]
            This method allows to create one-hot vector from list of words
        
            Arguments:
                features {str} -- list of words 
                feature_index {str} -- bag-of-words from all data (unlabeled + traning)
            
            returns:
                 {pytorch.view} -- one-hot vector
        """
        vec = torch.zeros(len(feature_index)) # pylint: disable=no-member 
        for feature in features:
            if feature in feature_index:
                vec[feature_index[feature]] += 1
        return vec.view(1, -1)

class DataCorresponder:
    def __init__(self, all_data_vec):
        self.all_data_vec = all_data_vec

    def get_vec_correspondence(self, data_text):
        if not data_text :
            raise Exception("data_text cannot be empty")
        
        X_all_data, _, id_all_data = self.all_data_vec
        X_data = []
        y_data = []
        id_data = []
        for item in data_text:
            id = int(item[0])
            if len(item) > 2:
                item[2] = item[2].replace(" '","")
                label = item[2]
            for feature_vec, x_id in zip(X_all_data,id_all_data):
                if id == x_id:
                    X_data.append(feature_vec)
                    y_data.append(label)
                    id_data.append(int(id))
                    break
        
        return X_data, y_data, id_data

class LazyDataCorresponder:
    def __init__(self, all_vec_data_path):
        self.all_vec_data_path = all_vec_data_path
    
    def get_vec_correspondence(self, data_text):
        if not data_text :
            raise Exception("data_text cannot be empty")

        X_data, y_data, id_data  = [], [], []
        with open(self.all_vec_data_path, 'rb') as pickle_file:
            try:
                while True:
                    result = pickle.load(pickle_file)
                    vec_result, target_result, id_result = result
                    id_result, target_result = id_result.decode("utf-8"), target_result.decode("utf-8")
                    for item in data_text:
                        id = item[0]
                        label = item[2]
                        if id == id_result:
                            X_data.append(vec_result)
                            y_data.append(label)
                            id_data.append(int(id))
                    vec, target, _id = result
            except EOFError:
                pass
        return X_data, y_data, id_data

class SplittedDataCorresponder:
    def __init__(self, all_vec_data_directory_path):
        self.all_vec_data_directory_path = all_vec_data_directory_path
    
    def get_vec_correspondence(self, data_text):
        if not data_text :
            raise Exception("data_text cannot be empty")

        X_data, y_data, id_data  = [], [], []
        for block_file in os.listdir(self.all_vec_data_directory_path):
            result = joblib.load(os.path.join(self.all_vec_data_directory_path, block_file))
            vec_result, _, id_result = result
            id_result = [item.decode("utf-8") for item in id_result]
            #print(id_result)
            #id_result, target_result = id_result.decode("utf-8"), target_result.decode("utf-8")
            for item in data_text:
                id = item[0]
                label = item[2]
                #print("{0} == {1}".format(id, id_result))
                #print("{0} == {1}".format(type(id), type(id_result)))
                if id in id_result:
                    X_data.append(vec_result)
                    y_data.append(label)
                    id_data.append(int(id))
            result = None #freed memory
        return X_data, y_data, id_data

class DataAdapter:
    def __init__(self):
        self.featuresHandler = FeaturesHandler()

    def adapt(self, data, features_index):
        if not data:
            raise Exception("data cannot be empty")

        if not features_index:
            raise Exception("features_index cannot be empty")

        X = [] #initialize X
        y = [] #initialize y (target)
        ids = [] #initialize id for identification

        for item in data:
            id = item[0]
            features = item[1].split()
            label = "_"
            if len(item) > 2:
                item[2] = item[2].replace(" '","")
                label = item[2]
            
            feature_vec = self.featuresHandler.make_feature_vector(features,features_index)
            X.append(feature_vec)
            y.append(label)
            ids.append(int(id))

        return X, y, ids

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
        self.AML_COMPUTE_VEC_CLUSTER_NAME = data["Azure"]["AmlComputes"]["Vectorization"]["ClusterName"]
        self.AML_COMPUTE_VEC_CLUSTER_VM_TYPE = data["Azure"]["AmlComputes"]["Vectorization"]["ClusterType"]
        self.AML_COMPUTE_DS_CLUSTER_NAME = data["Azure"]["AmlComputes"]["DataScience"]["ClusterName"]
        self.AML_COMPUTE_DS_CLUSTER_VM_TYPE = data["Azure"]["AmlComputes"]["DataScience"]["ClusterType"]
        self.AML_COMPUTE_SAMPLING_CLUSTER_NAME = data["Azure"]["AmlComputes"]["Sampling"]["ClusterName"]
        self.AML_COMPUTE_SAMPLING_DS_CLUSTER_VM_TYPE = data["Azure"]["AmlComputes"]["Sampling"]["ClusterType"]

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
        #Azureml
        self.LOCATION = data["Azure"]["Azureml"]["Location"]
        self.RESOURCEGROUP = data["Azure"]["Azureml"]["ResourceGroup"]
        self.WORKSPACENAME = data["Azure"]["Azureml"]["WorkspaceName"]


        #ExperimentName
        #self.EXPERIMENT_NAME = data["Azure"]["Azureml"]["Experiment"]["Name"]
        self.EXPERIMENT_VEC_NAME = data["Azure"]["Azureml"]["Experiments"]["Vectorization"]["Name"]
        self.EXPERIMENT_DS_NAME = data["Azure"]["Azureml"]["Experiments"]["DataScience"]["Name"]
        self.EXPERIMENT_SAMPLING_NAME = data["Azure"]["Azureml"]["Experiments"]["Sampling"]["Name"]
        
        #self.PIPELINE_NAME = data["Azure"]["Azureml"]["Pipeline"]["Name"]

        self.PIPELINE_VEC_NAME = data["Azure"]["Azureml"]["Pipelines"]["Vectorization"]["Name"]
        self.PIPELINE_VEC_ENDPOINT = data["Azure"]["Azureml"]["Pipelines"]["Vectorization"]["EndPoint"]
        self.PIPELINE_DS_NAME = data["Azure"]["Azureml"]["Pipelines"]["DataScience"]["Name"]
        self.PIPELINE_DS_ENDPOINT = data["Azure"]["Azureml"]["Pipelines"]["DataScience"]["EndPoint"]
        self.PIPELINE_SAMPLING_NAME = data["Azure"]["Azureml"]["Pipelines"]["Sampling"]["Name"]
        self.PIPELINE_SAMPLING_ENDPOINT = data["Azure"]["Azureml"]["Pipelines"]["Sampling"]["EndPoint"]
        #Model
        self.MODEL_NAME = data["Azure"]["Azureml"]["Model"]["Name"]
        self.SURROGATE_MODEL_NAME = data["Azure"]["Azureml"]["SurrogateModel"]["Name"]
        self.SURROGATE_VECTORIZER = data["Azure"]["Azureml"]["SurrogateModel"]["Vectorizer"]
        #Deploy
        self.DEPLOY_SERVICE_NAME = data["Azure"]["Azureml"]["Deploy"]["ServiceName"]
        self.DEPLOY_THRESHOLD =  data["Azure"]["Azureml"]["Deploy"]["ModelThreshold"]

        #ServicePrincipalAuthentication
        self.SPA_TENANTID = data["Azure"]["ServicePrincipalAuthentication"]["TenantId"]
        self.SPA_APPLICATIONID = data["Azure"]["ServicePrincipalAuthentication"]["ApplicationId"]
        self.SPA_PASSWORD = data["Azure"]["ServicePrincipalAuthentication"]["Password"]

        #Subscriptions
        self.SUBSCRIPTION_VALUE = data["Azure"]["Subscriptions"]["Value"]
        #self.SUBSCRIPTION_ENTERPRISE = data["Azure"]["Subscriptions"]["Enterprise"]
        #self.SUBSCRIPTION_PROFESSIONAL = data["Azure"]["Subscriptions"]["Professional"]

        #ApplicationInsights
        self.APPLICATION_INSIGHTS_CONNECTION_STRING = data["Azure"]["ApplicationInsights"]["ConnectionString"]

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