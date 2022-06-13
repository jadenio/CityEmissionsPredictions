import boto3

client = boto3.client('s3')
BUCKET = 's3groupturkey'   
FILE_NAME = 'data/kaggle/greenhouse_gas_inventory_data_data.csv' # DO NOT DELETE "data/"
client.download_file(BUCKET, FILE_NAME, '000_kaggle.csv')
#print(open('test.csv').read()) --> To read the document