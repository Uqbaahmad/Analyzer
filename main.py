import streamlit as st
# from fetch_file import fetch_github_repositories


import requests
import openai
import radon.metrics
import re
from github import Github

# from setup import calculate_complexity_with_gpt
import os
# from secret_key.api_key import OPENAI_SECRET_KEY
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Set the OpenAI API key in the environment variable.
os.environ["OPENAI_API_KEY"] = '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'

def calculate_complexity_with_gpt(code):
    prompt = PromptTemplate(
        input_variables=['code'], 
        template="Calculate the complexity of the given code and return the complexity in a float value without any explanation.")
    llm = OpenAI(temperature=0.8)

    # Create a Language Model Chain with the GPT-3.5 model and the prompt template.
    chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    return chain.run(code)


def fetch_repositories(github_url):
    user = github_url.split('/')[-1]
    response = requests.get(f'https://api.github.com/users/{user}/repos')
    if response.status_code == 200:
        repositories = response.json()
        repository_names = [repo['name'] for repo in repositories]
        return repository_names
    else:
        print(f"Failed to fetch repositories for user '{user}'. Error: {response.text}")
        return [] 


def calculate_complexity_of_repository(github_url, repository_name):
    username = github_url.split('/')[-1]

    score = 0.0
    response = requests.get(f'https://api.github.com/repos/{username}/{repository_name}/contents')

    if response.status_code == 200:
        contents = response.json()        
        for item in contents:
            print(item)
            if item['type'] == 'file':
                file_path = item['path']
                file_response = requests.get(f'https://raw.githubusercontent.com/{username}/{repository_name}/master/{file_path}')
                
                if file_response.status_code == 200:
                    file_contents = file_response.text

                    file_contents = re.sub(r'#.*', '', file_contents)

                    # Remove import statements
                    file_contents = re.sub(r'^import.*$', '', file_contents, flags=re.MULTILINE)
                    file_contents = re.sub(r'^from.*$', '', file_contents, flags=re.MULTILINE)

                    # Remove empty lines and leading/trailing whitespaces
                    file_contents = '\n'.join(line.strip() for line in file_contents.split('\n') if line.strip())
                    
                    try:
                        if '.py' in item['name']:
                            score += float(calculate_complexity_with_gpt(file_contents))
                        else :
                            score += float(calculate_complexity(file_contents, file_path))
                    except:
                        score += float(calculate_complexity(file_contents, file_path))
                else:
                    print(f"Failed to fetch contents of file '{file_path}'. Error: {file_response.text}")
    else:
        print(f"Failed to fetch contents of repository '{repository_name}'. Error: {response.text}")
    return score

import radon.metrics

def calculate_complexity(code, filepath=None):
    try:
        complexity = radon.metrics.cc_visit(code)
        return complexity
    except Exception as e:
        print(e)
        print(f"Failed to calculate complexity for file '{filepath}'.")
        return 0

def fetch_github_repositories(github_url):
    # Initialize variables to store the most complex repository
    most_complex_repo = None
    most_complex_score = -1

    try:
        # Parse the username from the GitHub URL
        username = github_url.split('/')[-1]

        # Initialize the GitHub API client
        g = Github()

        # Get the user object
        user = g.get_user(username)

        # Fetch all repositories for the user
        repositories = user.get_repos()

        # Find the most complex repository based on your criteria (e.g., stars, forks, size, etc.)
        for repo in repositories:
            complex_score = repo.stargazers_count + repo.forks_count
            if complex_score > most_complex_score:
                most_complex_repo = repo
                most_complex_score = complex_score

        if most_complex_repo:
            return most_complex_repo.full_name, most_complex_repo.html_url
        else:
            return None, None

    except Exception as e:
        print("Error:", e)
        return None, None

def get_user_input():
    # Display the title and input box for GitHub user URL in the web interface.
    st.title('Github Automated Analysis')
    github_url = st.text_input("Please Enter The GitHub User's URL")
    return github_url

def main():
    st.title("Welcome to the GitHub Repository Analyzer")   
    st.write("""This Python-based tool is designed to help you find the most technically complex and challenging repository from a given GitHub user's profile. Just enter the GitHub user's URL in the input box below and click the "Enter" to get started.""")

    st.write("""Once you enter the URL, our tool tool uses GPT and LangChain to assess each repository individually and find the most challenging one.""")
             
    st.write("""After analyzing all the repositories, the tool will determine and display the most technically challenging repository, allowing you to gain insights into the user's most sophisticated work.""")
             
    st.write("""We hope this tool helps you discover exceptional repositories and connect with top-notch developers in the GitHub community.""")

    st.write("Get started now. Happy exploring!")


    github_url = get_user_input()

    if github_url:
        most_complex_repository_name, most_complex_repository_link = fetch_github_repositories(github_url)

        if most_complex_repository_name and most_complex_repository_link:
            st.write(f"The most technically complex repository from user '{github_url}' is '{most_complex_repository_name}'.\n")
            st.write(f"Here is the direct link to the repository: [{most_complex_repository_name}]({most_complex_repository_link})")
        else:
            st.write("Oops!!! Some Error Occurred")

if __name__ == "__main__":
    main()


