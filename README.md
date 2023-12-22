# Spotify Data Analysis and Visualization using Power BI

## Overview
This project uses advanced data engineering and visualization techniques to extract, process, and analyze Spotify user data. It provides an insightful view into listening patterns and track characteristics, leveraging the Spotify Web API, Python, AWS (EC2 and S3), Power BI, Deneb, and HTML. A key aspect of this project is the implementation of Apache Airflow on an AWS EC2 instance, which orchestrates and automates the data pipeline, enhancing efficiency and scalability.
- [Link to Dashboard](https://app.powerbi.com/reportEmbed?reportId=8fe7f296-f66c-4e4b-a423-d686a53feeb9&autoAuth=true&embeddedDemo=true)
- ![Dashboard Preview](https://github.com/saad415/Spotify/blob/main/gif.gif)
- ![Dashboard Preview](https://github.com/saad415/Spotify/blob/main/dag_picture.png)

## Advanced Technical Implementation

### Automated Data Pipeline with Apache Airflow
- **Spotify API Integration:** Utilizes Python scripts on AWS EC2 to connect with the Spotify Web API for real-time data access.
- **AWS S3 Storage:** Uses AWS S3 buckets for secure, scalable data storage in CSV format.
- **Apache Airflow for Data Pipeline Automation:** Implements Apache Airflow on AWS EC2 to manage and automate the data pipeline, enabling more sophisticated and reliable data workflows.

### Data Extraction and Storage
- **Data Retrieval:** Extracts comprehensive user and track data, including user profiles, playlists, and detailed audio features of tracks.
- **CSV Storage:** Organizes data into CSV files for efficient processing and analysis.

### Data Analysis and Visualization
- **Power BI Integration:** Employs Power BI for advanced data analysis and visualization, creating an interactive user experience.
- **Custom Visualization:** Uses HTML and Deneb within Power BI to display track images and visualize average track popularity.

## Project Impact and Skills Demonstrated
- **Comprehensive Analysis:** Offers in-depth insights into Spotify usage and track characteristics.
- **Technical Expertise:** Showcases skills in Python scripting, API integration, AWS cloud services, Apache Airflow for automated data pipelines, and advanced Power BI visualizations.
- **Automation and Scalability:** Highlights the capability to automate data processes and handle large datasets efficiently in a cloud environment.

## Repository Contents
- `get_data.py/`: Python code to retrieve data from the S3 bucket into Power BI.
- `dag.py/`: Python dag script for scheduling and orchestrating data pipeline.
- `Softify_Ec2.pbix`: Power BI dashboard file.
- `Useful_code.txt`: Contains HTML and Deneb code for Power BI visualizations.
- `README.md`: This document, with a detailed project overview, technical implementation, and usage guide.
