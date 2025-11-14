def get_themed_images(theme, per_page, size="small"):
    import httpx
    from os import getenv
    from dotenv import load_dotenv

    load_dotenv()
    pexels_api_key = getenv("PEXELS_API_KEY")
    headers = {
    "Authorization": pexels_api_key
    }
    url = "https://api.pexels.com/v1/search"
    params = {
    "query": theme,
    "per_page": per_page,
    "page": 1
    }
    response = httpx.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        image_urls = [photo['src'][size] for photo in data['photos']]
        return image_urls
    else:
        return []