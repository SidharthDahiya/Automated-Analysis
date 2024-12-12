# Automated Analysis: Data Insights with LLMs

## Overview
**Automated Analysis** is a Python-based project that leverages a Language Learning Model (LLM) to analyze datasets, generate insightful visualizations, and narrate data stories. The script performs generic data analysis, creates visual representations, and writes a comprehensive Markdown report (`README.md`) summarizing the results.

This project works with any valid CSV file and provides:
- Summary statistics
- Missing value analysis
- Correlation matrices
- Visualizations (saved as PNG files)
- A narrative report in Markdown format

## Features
1. **Data Analysis**: Automatically computes summary statistics, missing values, and correlations.
2. **Visualization**: Generates 1-3 charts (e.g., histograms) to support data insights.
3. **Narrative Generation**: Uses LLM to write a story about the dataset and findings.
4. **Dynamic Workflow**: Efficiently integrates Python analysis with LLM capabilities.

## How It Works
The script (`autolysis.py`) accepts a single CSV file as input and performs the following steps:
1. Loads the dataset with encoding detection.
2. Conducts generic data analysis, including:
   - Summary statistics
   - Missing value counts
   - Correlation matrix for numeric columns
3. Creates visualizations for numeric columns using Seaborn and Matplotlib.
4. Sends analysis summaries to an LLM for generating a Markdown narrative.
5. Outputs:
   - A `README.md` file summarizing the analysis and insights.
   - PNG files of visualizations embedded in the README.
   - 
## Example Datasets Used
- **goodreads.csv**: A dataset containing 10,000 books from Goodreads, including genres and ratings.
- **happiness.csv**: Data from the World Happiness Report, providing insights into global well-being.
- **media.csv**: Ratings of movies, TV series, and books by course faculty.
  
## Setup Instructions
### Prerequisites
- Python 3.x installed on your system.
- Required libraries: `pandas`, `seaborn`, `matplotlib`, `httpx`, `chardet`.

Install dependencies using:
```bash
pip install pandas seaborn matplotlib httpx chardet
```
Usage
Set Environment Variable**: Ensure your AI Proxy token is set as an environment variable.
   ```bash
   export AIPROXY_TOKEN="your_actual_token"
```

## Project Structure
```
├── autolysis.py # Main Python script for automated analysis
├── goodreads/ # Output directory for goodreads.csv results
│ ├── README.md # Analysis report for goodreads.csv
│ ├── *.png # Visualizations for goodreads.csv
├── happiness/ # Output directory for happiness.csv results
│ ├── README.md # Analysis report for happiness.csv
│ ├── *.png # Visualizations for happiness.csv
├── media/ # Output directory for media.csv results
│ ├── README.md # Analysis report for media.csv
│ ├── *.png # Visualizations for media.csv

```
