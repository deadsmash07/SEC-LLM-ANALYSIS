from flask import Flask, request, jsonify, send_from_directory
from fetch_10k import download_10k_filings
import os
import subprocess
app = Flask(__name__, static_url_path='', static_folder='frontend')

@app.route('/')
def serve_frontend():
    return send_from_directory('frontend', 'index.html')

@app.route('/generate-insight', methods=['POST'])
def generate_insight():
    data = request.get_json()
    company = data['company']
    email = data['email']
    ticker = data['ticker']
    from_year = int(data['fromYear'])
    to_year = int(data['toYear'])

    try:
        # Fetch the 10-K filings
        download_10k_filings(company, email, ticker, from_year, to_year)
        # Perform text analysis and visualization
        command = f'python3 visualize.py --ticker="{ticker}" --start_year={from_year} --end_year={to_year}'
        print(command)
        subprocess.run(command, check=True, shell=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Return success with the path to generated visualization and latest insights
    return jsonify({
        'success': 'Visualization generated successfully'
       
    }), 200

@app.route('/visualizations/<path:path>')
def serve_visualizations(path):
    return send_from_directory('visualizations', path)

@app.route('/get-plots', methods=['GET'])
def get_plots():
    ticker = request.args.get('ticker')
    visualization_path = f'visualizations/{ticker}/insights'
    if not os.path.exists(visualization_path):
        return jsonify([]), 404

    plot_files = [{'title': f[:-4], 'path': f'visualizations/{ticker}/insights/{f}'} for f in os.listdir(visualization_path) if f.endswith('.png')]
    return jsonify(plot_files)

@app.route('/get-detailed-plots', methods=['GET'])
def get_detailed_plots():
    ticker = request.args.get('ticker')
    visualization_path = f'visualizations/{ticker}/detailed'
    if not os.path.exists(visualization_path):
        return jsonify([]), 404
    
    plot_files = [{'title': f[:-4], 'path': f'visualizations/{ticker}/detailed/{f}'} for f in sorted(os.listdir(visualization_path)) if f.endswith('.png')]
    print(jsonify(plot_files))
    return jsonify(plot_files)

if __name__ == '__main__':
    app.run(port=5000)
