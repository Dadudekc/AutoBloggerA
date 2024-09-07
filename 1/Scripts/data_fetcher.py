import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import base64

# Retry strategy setup
retry_strategy = Retry(
    total=3,  # Number of retries
    backoff_factor=1,  # Delay between retries
    status_forcelist=[429, 500, 502, 503, 504],  # Retry on certain status codes
    allowed_methods=["HEAD", "GET", "OPTIONS"]  # Use allowed_methods instead of method_whitelist
)

adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

def fetch_journal_entry_data():
    # Temporary mock API for testing
    api_url = "https://jsonplaceholder.typicode.com/posts/1"  # Replace this with actual API later
    try:
        response = http.get(api_url)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def publish_to_wordpress(title, content):
    url = 'https://tradingrobotplug.com/wp-json/wp/v2/posts'
    
    # Authorization: Either use Application Password or API Key
    headers = {
        'Authorization': 'Basic ' + base64.b64encode('your_username:your_password'.encode()).decode(),
        'Content-Type': 'application/json'
    }
    
    data = {
        'title': title,
        'content': content,  # Ensure the content is properly formatted in HTML
        'status': 'publish'
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print('Post published successfully!')
    else:
        print(f'Failed to publish post: {response.status_code}, Error: {response.text}')

if __name__ == "__main__":
    # Fetch the journal entry data (using mock data from JSONPlaceholder)
    data = fetch_journal_entry_data()
    
    if data:
        print(f"Journal data fetched: {data}")
        # Example publishing to WordPress with fetched content
        title = data['title']
        content = f"<p>{data['body']}</p>"
        publish_to_wordpress(f"Journal Entry - {title}", content)
    else:
        print("Failed to fetch data.")
