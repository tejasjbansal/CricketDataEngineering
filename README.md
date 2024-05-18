# Cricket Stadium Data Pipeline

Welcome to the Cricket Stadium Data Pipeline project! This Python-based project is designed to automate the process of extracting cricket stadium data from Wikipedia, cleaning it, and storing it in Azure Data Lake. The data is then processed using Azure Data Factory, analyzed with Azure Synapse Analytics, and visualized with Tableau.

## Table of Contents
- [Introduction](#introduction)
- [System Architecture](#System-Architecture) 
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Dashboard](#dashboard)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project leverages Apache Airflow to crawl cricket stadium data from Wikipedia, clean the data, and push it to Azure Data Lake. Azure Data Factory is then used to pull and process the data, storing the clean data back into Azure Data Lake. For analytics, Azure Synapse Analytics is utilized, and the data is finally visualized using Tableau.

## System Architecture
![Project Architecture](https://github.com/tejasjbansal/CricketDataEngineering/assets/56173595/6f3edab5-9137-47ad-b5db-2eeb5a1d27b6)


## Features

- **Data Crawling**: Uses Apache Airflow to extract data from Wikipedia.
- **Data Cleaning**: Cleans and prepares the data for processing.
- **Data Storage**: Stores data in Azure Data Lake.
- **Data Processing**: Processes data using Azure Data Factory.
- **Analytics**: Analyzes data with Azure Synapse Analytics.
- **Visualization**: Visualizes data with Tableau.

## Requirements

- Python 3.9 (minimum)
- Docker
- PostgreSQL
- Apache Airflow 2.6 (minimum)
- Azure Account for Azure Services
- Tableau for Visualization

## Installation

1. **Clone the Repository**

    ```sh
    git clone https://github.com/tejasjbansal/CricketDataEngineering.git
    cd CricketDataEngineering
    ```

2. **Set Up Python Environment**

    Create and activate a virtual environment:

    ```sh
    python3.9 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set Up Docker**

    Ensure Docker is installed and running on your system. You may refer to the [Docker installation guide](https://docs.docker.com/get-docker/) for assistance.

5. **Run the Docker Compose**

    For Initialize Postgres database and start the Airflow webserver and scheduler:

    ```sh
    docker compose up -d
    ```

6. **Set Up Azure Services**

    - Create an Azure account if you don't have one.
    - Set up Azure Data Lake and Azure Data Factory.
    - Configure Azure Synapse Analytics.
    - Install Tableau for data visualization.

## Usage

1. **Run the Airflow DAG**

    Navigate to the Airflow web interface (http://localhost:8080) and trigger the DAG for data extraction and storing data to Azure Data Lake.

2. **Process Data with Azure Data Factory**

    Use Azure Data Factory to pull data from Azure Data Lake, process it, and store the clean data back in Azure Data Lake.

3. **Analyze Data with Azure Synapse Analytics**

    Utilize Azure Synapse Analytics for any required data analysis.

4. **Visualize Data with Tableau**

    Connect Tableau to your Azure Synapse Analytics to create visualizations and dashboards.

## Project Structure

```plaintext
cricket-stadium-data-pipeline/
├── dags/
│   ├── wikipedia_flow.py
├── scripts/
│   ├── setup_postgres.sh
├── data/
|── pipelines/
│   ├── wikipedia_pipeline.py
├── requirements.txt
├── README.md
```

- **dags/**: Contains Apache Airflow DAGs for data crawling and cleaning.
- **scripts/**: Shell scripts for setting up Apache Airflow.
- **data/**: Directory for storing temporary data files.
- **requirements.txt**: Python dependencies.
- **README.md**: Project documentation.

## Dashboard
![Dashboard](https://github.com/tejasjbansal/CricketDataEngineering/assets/56173595/e8462f24-5236-4f6c-9679-e32106e8bb3d)

## Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) file for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Happy coding! If you have any questions or need further assistance, feel free to open an issue or contact the project maintainers.
