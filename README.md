# beatbuddy
# Spotify Listening History Collector
This script collects the listening history of a Spotify user and saves it into an Excel file. It uses the Spotify API to fetch recently played tracks, processes the data, and appends it to an existing Excel file, avoiding duplicates. The script includes error handling, logging, and retry logic to manage transient network issues.

## Features
1. Spotify Authentication: Authenticates using Spotify OAuth.
2. Fetch Recently Played Tracks: Retrieves up to 50 of the user's most recently played tracks.
3. Save to Excel: Saves the track data to an Excel file, appending to existing data while avoiding duplicates.
4. Error Handling: Includes error handling for network issues and API errors.
5. Retry Logic: Implements retry logic with exponential backoff for transient errors.
6. AWS Lambda Integration: Can be deployed as an AWS Lambda function for automated periodic execution.

## Prerequisites
1. Python 3.x
2. Spotify Developer Account with a registered application
3. Required Python packages:
spotipy

pandas

openpyxl

requests

## Setup
1. Clone the repository:

`git clone https://github.com/drtechbro/spotify-listening-history-collector.git`

`cd spotify-listening-history-collector`

2. Install dependencies:

`pip install spotipy pandas openpyxl requests`

3. Set up Spotify API credentials:

Register your application on the Spotify Developer Dashboard and obtain the Client ID and Client Secret.

4. Set environment variables:

`export SPOTIFY_CLIENT_ID='your_client_id'`
`export SPOTIFY_CLIENT_SECRET='your_client_secret'`

5. Run the script:

`python download_spotify_data.py`

## AWS Lambda Deployment
1. Package the project:

Zip the contents of the project directory including dependencies.

2. Create an AWS Lambda function:

Use the AWS Management Console to create a new Lambda function and upload the zipped package.

3. Set environment variables in the Lambda configuration:

`SPOTIFY_CLIENT_ID`
`SPOTIFY_CLIENT_SECRET`

4. Configure a trigger to run the Lambda function periodically, such as using an AWS CloudWatch Events rule.

## Usage
Fetch and Save Data Locally

1. Run the script locally to fetch recently played tracks and save them to an Excel file:

`python download_spotify_data.py`

2. Lambda Function

To deploy as an AWS Lambda function, ensure the lambda_handler function is used as the entry point. The Lambda function fetches recently played tracks and saves them to an Excel file stored in the specified S3 bucket.

## Error Handling and Logging
The script includes comprehensive error handling and logging to ensure smooth operation. Logs provide detailed information about each step of the process and any errors encountered.

# Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

# License
This project is licensed under the MIT License.

