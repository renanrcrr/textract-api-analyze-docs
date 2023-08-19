"""
The code is developed using reference from
https://docs.aws.amazon.com/textract/latest/dg/examples-blocks.html
"""

import json
import logging
import boto3

# Python trp module is Amazon textract result parser
# https://pypi.org/project/textract-trp/
# You have uploaded module using Lambda Layer.
from trp import Document
from urllib.parse import unquote_plus

# It is good practice to use proper logging.
# Here we are using the logging module of python.
# https://docs.python.org/3/library/logging.html

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Boto3 - s3 Client
# More Info: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html
s3 = boto3.client('s3')

# Declare output file path and name
output_key = "output/textract_response.json"


def lambda_handler(event, context):   
    # log the event
    logger.info(event)
    # Iterate through the event
    for record in event['Records']:
        # Get the bucket name and key for the new file
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        # Using Amazon Textract client
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html
        textract = boto3.client('textract')

        # Analyze document
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.analyze_document
        try:
            response = textract.analyze_document(   # You are calling analyze_document API
                Document={                          # to analyzing document Stored in an Amazon S3 Bucket
                    'S3Object': {
                        'Bucket': bucket,
                        'Name': key
                    }
                },
                FeatureTypes=['<Enter_Your_Feature_Type>',  # FeatureTypes is a list of the types of analysis to perform.
                              ])                            # Add TABLES to the list to return information about
                                                            # the tables that are detected in the input document.
                                                            # Add FORMS to return detected form data. To perform both
                                                            # types of analysis, add TABLES and FORMS to FeatureTypes .

            doc = Document(response)  # You are parsing the textract response using Document.

            # The below code reads the Amazon Textract response and
            # prints the Key and Value
            for page in doc.pages:
                # Print fields
                print("Fields:")
                for field in page.form.fields:
                    print("Key: {}, Value: {}".format(field.key, field.value))

                    # Search fields by key
                    # Enter your code below

            # The below code reads the Amazon Textract response and
            # prints the Table data. Uncomment below to use the code.

            # for page in doc.pages:
            #     print("\nTable details:")
            #     for table in page.tables:
            #         for r, row in enumerate(table.rows):
            #             for c, cell in enumerate(row.cells):
            #                 print("Table[{}][{}] = {}".format(r, c, cell.text))

            return_result = {"Status": "Success"}

            # Finally the response file will be written in the S3 bucket output folder.
            s3.put_object(
                Bucket=bucket,
                Key=output_key,
                Body=json.dumps(response, indent=4)
            )

            return return_result
        except Exception as error:
            return {"Status": "Failed", "Reason": json.dumps(error, default=str)}

