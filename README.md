# Insurance-Risk-Analytics-Predictive-Modeling

A comprehensive insurance risk analytics platform that performs exploratory data analysis (EDA) and predictive modeling on insurance claim data. This project analyzes loss ratios, claim patterns, and vehicle/geographic risk factors using advanced statistical techniques and machine learning.

## Project Overview

This repository contains:
- **Exploratory Data Analysis (EDA)**: Comprehensive statistical analysis including data quality assessment, univariate/bivariate analysis, and outlier detection
- **Utility Modules**: Reusable Python functions for data processing, visualization, and analysis
- **CI/CD Pipeline**: Automated GitHub Actions workflows for linting and testing
- **Documentation**: Clear insights and recommendations from the analysis

## Dataset

The analysis uses the `MachineLearningRating_v3.txt` dataset containing:
- Insurance claim records with financial metrics (TotalPremium, TotalClaims)
- Vehicle information (Make, Model, Type)
- Geographic data (Province, ZipCode)
- Customer demographics (Gender, Age)
- Temporal data spanning an 18-month period

## Key Analyses

### Data Summarization
- Descriptive statistics for numerical features
- Data type validation for categorical, date, and numerical columns

### Data Quality
- Missing value analysis and handling strategy
- Data consistency checks

### Univariate Analysis
- Histograms and distributions for numerical columns
- Bar charts for categorical variables
- Statistical summaries

### Bivariate & Multivariate Analysis
- Loss Ratio analysis by Province, VehicleType, and Gender
- Correlation matrices
- Relationships between TotalPremium and TotalClaims
- Geographic trend analysis

### Outlier Detection
- Box plots for key numerical features
- Outlier identification and documentation

### Key Insights
- Loss ratio patterns across dimensions
- Claim severity and frequency trends
- Vehicle make/model risk profiles
- Geographic risk variations

## Project Structure

```
.
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
├── .gitignore                        # Git ignore rules
├── .github/
│   └── workflows/
│       └── ci.yml                    # GitHub Actions CI/CD pipeline
├── data/
│   └── MachineLearningRating_v3.txt  # Insurance dataset
├── src/
│   ├── __init__.py
│   ├── data_loader.py                # Data loading utilities
│   ├── eda_utils.py                  # EDA utility functions
│   ├── visualization.py              # Visualization helpers
│   └── analysis.py                   # Analysis functions
└── notebooks/
    └── EDA_Insurance_Analysis.ipynb  # Main EDA notebook
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Insurance-Risk-Analytics-Predictive-Modeling
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the EDA

1. **Open the Jupyter notebook**
   ```bash
   jupyter notebook notebooks/EDA_Insurance_Analysis.ipynb
   ```

2. **Run all cells** to execute the complete analysis

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) automatically:
- Runs on every push to any branch
- Executes linting checks (flake8, pylint)
- Runs unit tests (pytest)
- Reports results in GitHub

To view pipeline status, check the **Actions** tab in your GitHub repository.

## Key Findings & Questions Addressed

The EDA notebook addresses:
1. **Overall Loss Ratio**: Portfolio-wide and segmented by Province, VehicleType, and Gender
2. **Financial Distribution**: Key statistics on TotalPremium, TotalClaims, and CustomValueEstimate with outlier analysis
3. **Temporal Trends**: Changes in claim frequency/severity over the 18-month period
4. **Vehicle Analysis**: Claim amounts by vehicle make/model
5. **Geographic Patterns**: Regional variations in coverage, premiums, and vehicle types

## Dependencies

- pandas: Data manipulation and analysis
- numpy: Numerical computing
- matplotlib: Static visualization
- seaborn: Statistical graphics
- plotly: Interactive visualizations
- scikit-learn: Machine learning utilities
- pytest: Testing framework
- flake8: Code linting

See `requirements.txt` for complete list with versions.

## Data Version Control (DVC)

This project implements Data Version Control (DVC) for reproducible and auditable data pipeline management, a critical practice in regulated industries.

### DVC Setup

DVC has been initialized and configured with a local remote storage for version tracking of all data files. This enables:
- **Reproducibility**: Exact data versions for any analysis at any time
- **Auditability**: Complete history of data transformations
- **Regulatory Compliance**: Full audit trail for regulatory requirements

### Data Versions

The project tracks multiple versions of the dataset:

1. **Raw Data Version**: `data/MachineLearningRating_v3.txt` - Original insurance data
2. **Cleaned Data Version**: `data/MachineLearningRating_cleaned_v1.txt` - Deduplicated and cleaned version

### DVC Configuration

- **Remote Storage**: Local directory at `C:\Users\usb\Documents\dvc_storage_v2`
- **Remote Name**: `localstorage` (default remote)
- **Storage Format**: Content-addressable storage (files organized by MD5 hash)

### Reproducing the Data Pipeline

To reproduce the data pipeline and retrieve specific versions:

```bash
# Initialize DVC (if not already done)
dvc init

# Add the default remote (already configured)
dvc remote add -d localstorage /path/to/dvc_storage

# Pull data from remote storage
dvc pull

# View DVC status
dvc status

# Check data file tracking
dvc dag

# Create a new version of data
python src/data_versioning.py

# Track new data version
dvc add data/new_data_version.txt

# Push data to remote
dvc push

# Commit metadata to git
git add data/new_data_version.txt.dvc
git commit -m "Add new data version"
```

### Data Versioning Workflow

1. **Create Data Version**: Generate or modify data using `src/data_versioning.py`
2. **Track with DVC**: Use `dvc add` to track the data file
3. **Push to Remote**: Store actual data in remote storage using `dvc push`
4. **Commit Metadata**: Track `.dvc` files in Git for versioning metadata

### Accessing Data From Remote

To retrieve data from remote storage:

```bash
# Pull all tracked data
dvc pull

# Pull specific file
dvc pull data/MachineLearningRating_v3.txt.dvc

# Check what's been modified
dvc status
```

This approach ensures that large data files (>100MB) can be tracked without bloating the Git repository, while maintaining complete auditability and reproducibility for regulatory compliance.

## Contributing

1. Create a new branch for your work: `git checkout -b feature/your-feature`
2. Make your changes and commit with descriptive messages
3. Push to your branch: `git push origin feature/your-feature`
4. Open a Pull Request

## License

This project is for analytical and educational purposes.

## Author

Insurance Risk Analytics Team