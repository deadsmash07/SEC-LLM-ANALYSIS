from analyzer import analyze, parse_filing_text
import os
import re
import argparse
import json
import matplotlib.pyplot as plt
import shutil
import numpy as np

def get_year(folder_name):
    """
    Extract the year from the folder name using a regular expression.
    """
    match = re.search(r'-(\d{2})-', folder_name)
    if match:
        year = int(match.group(1))
        return str(1900 + year) if year > 80 else str(2000 + year)
    return None


def extract_total_values(json_data):
    try:
        total_values = {}
        # Parse JSON data
        for key, value in json_data.items():
            if isinstance(value, dict):
                total_value = sum(parse_value(sub_value) for sub_value in value.values())
                total_values[key] = total_value
            else:
                total_values[key] = parse_value(value)
        return total_values
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return {}
    except Exception as e:
        print(f"Error processing data: {e}")
        return {}

def parse_value(value):
    if not isinstance(value, str):
        print(f"Error: value is not a string, it's a {type(value)}")
        return 0    
    try:
        value = value.strip('$').lower()
        number = float(re.sub(r'[^\d.]', '', value))
        if 'billion' in value:
            return number
        elif 'million' in value:
            return number / 1000
        elif 'thousand' in value:
            return number / 1000000
        return number
    except ValueError:
        print(f"ValueError: could not convert {value} to float")
        return 0


def drop_none_values(data):
    """
    Remove entries from the dictionary where the value is None.
    """
    return {k: v for k, v in data.items() if v is not None}

def create_bar_plot(ticker, insights):
    """
    Create bar plots for the total values of insights over the years, ensuring no overlap in x-axis labels.
    """
    directory = f'visualizations/{ticker}/insights'
    shutil.rmtree(directory, ignore_errors=True)
    os.makedirs(directory, exist_ok=True)

    # Gather all unique keys from all years to ensure no data is missed
    all_keys = set(key for year_data in insights.values() for key in year_data.keys())
    
    for key in all_keys:
        # Gather data for each key from each year, ensuring to handle missing data
        years = sorted(insights.keys())
        values = [insights[year].get(key, 0) for year in years]

        # Creating the bar plot
        plt.figure(figsize=(10, 6))
        plt.bar(years, values, color=['red' if v < 0 else 'blue' for v in values])
        plt.xlabel('Year')
        plt.ylabel(key)
        plt.title(f'{key} over the Years')
        plt.xticks(years, rotation=45)  # Adjust for better label visualization
        plt.yscale('symlog')  # Use logarithmic scale for the y-axis
        plt.tight_layout()  # Adjust layout to make room for label rotation

        # Save the plot in the designated directory
        plt.savefig(f'{directory}/{key}.png')
        plt.close()

def extract_values_for_segments_charts(json_data):
    """
    Extract segment-wise data for detailed bar charts.
    """
    segment_values = {}
    for key, segments in json_data.items():
        if isinstance(segments, dict):
            segment_values[key] = {sub_key: parse_value(sub_value) for sub_key, sub_value in segments.items()}
    return segment_values

def create_segment_bar_plots(ticker, insights):
    """
    Create bar plots for Revenue and Net Income segments for each year.

    Args:
        - ticker: The company's stock ticker symbol
        - insights: A dictionary containing the insights for each year

    Returns:
        - None
        - Saves the bar plots in the "visualizations/{ticker}/detailed" directory
    """
    directory = f'visualizations/{ticker}/detailed'
    shutil.rmtree(directory, ignore_errors=True)
    os.makedirs(directory, exist_ok=True)

    for year, data in insights.items():
        segments = extract_values_for_segments_charts(data)
        for segment_name, values in segments.items():
            if values:  # Ensure there is data to plot
                labels, amounts = zip(*values.items())
                num_segments = len(amounts)
                colors = generate_colors(num_segments, amounts)
                plot_segments(year, segment_name, labels, amounts, colors, directory)

def generate_colors(num_segments, amounts):
    """
    Generate color array based on the value (positive or negative) of amounts.
    """
    base_colors = np.linspace(0, 255, num_segments, dtype=int)
    colors = ['#%02x%02x%02x' % (r, g, b) for r, g, b in zip(
        np.round(np.linspace(255, 0, num_segments)).astype(int),
        np.round(np.linspace(102, 204, num_segments)).astype(int),
        np.round(np.linspace(204, 102, num_segments)).astype(int))]
    return [colors[i] if amount >= 0 else colors[-i - 1] for i, amount in enumerate(amounts)]

def plot_segments(year, segment_name, labels, amounts, colors, directory):
    """
    Plot individual bar charts for segments.
    """
    plt.figure(figsize=(10, 6))
    plt.bar(labels, amounts, color=colors)
    plt.xlabel('Segment')
    plt.ylabel('Value (in billions)')
    plt.title(f'{segment_name} in {year}')
    plt.xticks(rotation=45, ha="right")  # Rotate and align labels to prevent overlap
    plt.tight_layout()
    plt.savefig(os.path.join(directory, f'{year}_{segment_name}.png'))
    plt.close()
            
def visualize(ticker, start_year, end_year):
    """
    Main function to manage the flow of data from parsing to plotting.
    """
    data_path = f'data/sec-edgar-filings/{ticker}/10-K'
    insights = {}

    for year_folder in os.listdir(data_path):
        year = get_year(year_folder)
        if year and int(year) >= start_year and int(year) <= end_year:
            filing_path = os.path.join(data_path, year_folder, 'primary-document.html')
            filing_text = parse_filing_text(filing_path)
            analysis = analyze(filing_text)
            insights[year] = extract_total_values(analysis)

    create_bar_plot(ticker, insights)
    create_segment_bar_plots(ticker, insights)

def main():
    """
    Parse command line arguments and initiate visualization process.
    """
    parser = argparse.ArgumentParser(description="Generate insights from 10-K filings")
    parser.add_argument('--ticker', type=str, required=True, help="The company's stock ticker symbol")
    parser.add_argument('--start_year', type=int, required=True, help="The start year for analysis")
    parser.add_argument('--end_year', type=int, required=True, help="The end year for analysis")
    args = parser.parse_args()

    visualize(args.ticker, args.start_year, args.end_year)

if __name__ == '__main__':
    main()
