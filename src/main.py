import requests

# Define the endpoint
url = "https://en.wikipedia.org/w/api.php"

# Step 1: Fetch the page content to get image file names
params = {
    "action": "query",
    "format": "json",
    "titles": "Black Hills State Yellow Jackets",
    "prop": "images"
}

response = requests.get(url, params=params)
data = response.json()

page = next(iter(data['query']['pages'].values()))
images = page.get('images', [])

logo_filename = None
for image in images:
    if "logo" in image['title'].lower():
        logo_filename = image['title']
        break

if logo_filename:
    # Step 2: Get the URL of the logo image
    params = {
        "action": "query",
        "format": "json",
        "titles": logo_filename,
        "prop": "imageinfo",
        "iiprop": "url"
    }

    response = requests.get(url, params=params)
    data = response.json()

    page = next(iter(data['query']['pages'].values()))
    image_info = page.get('imageinfo', [])

    if image_info:
        logo_url = image_info[0]['url']
        print(f"Logo URL: {logo_url}")

        # Step 3: Download the logo image
        response = requests.get(logo_url)
        with open("bhsu_logo.png", "wb") as file:
            file.write(response.content)

        print("Logo image downloaded and saved as bhsu_logo.png")
    else:
        print("Image URL not found.")
else:
    print("Logo image not found.")
