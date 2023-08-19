# Textract API Analyze Docs Synchronously

This code gets the S3 attributes from the trigger event, then invokes the textract api to analyze documents synchronously.

## Code to Test Event

```json
{
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "<Your_bucket_name>"
        },
        "object": {
          "key": "input/employment_form.png"
        }
      }
    }
  ]
}