# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx",
#   "pandas",
#   "seaborn",
#   "matplotlib",
#   "chardet",
#   "scikit-learn"
# ]
# ///

import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import httpx
import chardet
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.ensemble import IsolationForest
from pathlib import Path

API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"


def get_token():
    """Retrieve API token from environment variable."""
    try:
        return os.environ["AIPROXY_TOKEN"]
    except KeyError:
        print("Error: AIPROXY_TOKEN environment variable not set.")
        sys.exit(1)


def load_data(file_path):
    """Load CSV data with encoding detection."""
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']
        print(f"Detected file encoding: {encoding}")

    return pd.read_csv(file_path, encoding=encoding)


def preprocess_data(df):
    """Preprocess data by handling missing values."""
    numeric_df = df.select_dtypes(include=['number'])
    imputer = SimpleImputer(strategy='mean')
    numeric_df_imputed = pd.DataFrame(imputer.fit_transform(numeric_df), columns=numeric_df.columns)
    return numeric_df_imputed


def analyze_data(df):
    """Perform enhanced data analysis including clustering and anomaly detection."""
    if df.empty:
        print("Error: Dataset is empty.")
        sys.exit(1)

    numeric_df_imputed = preprocess_data(df)

    # Basic analysis
    analysis = {
        'summary': df.describe(include='all').to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'correlation': numeric_df_imputed.corr().to_dict()
    }

    # Advanced analysis: Clustering and Anomaly Detection
    if not numeric_df_imputed.empty:
        kmeans = KMeans(n_clusters=3, random_state=0).fit(numeric_df_imputed)
        analysis['clusters'] = kmeans.labels_.tolist()

        iso_forest = IsolationForest(contamination=0.1, random_state=0)
        analysis['anomalies'] = iso_forest.fit_predict(numeric_df_imputed).tolist()

    print("Data analysis complete.")
    return analysis


def visualize_data(df, output_dir, analysis):
    """Generate and save enhanced visualizations."""
    sns.set(style="whitegrid")
    numeric_columns = df.select_dtypes(include=['number']).columns

    output_dir.mkdir(parents=True, exist_ok=True)

    for column in numeric_columns:
        plt.figure()
        sns.histplot(df[column].dropna(), kde=True)
        plt.title(f'Distribution of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.legend(['KDE', 'Histogram'])
        file_name = output_dir / f'{column}_distribution.png'
        plt.savefig(file_name)
        print(f"Saved distribution plot: {file_name}")
        plt.close()

    if not numeric_columns.empty:
        plt.figure(figsize=(8, 6))
        corr = df[numeric_columns].corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm', square=True)
        plt.title('Correlation Heatmap')
        file_name = output_dir / 'correlation_heatmap.png'
        plt.savefig(file_name)
        print(f"Saved correlation heatmap: {file_name}")
        plt.close()


def generate_narrative(analysis, token, file_path):
    """Generate narrative using LLM with optimized prompts."""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    prompt = (
        f"You are a data analyst. Provide a detailed narrative based on the following data analysis results for the file '{file_path.name}':\n\n"
        f"Column Names & Types: {list(analysis['summary'].keys())}\n\n"
        f"Summary Statistics: {analysis['summary']}\n\n"
        f"Missing Values: {analysis['missing_values']}\n\n"
        f"Correlation Matrix: {analysis['correlation']}\n\n"
        f"Clusters: {analysis.get('clusters', [])}\n\n"
        f"Anomalies: {analysis.get('anomalies', [])}\n\n"
        "Based on this information, provide insights into trends, outliers, anomalies, or patterns you can detect."
    )

    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = httpx.post(API_URL, headers=headers, json=data, timeout=30.0)
        response.raise_for_status()

        return response.json()['choices'][0]['message']['content']

    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")

    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return "Narrative generation failed due to an error."


def save_narrative_with_images(narrative, output_dir):
    """Save narrative to README.md and embed image links."""
    readme_path = output_dir / 'README.md'

    image_links = "\n".join(
        [f"![{img.name}]({img.name})" for img in output_dir.glob('*.png')]
    )

    with open(readme_path, 'w') as f:
        f.write(narrative + "\n\n## Visualizations\n\n" + image_links)

    print(f"Narrative successfully written to {readme_path}")


def main(file_path):
    file_path = Path(file_path)

    if not file_path.is_file():
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    token = get_token()

    df = load_data(file_path)

    analysis = analyze_data(df)

    output_dir = Path(file_path.stem)  # Create directory named after dataset
    visualize_data(df, output_dir, analysis)

    narrative = generate_narrative(analysis, token, file_path)

    if narrative != "Narrative generation failed due to an error.":
        save_narrative_with_images(narrative, output_dir)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python autolysis-2.py <dataset.csv>")
        sys.exit(1)

    main(sys.argv[1])
