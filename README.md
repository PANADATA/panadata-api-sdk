# Panadata API SDK
This python SDK helps you interact with the panadata API to genrate reports and lots more.

## Main functionalities
- sanitizing/enriching input data
- transforming/sorting results
- reading/generating CSV reports

## Methods
- **csv**: transform input CSVs into lists of dicts to facilitate manipulation of the data and generate CSV reports with results
- **generator**: Methods to generate random data i.e. cedulas and RUCs for testing purposes
- **organizations**: Methods to help maximize your usage of the organizations endpoint. Maximize the amount of matches for organizations on the panadata API by searching for various fields in specific orders, asigning a minimum match level to results and more!

## Installation
first create a .env file in the root of your project with the variables bellow. Then instantiate these by running `. .env`

```
export PANADATA_API_TOKEN=<yoyr_panadata_api_token>
export GH_TOKEN=<your_gh_personal_access_token>
export PROCESSES=5
```
Now you can install the panadata API SDK with pip by running the following command from the root of your project or by adding the path in your python requirements file. Here GH_TOKEN is an environment variable that contains a valid github personal access token with access to the panadatalyer repo

```
pip install git+https://${GH_TOKEN}:@github.com/PANADATA/panadata-api-sdk.git@master#egg=panadatalayer
```

## Usage
The example bellow is a script to verify company information (RUCs and names). Once fed a CSV file in the correct format, this method will do the follwoign for each row in the CSV:
1. convert rucs into fichas
2. simplify organization names by removing common organization suffixes
3. search by ficha & sort results by name
4. if names match set name_match as true and ficha_match as true
5. if names dont match set ficha_match as false and search by simplified name
6. if names match set name match as true
7. add a ruc_match

**input:** name of a csv file with the correct format that contains columns input_name and input_ruc plus any additional columns
**output:** a csv with the input and output rucs/names/fichas and a match score for ficha, name, and ruc

```
from panadata_api_sdk.organizations import organization_matches_report

organization_matches_report('sample', 'output')
```