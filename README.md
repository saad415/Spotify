# Spotify Data Analysis and Visualization using Power BI

## Overview
This project leverages advanced data engineering and visualization techniques to extract, process, and analyze Spotify user data. It provides a dynamic and insightful view into listening patterns and track characteristics using the Spotify Web API, Python, AWS (EC2 and S3), Power BI, Deneb, HTML, and Google Drive. 
![Link to Dashboard](https://app.powerbi.com/reportEmbed?reportId=8fe7f296-f66c-4e4b-a423-d686a53feeb9&autoAuth=true&embeddedDemo=true)
![Dashboard Preview](https://github.com/saad415/Spotify/blob/main/gif.gif)

## Advanced Technical Implementation

### Automated Data Pipeline
- **Spotify API Integration:** Utilized Python scripts hosted on an AWS EC2 instance to interface with the Spotify Web API, ensuring real-time data access.
- **AWS S3 Storage:** Configured AWS S3 buckets for secure and scalable storage of extracted data in CSV format.
- **Automated Data Refresh:** Established a cron job on the AWS EC2 instance to update CSV files daily, maintaining data relevancy and accuracy.

### Data Extraction and Storage
- **Data Retrieval:** Extracted comprehensive user and track data, including user profiles, playlists, and detailed audio features of tracks.
- **CSV Storage:** Efficiently compiled and organized data into CSV files for ease of processing and analysis.

### Data Analysis and Visualization
- **Power BI Integration:** Employed Power BI for advanced data analysis and visualization, creating an interactive and dynamic user experience.
- **Custom Visualization:** Integrated HTML and Deneb within Power BI to showcase track images and visualize average track popularity.

## Project Impact and Skills Demonstrated
- **Comprehensive Analysis:** Offers in-depth insights into personal Spotify usage and track characteristics.
- **Technical Proficiency:** Showcases expertise in Python scripting, API integration, AWS cloud services, automated data pipelines, and advanced Power BI visualizations.
- **Automation and Scalability:** Highlights the ability to automate data processes and efficiently handle large datasets in a cloud environment.

## Repository Contents
- `scripts/`: Python scripts for data extraction and interaction with the Spotify API.
- `get_data.py/`: It is the python code to get data from s3 bucket into power bi.
- `main.py/`: The main Python script for data extraction and processing.
- `Softify_Ec2.pbix`: The Power BI dashboard file for visualization.
- `Useful_code.txt`: Contains HTML and Deneb code for Power BI visualizations.
- `README.md`: This documentation, including detailed project overview, technical implementation, and usage guide.
