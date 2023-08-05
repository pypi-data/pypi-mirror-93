# AUTOGENERATED! DO NOT EDIT! File to edit: database2.ipynb (unless otherwise specified).

__all__ = ['DEFAULTCOLS', 'PandasDataFrameAttribute', 'Database', 'updateWithDfs', 'lambdaPresignUpload',
           'lambdaIngestUpload', 'lambdaSingleBranchQuery', 'lambdaAllBranchesQuery']

# Cell
from .helper import DatabaseHelper
from .s3 import DatabaseS3
from .query import Querier
from .update import Updater
import pandas as pd
from datetime import datetime
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, JSONAttribute, BooleanAttribute, BinaryAttribute, Attribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.constants import BINARY
from awsSchema.apigateway import Response, Event
from botocore.config import Config
from s3bz.s3bz import S3
from linesdk.slack import SlackBot
from pprint import pprint
from nicHelper.wrappers import add_class_method, add_method
from nicHelper import pdUtils
from nicHelper.pdUtils import getDfHash
from nicHelper.dictUtil import hashDict
from io import BytesIO

import pickle, json, boto3, bz2, requests, validators, os, logging, sys, zlib

# Cell

DEFAULTCOLS = json.loads(os.environ.get('DEFAULTCOLS') or '[]')
try:
  SLACK = os.environ.get('SLACK')
  DATABASE_TABLE_NAME = os.environ['DATABASE_TABLE_NAME']
  PRICE_BUCKET_NAME = os.environ['PRICE_BUCKET_NAME']
  INPUT_BUCKET_NAME = os.environ['INPUT_BUCKET_NAME']
  REGION = os.environ['REGION']
  ACCESS_KEY_ID = None
  SECRET_ACCESS_KEY = None
except Exception as e:
  print(f'error, missing environment variables \n{e}')
  DATABASE_TABLE_NAME = None
  INVENTORY_BUCKET_NAME = None
  INPUT_BUCKET_NAME = None
  ACCESS_KEY_ID = None
  SECRET_ACCESS_KEY = None
  REGION = 'ap-southeast-1'
try:
  DAX_ENDPOINT = os.environ['DAX_ENDPOINT']
except:
  DAX_ENDPOINT = None
  print('dax endpoint missing')


# Cell
# dont forget to import dependent classes from the relevant notebooks
class PandasDataFrameAttribute(Attribute):
  attr_type = BINARY
  def serialize(self, value: pd.DataFrame)->bin:
    bio = BytesIO()
    floatVal:pd.DataFrame = value.astype(float)
    floatVal[DEFAULTCOLS].to_feather(bio)
    data:bin = bio.getvalue()
    compressedData:bin = zlib.compress(data)
    return compressedData
  def deserialize(self, compressedData: bin)->pd.DataFrame:
    data = zlib.decompress(compressedData)
    bio = BytesIO(data)
    df: pd.DataFrame = pd.read_feather(bio)[DEFAULTCOLS]
    return df
class Database(Model):
  class Meta:
    table_name = DATABASE_TABLE_NAME
    region = REGION
    billing_mode='PAY_PER_REQUEST'
    dax_read_endpoints = [DAX_ENDPOINT] if DAX_ENDPOINT else None
    dax_write_endpoints = [DAX_ENDPOINT] if DAX_ENDPOINT else None

  brcode = UnicodeAttribute(hash_key=True, default = 0)
  lastUpdate = NumberAttribute(default=datetime.now().timestamp())
  data = PandasDataFrameAttribute()

  def __repr__(self):
    return self.data.head().to_string()
  def size(self):
    return f'data is size {sys.getsizeof(self.data)/1e3} kB'





# Cell
@add_class_method(Database)
def updateWithDfs(cls, df: pd.DataFrame, defaultDf= pd.DataFrame({i:[] for i in DEFAULTCOLS})):
  results = []
  ##### split df based on brcode
  fdf = {}
  brcodes = df['brcode'].unique()
  for brcode in brcodes:
    mask = df['brcode'] == brcode
    fdf[brcode] = df[mask]

  ##### loop through each df and update in the database
  with cls.batch_write() as batch:
    for brcode, data in fdf.items():
      db:cls = next(cls.query(str(brcode)),None) or cls(brcode=str(brcode), data=defaultDf)
      db.lastUpdate = datetime.now().timestamp()
      df0 = db.data.set_index('cprcode')
      df1 = data.set_index('cprcode')
      db.data = df0.combine_first(df1).reset_index()
      print(db.size())
      result = batch.save(db)
  return True

# Cell
def lambdaPresignUpload(event, *args):
  key:str = Event.parseBody(event)['key']
  presigned:dict = S3.presignUpload(bucket=PRICE_BUCKET_NAME, key = key, expiry = 1000)
  return Response.returnSuccess(body = presigned)

# Cell
def lambdaIngestUpload(event, *args):
  body = Event.parseBody(event)
  key = body['key']
  dtype = body.get('dtype') or 'json'
  path = '/tmp/input'
  S3.loadFile(key = key, path = path, bucket = PRICE_BUCKET_NAME)
  if dtype == 'json':
    df = pd.read_json(path, dtype=str)
    print(f'reading jsoon {df.head()}')
  if dtype == 'feather':
    df = pd.read_feather(path)
    print(f'reading feather{df.head()}')
  result = Database.updateWithDfs(df=df)
  return Response.returnSuccess(df.head().to_dict())

# Cell
def lambdaSingleBranchQuery(event, *args):
  path = '/tmp/tempFile'
  body = Event.parseBody(event)
  brcode = body['brcode']
  cprcodes = body.get('cprcodes')
  format_ = body.get('format') or 'json'
  ###### get branch data #####
  df:pd.DataFrame = next(Database.query(brcode), Database(data=pd.DataFrame())).data
  if cprcodes:
    filteredDf:pd.DataFrame = df[df['cprcode'].isin(cprcodes)]
  else:
    filteredDf:pd.DataFrame = df
  if format_ == 'feather': filteredDf.to_feather(path=path)
  else: dbDict:dict = filteredDf.to_json(path,  orient='split')
  key = hashDict(body)
  S3.saveFile(key=key,path=path,bucket=PRICE_BUCKET_NAME)
  url = S3.presign(key=key,path=path,bucket=PRICE_BUCKET_NAME)
  return Response.returnSuccess({'url': url})

# Cell
from nicHelper.dictUtil import hashDict
def lambdaAllBranchesQuery(event, *args):
  body = Event.from_dict(event).getBody()
  cprcodes = body.get('cprcodes')
  outputFormat = body.get('format') or 'json'
  #### get data from db
  result = Database.scan()
  dfs = [i.data for i in result]
  df = pd.concat(dfs).astype(str).reset_index(drop=True)

  #### filter data if cprcodesExist
  if cprcodes:
    fdf:pd.DataFrame = df[df['cprcode'].isin(cprcodes)]
  else:
    fdf: pd.DataFrame = df

  ### convert to output format and upload to s3
  key = hashDict(body)
  path = '/tmp/tmpFile'
  if outputFormat == 'feather':
    fdf.to_feather(path)
  else:
    fdf.to_json(path, orient = 'split')
  ##### upload to s3
  S3.saveFile(key=key,path=path,bucket=PRICE_BUCKET_NAME)
  url = S3.presign(key=key,path=path,bucket=PRICE_BUCKET_NAME)

  return Response.returnSuccess(body = {'url':url})
