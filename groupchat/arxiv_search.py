# filename: arxiv_search.py

import feedparser
import re
import datetime

# Function to search arXiv for papers related to GPT-4
def search_arxiv(query, max_results=10):
    base_url = 'http://export.arxiv.org/api/query?'
    search_query = f'all:{query}'
    start = 0
    max_results = max_results
    query = f'search_query={search_query}&start={start}&max_results={max_results}'
    response = feedparser.parse(base_url + query)
    return response.entries

# Function to extract potential applications from the abstract
def extract_applications(text):
    # Simple heuristic: look for sentences that mention "application" or "software"
    sentences = re.split(r'\. |\.\n', text)
    applications = [sentence for sentence in sentences if re.search(r'\b(application|software)\b', sentence, re.IGNORECASE)]
    return applications

# Search for the most recent GPT-4 papers
papers = search_arxiv('GPT-4', max_results=5)

# Find the most recent paper
most_recent_paper = max(papers, key=lambda paper: datetime.datetime.strptime(paper.published, '%Y-%m-%dT%H:%M:%SZ'))

# Extract potential applications from the abstract
applications = extract_applications(most_recent_paper.summary)

# Output the title, authors, published date, and potential applications
print(f"Title: {most_recent_paper.title}")
print(f"Authors: {', '.join(author.name for author in most_recent_paper.authors)}")
print(f"Published Date: {most_recent_paper.published}")
print("Potential Applications in Software Development:")
for app in applications:
    print(f"- {app}")

# If no applications are found in the abstract, inform the user
if not applications:
    print("No explicit mention of potential applications in software development found in the abstract.")