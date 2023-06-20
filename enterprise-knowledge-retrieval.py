from ast import literal_eval
import openai
import os
import numpy as np
from numpy import array, average
import pandas as pd
from tenacity import retry, wait_random_exponential, stop_after_attempt
import tiktoken
from tqdm import tqdm
from typing import List, Iterator
import wget
#import urllib.request

# Redis imports
from redis import Redis as r
from redis.commands.search.query import Query
from redis.commands.search.field import (
    TextField,
    VectorField,
    NumericField
)
from redis.commands.search.indexDefinition import (
    IndexDefinition,
    IndexType
)

# Langchain imports
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA

CHAT_MODEL = "gpt-3.5-turbo"
pd.set_option('display.max_colwidth', 0)


embeddings_url = 'https://cdn.openai.com/API/examples/data/wikipedia_articles_2000.csv'
wget.download(embeddings_url)


# Setup Redis


REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_DB = '0'

redis_client = r(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB,decode_responses=False)


# Constants
VECTOR_DIM = 1536 # length of the vectors
PREFIX = "wiki" # prefix for the document keys
DISTANCE_METRIC = "COSINE" # distance metric for the vectors (ex. COSINE, IP, L2)


# Create search index

# Index
INDEX_NAME = "wiki-index"           # name of the search index
VECTOR_FIELD_NAME = 'content_vector'

# Define RediSearch fields for each of the columns in the dataset
# This is where you should add any additional metadata you want to capture
id = TextField("id")
url = TextField("url")
title = TextField("title")
text_chunk = TextField("content")
file_chunk_index = NumericField("file_chunk_index")

# define RediSearch vector fields to use HNSW index

text_embedding = VectorField(VECTOR_FIELD_NAME,
    "HNSW", {
        "TYPE": "FLOAT32",
        "DIM": VECTOR_DIM,
        "DISTANCE_METRIC": DISTANCE_METRIC
    }
)
# Add all our field objects to a list to be created as an index
fields = [url,title,text_chunk,file_chunk_index,text_embedding]

redis_client.ping()