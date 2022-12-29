# Instructions

## Requirements

Following files are required.

- `utils.py` : Contains utilites
- `main.py`  : Main flow of the program
- `environment.yml`: Contains the conda environment containing necessary packages required.

## Setup
Steps to recreate the environment:
```python

conda env create -f environment.yml;
conda activate EOD;
```

PS: If this script fails,manually install matplotlib, sentinelhub, pillow(PIL), gdal, numpy.

Read [sentinelhub](https://sentinelhub-py.readthedocs.io/en/latest/configure.html) docs on how to configure the API for usage. 
Create the account required [HERE](https://www.sentinel-hub.com/develop/api/ogc/standard-parameters/).

For Instance ID go to [Configuration Utility](https://apps.sentinel-hub.com/dashboard/#/configurations).
For SH_Client_ID go to [User Settings]()
and click of 'Create New' under OAuth Clients and use the secret key as SH_Client_Secret.
OR
use my acc credentials already set instead.


## File Structure

```
.
├── data
│   ├── d19514cf33acf6fe96e66c4f12ee1085
│   │   ├── request.json
│   │   ├── response_cog.tiff
│   │   ├── response.tiff
│   │   └── response.webp
│   └── f1c3a296d2ee6a5ccb78451909e72726
│       ├── request.json
│       ├── response_cog_cog.tiff
│       ├── response_cog.tiff
│       ├── response_cog.webp
│       ├── response.tiff
│       └── response.webp
├── environment.yml
├── main.py
├── __pycache__
│   └── utils.cpython-311.pyc
├── README.md
└── utils.py


```
# Output Folder

- data/ This folder contains all output and transformation results.
  - `request.json` : The API request parameters
  - `response.tiff` : The original tiff image returned by the API
  - `response.webp`: Original image transformed into (500x500) webp format with transparency where 0 pixels are presnt for Thumbnails viewing.
  - `response_cog.tiff`: The original high res tiff image converted to Cloud Optimized GeoTIFF format.



# Process

This is the process of the entire code
```
                                   ┌────────────────────────────┐
                                   │                            │
                            ┌──────►   SentinelHub API          │
                            │      │                            │
                            │      │                            │
                            │      └─────────────────┬──────────┘
                            │                        │
                            │                        │
                            │                        │
                            │                        │
                            │                        │
                          Request                 Response
                            │                        │
                            │                        │
                            │                        │
                            │                        │
                                                     │
                                   ┌─────────────────▼────────────┐             |                              |             |                              |
                                   │         Image Data           │
                                   └─────────────────┬────────────┘
                                                     │
                                                     ▼
                                            ┌──────────────────────┐
                                            │                      │
                                            │                      │
                 ┌──────────────────────────┤   Data Folder        │
                 │                          │                      │
                 │                          └────────────▲─────────┘
                 │                                       |│                                       |
 ┌───────────────▼───────────────────────┐               │
 │                                       │               │
 │          Traverse all files in Data   │               │
 │                 folder                │               │
 │                                       │               │
 │                                       │               │
 │                                       │               │
 └──────────────────┬────────────────────┘               │
                    │                                    │
                    │                                    │
           ┌────────▼─────────────┐                      │
           │                      │                      │
           │                      │                      │
           │                      │                      │
┌──────────▼──────────┐      ┌────▼────────────┐         │
│                     │      │                 │         │
│ convert_to_thumbnail│      │ convert_to_cog  │         │
│                     │      │                 │         │
│                     │      │                 │         │
└──────────┬──────────┘      └─────┬───────────┘         │
           │                       │                     │
           │                       │                     │
           │                       │                     │
           │                       │                     │
           └──────────►┌───────────┘                     │
                       │                                 │
                       │                                 │
                       │                                 │
                       └─────────────────────────────────┘
```
