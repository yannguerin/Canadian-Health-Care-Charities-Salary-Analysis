# Canadian Health-Care Charities Salary Analysis

# Project Organization

## Charity Scraping
This folder contains all of the scripts for scraping the data from the Canada Revenue Agency Website. I first scraped all of the detailed charity information for all 60,000+ registered charities in Canada. I then extracted all of the Registration Numbers for Health-Care related charities in Canada. For each Health-Care related charity, I scraped their financial data for up to five reporting periods (yearly reports). All of the data was saved as JSON files, then uploaded to MongoDB.

**detailed_charity_list.py** - Scrapes the detailed charity info from each page in the advanced search of the Canada Revenue Agency website.
**scrape_all_charities.py** - Scrapes the financial data for each of the 6300+ health-care related charities in Canada.

## Charity Analysis
I first started by cleaning the data. I normalized all of the JSON documents into CSV, handled the missing data and manually fixed a few incorrect data points (incorrectly reported by the charity). After the cleaning, I had a CSV file containing all the data about health-care charities.

Then I began exploring the data with distribution plots for various columns, box and violin plots to better understand the distribution of salaries based on various factors. After thorough exploration, I began to analyze the charities in relation to Lung Cancer Canada. Finally, I produced a report for Lung Cancer Canda showing them where they stand with regard to salaries in relation to other health-care charities in Canada. I delivered this report to the President of Lung Cancer Canada - Stephanie Snow.

**health_care_charities_cleaning_and_exploration.ipynb** - Notebook where I did the data cleaning and preprocessing
**feature_creation** - Creating new interesting features to explore
**exploratory_charity_analysis.ipynb** - The initial exploration of the data, contains a mess of code and plots that I refined for the Exploratory Report and Final Report
**Exploratory Report on Health Care Charities in Canada.ipynb** - An exploration of the data, intended to be read by the Board of Directors at Lung Cancer Canada

---

**Lung Cancer Canada Final Report.pdf** - The Final Report I gave to the President of Lung Cancer Canada - Stephanie Snow

A note regarding the organization within the files: Lung Cancer Canada wanted quick results, and wanted an exploratory report on the salary data. They werent interested in fancy modeling nor having a project that could be re-run regularly, therefore I prioritized the speed of my analysis over properly commented code and reproducible results.

# Overview
Lung Cancer Canada, a charity located in Toronto, asked me to analyze the distribution of top salaries for all Health-Care charities in Canada. I scraped the data from the registered charities website of Revenue Canada, scraping financial statements for over 6000 charities for up to 5 years back. I prepared an exploratory analysis of the Health Care charities, along with a detailed analysis of the relationship between top salaries and other factors such as: Revenue, Expenses, Government Funding, number of employees...

# Result
Lung Cancer Canada wanted to make sure that their salaries were in-line with other similar charities in Canada before moving forward with raises for their employees. The data demonstrated that based on certain factors they were paying too little to their employees, but based on others they may be paying a bit too much. The President of Lung Cancer Canada, Dr. Stephanie Snow, was pleased with the analysis and provide me with the following recommendation:

"Yann quickly turned an idea, a question, about salaries at health care charities in Canada, into a comprehensive dataset and associated analysis. His ability to extract rich but seemingly inaccessible data from the Canada Revenue Agency website and turn it into a comprehensive analysis of salaries at these charities, helped us at Lung Cancer Canada better understand where we stand among our peer organizations." - Dr. Stephanie Snow