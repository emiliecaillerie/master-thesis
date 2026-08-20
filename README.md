# Machine Learning-Based Classification of Climate Legislation: A Comparative Analysis of Legislative Coverage and Hazard Intensity

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Repository structure

```bash
├── law
│   ├── data
│   │   ├── *.csv
│   ├── outputs
│   │   ├── *.csv
│   ├── .env
│   ├── 2_law_exploration.ipynb
│   ├── 3_law_preprocessing.ipynb
│   ├── 4_law_classification_baseline.ipynb
│   ├── 4_law_classification_llm.ipynb
│   ├── 4_law_classification_nlp.ipynb
│   └── 5_law_classification_eval.ipynb
├── sensor
│   ├── data
│   │   ├── *.csv
│   ├── outputs
│   │   ├── *.csv
│   ├── 2_sensor_preprocessing.ipynb
│   ├── 3_sensor_exploration.ipynb
│   ├── 4_sensor_correlation_continent.ipynb
│   ├── 4_sensor_correlation_country.ipynb
│   └── 5_sensor_correlation_eval.ipynb
├── visualization
│   ├── outputs
│   │   ├── *.csv
│   ├── visualization_dashboard.py
│   └── visualization_datasets.ipynb
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup

The version of Python used throughout the research is 3.13.1.

```bash
# Install dependencies
pip install -r requirements.txt
```

LLM classification uses the [Ollama Cloud API](https://ollama.com), requiring an Ollama account with an API key set as an environment variable:

```bash
# .env file in law/
OLLAMA_API_KEY=your_key_here
```

## Data Sources

All three datasets are available as open data under the Creative Commons Attribution Licence (CC-BY) 4.0 and redistribution is permitted as of August 2026.

### [Climate Change Laws of the World (CCLW)](https://climate-laws.org)

- Grantham Research Institute at the London School of Economics and Climate Policy Radar (2023). Climate Change Laws of the World. [https://climate-laws.org](https://climate-laws.org) and [https://app.climatepolicyradar.org/search](https://app.climatepolicyradar.org/search)

Modifications: Data was cleaned, spatially/temporally aggregated, and classified for the purposes of this study. Full processing scripts are available in `law/`.

### [Climate Policy Database (CPDB)](https://climatepolicydatabase.org)

- NewClimate Institute, Wageningen University and Research & PBL Netherlands Environmental Assessment Agency (2025).   Climate Policy Database. DOI: 10.5281/zenodo.19682932

Modifications: Data was cleaned, spatially/temporally aggregated, and classified for the purposes of this study. Full processing scripts are available in `law/`.

### [Copernicus Climate Data Store (CDS)](https://cds.climate.copernicus.eu/)

- European Centre for Medium-Range Weather Forecasts (2025): Monthly drought indices from 1940 to present derived from ERA5 reanalysis. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). DOI: 10.24381/9bea5e16
- Copernicus Climate Change Service, Climate Data Store, (2018): Sea level gridded data from satellite observations for the global ocean from 1993 to present. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). DOI: 10.24381/cds.4c328c78
- Copernicus Climate Change Service (2022): ERA5-Land monthly averaged data from 1950 to present. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). DOI: 10.24381/cds.68d2bb30
- Copernicus Climate Change Service (2023): ERA5 monthly averaged data on single levels from 1940 to present. Copernicus Climate Change Service (C3S) Climate Data Store (CDS). DOI: 10.24381/cds.f17050d7

Modifications: Data was cleaned, spatially/temporally aggregated, and correlated for the purposes of this study. Full processing scripts are available in `sensor/`.

## Running the Code

### RQ1: `law/`

```bash
# Data Understanding and Preparation of Legislation Data:
jupyter notebook law/2_law_exploration.ipynb
jupyter notebook law/3_law_preprocessing.ipynb

# RQ1 Modeling - Classification Approaches:
jupyter notebook law/4_law_classification_baseline.ipynb
jupyter notebook law/4_law_classification_nlp.ipynb
jupyter notebook law/4_law_classification_llm.ipynb  

# RQ1 Evaluation:
jupyter notebook law/5_law_classification_eval.ipynb
```

### RQ2: `sensor/`

```bash
# Data Preparation and Understanding of Sensor Data:
jupyter notebook sensor/2_sensor_preprocessing.ipynb
jupyter notebook sensor/3_sensor_exploration.ipynb

# RQ2 Modeling - Correlation on Different Levels:
jupyter notebook sensor/4_sensor_correlation_country.ipynb
jupyter notebook sensor/4_sensor_correlation_continent.ipynb

# RQ2 Evaluation:
jupyter notebook sensor/5_sensor_correlation_eval.ipynb
```

### RQ3: `visualization/`

```bash
# RQ3 Modeling:
jupyter notebook visualization/visualization_datasets.ipynb 
python visualization/visualization_dashboard.py
```

The dashboard can be opened at [http://127.0.0.1:8050](http://127.0.0.1:8050)

## License

This project is licensed under the MIT License, see the [LICENSE](LICENSE) file for details.
The MIT License applies solely to the software scripts, source code, and associated documentation authored for this repository.

Datasets and data files included in the `/data` directories are third-party materials licensed under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) license. Full citations, source links, and modification notices are provided in **Data Sources** section.

## Contact

Emilie Caillerie: [emilie.caillerie@student.tuwien.ac.at](emilie.caillerie@student.tuwien.ac.at)
