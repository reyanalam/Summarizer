import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def fetch_webpage(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}  
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching webpage: {e}"

def extract_content(html):
    
    soup = BeautifulSoup(html, 'html.parser')
    paragraphs = soup.find_all('p')
    text = '\n'.join([para.get_text() for para in paragraphs])
    return text if text else "No content found"

def summarize_text(text, sentence_count=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return " ".join(str(sentence) for sentence in summary)

def main():
    url = input("Enter the URL: ")
    html = fetch_webpage(url)
    if "Error" in html:
        print(html)
        return
    
    content = extract_content(html)
    print("\nExtracted Content:\n", content[:1000], "...")  
    
    summary = summarize_text(content)
    print("\nSummary:\n", summary)

if __name__ == "__main__":
    print("Script is running...")
    main()
