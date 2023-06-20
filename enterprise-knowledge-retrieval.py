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
