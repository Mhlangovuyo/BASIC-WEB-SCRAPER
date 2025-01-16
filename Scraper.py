import requests
from bs4 import BeautifulSoup

# Function to fetch the page content
def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise HTTPError for bad responses (4xx, 5xx)
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        return None

# Function to extract all links
def extract_links(soup):
    links = []
    for link in soup.find_all('a', href=True):  # Find all <a> tags with href attribute
        href = link['href']
        if href.startswith('http'):  # Filter absolute URLs (could add more logic here)
            links.append(href)
    return links

# Function to extract all headings (h1 to h6)
def extract_headings(soup):
    headings = {}
    for i in range(1, 7):  # Search for h1 to h6 headings
        heading_tags = soup.find_all(f'h{i}')
        headings[f'h{i}'] = [tag.get_text(strip=True) for tag in heading_tags]
    return headings

# Function to save extracted data to a text file
def save_to_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(data)
    print(f"Data saved to {filename}")

# Main function
def main(url):
    print(f"Fetching content from: {url}")
    
    # Fetch the HTML content of the page
    html_content = fetch_page(url)
    if not html_content:
        return
    
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract links and headings
    links = extract_links(soup)
    headings = extract_headings(soup)
    
    # Save the links to a file
    save_to_file('links.txt', '\n'.join(links))
    
    # Save the headings to a file
    headings_content = ""
    for level, heading_list in headings.items():
        headings_content += f"\n{level}:\n" + "\n".join(heading_list) + "\n"
    save_to_file('headings.txt', headings_content)

# Run the script
if __name__ == "__main__":
    # Replace with the URL of the page you want to scrape
    url = 'http://localhost/sample.html'  # Change this to the actual URL if hosted
    main(url)
