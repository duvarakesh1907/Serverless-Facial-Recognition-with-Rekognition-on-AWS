import boto3
      import json
      import os

      rekognition = boto3.client('rekognition')
      dynamodb = boto3.client('dynamodb')

      def lambda_handler(event, context):
          bucket_name = event['Records'][0]['s3']['bucket']['name']
          object_key = event['Records'][0]['s3']['object']['key']

          response = rekognition.detect_faces(
              Image={
                  'S3Object': {
                      'Bucket': bucket_name,
                      'Name': object_key,
                  }
              },
              Attributes=['ALL']
          )

          # Store results in DynamoDB
          dynamodb.put_item(
              TableName=os.environ['DYNAMODB_TABLE'],
              Item={
                  'ImageID': {'S': object_key},
                  'RekognitionData': {'S': json.dumps(response)}
              }
          )

          return response