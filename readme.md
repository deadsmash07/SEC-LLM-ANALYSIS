Project Overview
----------------

This project provides an interactive web application designed to analyze and visualize financial data extracted from 10-K filings of publicly traded companies. The application allows users to select a company by its ticker symbol and specify a range of years for analysis. It then presents detailed financial insights through interactive graphs, aiding stakeholders in understanding the financial health and trends of the company.

Key Features
------------

-   **Data Extraction**: Utilizes SEC filings to pull financial data specific to user queries.
-   **Dynamic Visualizations**: Generates both high-level insights and detailed financial breakdowns through various charts.
-   **User Interaction**: Offers an intuitive web interface for easy access to financial data.



## Demo 
working of the code can be found [here](demo.mp4).
* * * * *

## Command to run the code
To fix the dependencies run the following command:
```
pip3 install -r requirements.txt
```

The application also incorporates `Tailwind CSS` for styling the frontend. Ensure that it's properly installed on your system by following the instructions on the [Tailwind CSS Installation page](https://tailwindcss.com/docs/installation).

Store your API key in a `.env` file at the root of your project directory in the following format: `ANTHROPIC_API_KEY=<YOUR_API_KEY>`.

### Getting Started

To launch the application, execute the following steps:

1.  Clone the repository to your local machine.
2.  Open your command prompt or terminal and navigate to the project directory.
3.  Execute `python3 app.py` to initiate the server.
```python
python3 app.py
```
4.  Access the application by entering `localhost:5000` in your web browser's address bar.
5.  The homepage will display a form where you can input details such as the company's stock ticker. This form is similar to what is shown in the demo videos.
6.  Complete the form and click "Generate Insights" to retrieve and display financial insights for the selected company.

## Directory Structure
```
project-root/
├── webapp/
│   ├── index.html
│   ├── jscode.js
│   ├── style.css
│   └── home.css
|  
├── app.py
├── data_fetch.py
├── prompt.py
├── graphing.py
├── .env 
├── data/
│   └── sec-edgar-filings/
│       └── <ticker>/
├── requirements.txt
├── demo.mp4
├── demo.webm
└── graphs/
    └── <ticker>/
        ├── insights/
        └── detailed/
        └── summary.jason
```

Conclusion
----------

This project leverages the power of data visualization to make complex financial data accessible and understandable. By automating the extraction and visualization processes, it provides valuable insights that can support financial analysis, investment decisions, and educational purposes.