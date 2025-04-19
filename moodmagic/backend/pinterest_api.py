import os
import requests
from typing import List
from dotenv import load_dotenv
from config import settings

load_dotenv()

class PinterestAPI:
    def __init__(self):
        self.api_key = os.getenv("PINTEREST_API_KEY")
        self.base_url = "https://api.pinterest.com/v5"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def search_images(self, vibe_text: str, tags: List[str], limit: int = 12) -> List[str]:
        """
        Search Pinterest for images based on vibe text and tags
        Returns a list of image URLs
        """
        try:
            # Combine vibe text and tags for search query
            search_query = f"{vibe_text} {' '.join(tags)} design inspiration"
            
            # For now, return mock data
            return self._get_mock_images(limit)
            
            # Uncomment this when ready to use real API
            # response = requests.get(
            #     f"{self.base_url}/pins/search",
            #     headers=self.headers,
            #     params={
            #         "query": search_query,
            #         "limit": limit,
            #         "fields": "image_url"
            #     }
            # )
            # response.raise_for_status()
            # pins = response.json().get("data", [])
            # return [pin.get("image_url") for pin in pins if pin.get("image_url")]

        except Exception as e:
            print(f"Error searching Pinterest: {e}")
            return self._get_mock_images(limit)

    def _get_mock_images(self, limit: int) -> List[str]:
        """
        Return mock image URLs for testing
        """
        mock_images = [
            "https://i.pinimg.com/564x/8a/71/bf/8a71bf0a5c1a5a0a5c1a5a0a5c1a5a0a.jpg",
            "https://i.pinimg.com/564x/9b/72/c0/9b72c0a5c1a5a0a5c1a5a0a5c1a5a0a.jpg",
            "https://i.pinimg.com/564x/7c/73/d1/7c73d1a5c1a5a0a5c1a5a0a5c1a5a0a.jpg",
            "https://i.pinimg.com/564x/6d/74/e2/6d74e2a5c1a5a0a5c1a5a0a5c1a5a0a.jpg",
            "https://i.pinimg.com/564x/5e/75/f3/5e75f3a5c1a5a0a5c1a5a0a5c1a5a0a.jpg",
            "https://i.pinimg.com/564x/4f/76/04/4f7604a5c1a5a0a5c1a5a0a5c1a5a0a.jpg",
            "https://i.pinimg.com/564x/3d/77/15/3d7715a5c1a5a0a5c1a5a0a5c1a5a0a.jpg",
            "https://i.pinimg.com/564x/2e/78/26/2e7826a5c1a5a0a5c1a5a0a5c1a5a0a.jpg",
            "https://i.pinimg.com/564x/1f/79/37/1f7937a5c1a5a0a5c1a5a0a5c1a5a0a.jpg",
            "https://i.pinimg.com/564x/0a/7a/48/0a7a48a5c1a5a0a5c1a5a0a5c1a5a0a.jpg",
            "https://i.pinimg.com/564x/fb/7b/59/fb7b59a5c1a5a0a5c1a5a0a5c1a5a0a.jpg",
            "https://i.pinimg.com/564x/ec/7c/6a/ec7c6aa5c1a5a0a5c1a5a0a5c1a5a0a.jpg",
            "https://i.pinimg.com/564x/dd/7d/7b/dd7d7ba5c1a5a0a5c1a5a0a5c1a5a0a.jpg",
            "https://i.pinimg.com/564x/ce/7e/8c/ce7e8ca5c1a5a0a5c1a5a0a5c1a5a0a.jpg",
            "https://i.pinimg.com/564x/bf/7f/9d/bf7f9da5c1a5a0a5c1a5a0a5c1a5a0a.jpg"
        ]
        return mock_images[:limit]

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def fetch_images(vibe_text: str, tags: List[str]) -> List[str]:
    """
    Fetch image URLs from Pinterest using SerpAPI.
    Returns a list of image thumbnail URLs.
    """
    try:
        if not SERPAPI_KEY or SERPAPI_KEY == "your_serpapi_key":
            print("Warning: Using fallback images due to missing or invalid SERPAPI_KEY")
            return get_fallback_images()

        # Construct search query
        query = f"site:pinterest.com {vibe_text} " + " ".join(tags)
        
        # Set up SerpAPI parameters
        params = {
            "q": query,
            "engine": "google",
            "tbm": "isch",
            "ijn": "0",
            "api_key": SERPAPI_KEY
        }
        
        # Make API request
        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()
        
        # Parse response and extract thumbnail URLs
        data = response.json()
        images = []
        
        for img in data.get("images_results", [])[:9]:  # Get top 9 images
            if "original" in img:
                images.append(img["original"])
            elif "thumbnail" in img:
                images.append(img["thumbnail"])
                
        return images if images else get_fallback_images()

    except Exception as e:
        print(f"Error fetching images: {e}")
        return get_fallback_images()

def get_fallback_images() -> List[str]:
    """Return a list of fallback image URLs for the futuristic brutalist theme."""
    return [
        "https://i.pinimg.com/736x/a1/b2/c3/futuristic-brutalist-1.jpg",
        "https://i.pinimg.com/736x/d4/e5/f6/minimal-concrete-structure-2.jpg",
        "https://i.pinimg.com/736x/g7/h8/i9/organic-brutalism-3.jpg",
        "https://i.pinimg.com/736x/j0/k1/l2/sci-fi-architecture-4.jpg",
        "https://i.pinimg.com/736x/m3/n4/o5/modern-brutalist-5.jpg"
    ]

def fetch_pinterest_images(query: str, count: int = 5) -> list:
    """
    Fetch images from Pinterest using SerpAPI
    """
    params = {
        "engine": "pinterest",
        "q": query,
        "api_key": settings.SERPAPI_KEY
    }
    
    try:
        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract image URLs from the response
        images = []
        if "pins" in data:
            for pin in data["pins"][:count]:
                if "images" in pin and "orig" in pin["images"]:
                    images.append(pin["images"]["orig"]["url"])
        
        return images
        
    except Exception as e:
        print(f"Error fetching Pinterest images: {str(e)}")
        return []

# Example usage
if __name__ == "__main__":
    vibe = "minimalist scandinavian"
    tags = ["modern", "cozy", "neutral"]
    
    images = fetch_images(vibe, tags)
    print(f"\nFetched {len(images)} images:")
    for i, url in enumerate(images, 1):
        print(f"{i}. {url}") 