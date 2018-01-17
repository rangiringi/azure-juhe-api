import os
import string
import json
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
from azure.storage.blob import BlockBlobService

def processBlob(filename):
   reader = DataFileReader(open(filename, 'rb'), DatumReader())
   dict = {}
   for reading in reader:
       parsed_json = json.loads(reading["Body"])
       if not 'id' in parsed_json:
           return
       if not dict.has_key(parsed_json['id']):
           list = []
           dict[parsed_json['id']] = list
       else:
           list = dict[parsed_json['id']]
           list.append(parsed_json)
   reader.close()
   for device in dict.keys():
       deviceFile = open(device + '.csv', "a")
       for r in dict[device]:
           deviceFile.write(", ".join([str(r[x]) for x in r.keys()])+'\n')

def startProcessing(accountName, key, container):
   print('Processor started using path: ' + os.getcwd())
   block_blob_service = BlockBlobService(account_name=accountName, account_key=key)
   generator = block_blob_service.list_blobs(container)
   for blob in generator:
       #content_length == 508 is an empty file, so only process content_length > 508 i.e. skip  empty files
       if blob.properties.content_length > 508:
           print('Downloaded a non empty blob: ' + blob.name)
           cleanName = string.replace(blob.name, '/', '_')
           block_blob_service.get_blob_to_path(container, blob.name, cleanName)
           processBlob(cleanName)
           os.remove(cleanName)
       block_blob_service.delete_blob(container, blob.name)
startProcessing('tollstation', 'IDh7SmUMUkT3p4imee02MdiZIPFHCkyLNt9/J6tfIqL6fkk1w/+3NnAUq0YOKWZX2/RNMZIcDkojCR2yEoVqMA==', 'streamoutput')