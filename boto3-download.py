import boto3
import botocore

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

# response = s3_client.list_buckets()
# print('The list of bucket: ')
# for Iresponse in response:
#     if Iresponse=="Buckets":
#         dict=response[Iresponse]
#         for item in dict:
#             bucket=item['Name']
#             print (bucket)
#
# buckets=[bucket['Name'] for bucket in response['Buckets']]
# print('bucket name: %s' % buckets)
#
# print('\n')

# Create a bucket:
# s3.create_bucket(Bucket='mp3txt', create_bucketconfigration,,,,)

BUCKET_NAME='songhaow-test'

response01=s3_client.list_objects_v2(Bucket=BUCKET_NAME)
print('The list of mp3 files: ')
for  Iresponse01 in response01:
  if Iresponse01=="Contents":
        dict=response01[Iresponse01]
        for item in dict:
            imp3=item['Key']
            print (imp3)
            localname=imp3
            s3.Bucket(BUCKET_NAME).download_file(imp3, localname)
