import boto3
import pandas as pd
import io
# AWS credentials (configure these with your own values)
aws_access_key_id = 'AKIAUTEANXGB2VM2JSPP'
aws_secret_access_key = 'QfrguEBd0/8rmXctChoj+oO6WyaZLUZvhU2Jlcht'
s3_bucket_name = 'saad-spotify'
s3_file_key = 'track_audio_features.csv'  # Update to point to the CSV file in your S3 bucket

# Initialize an S3 client
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Specify the S3 bucket and file you want to retrieve
bucket_name = s3_bucket_name
file_key = s3_file_key

# Download the CSV file from S3
try:
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    content = response['Body'].read()

    # Read the CSV content into a Pandas DataFrame
    df = pd.read_csv(io.BytesIO(content))

    # Now you can work with the DataFrame 'df' containing the CSV data
    # Optionally, you can save the DataFrame as a new CSV file locally
    local_csv_file = 'downloaded_data.csv'  # Specify the local file path
    df.to_csv(s3_file_key, index=False)

   # print(f"Data saved to '{local_csv_file}'")
except Exception as e:
    print(f"An error occurred: {str(e)}")