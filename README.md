# Mercor Challenge - Github Automated Analyzer

## Project Description
This project aims to build a Python-based tool that utilizes the power of GPT and LangChain to analyze GitHub repositories 
and identify the most technically complex and challenging repository from a given user's profile. The tool will take a GitHub user's URL 
as input and perform an in-depth assessment of each repository, considering factors such as code structure, complexity, and other relevant metrics.

## Overview
This project is a Python-based tool that helps you find the most technically complex and challenging repository from a given GitHub user's profile.
The tool utilizes the power of GPT and LangChain to assess each repository individually before determining the most technically challenging one.

## Requirements
Before using the tool, ensure you have the following installed:

* Python 3.x
* Pip package manager

## How It Works
1. **User Input:** The tool prompts the user to enter a GitHub user's URL.
2. **Fetching Repositories:** The tool fetches all repositories from the provided GitHub user's profile using the GitHub API.
3. **Assessing Complexity:** For each repository, the tool leverages GPT and LangChain to assess its technical complexity and challenge level.
4. **Determining the Most Challenging:** After evaluating all repositories, the tool selects the one with the highest complexity score as the most technically challenging repository.
6. **Output:** The tool displays the name of the most challenging repository along with a direct link to it on GitHub.
## Installation
Clone this repository to your local machine.<br/>
Install the required dependencies by running the following command:
'
```
pip install -r requirements.txt
```

### Usage
Run the application using the following command:
```
streamlit run app.py
```
In the web interface, enter the GitHub user's URL and click on "Enter".<br/>
The tool will process the information and display the most technically challenging repository from the user's profile.

## Dependencies
The tool uses the following major dependencies:

* Python 3.9 
* Streamlit
* PyGitHub
* GPT (OpenAI GPT-3 or later version)
* LangChain
