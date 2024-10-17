import aiohttp
import asyncio
from aiohttp import ClientTimeout
from django.http import JsonResponse

# Set headers and proxy, so that APIs form Stack Overflow, GitHub and Reddit can work.
# API from Dev.to can work whether headers and proxy are set or not.
TIMEOUT = ClientTimeout(total=10)


# Get hot questions from Stack Overflow
# Reference: https://api.stackexchange.com/
async def fetch_from_stackoverflow():
    url = 'https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow&pagesize=5'
    headers = {
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    proxy = "http://127.0.0.1:7890"
    try:
        async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
            async with session.get(url, headers=headers, proxy=proxy) as response:
                response.raise_for_status()
                data = await response.json()
                return [
                    {
                        'title': item['title'],
                        'link': item['link'],
                        'source': 'Stack Overflow'
                    }
                    for item in data.get('items', [])
                ]
    except Exception as e:
        print(f"Error fetching from Stack Overflow: {e}")
        return []


# Get popular repositories from GitHub
# Reference: https://docs.github.com/en/rest?apiVersion=2022-11-28
async def fetch_from_github():
    url = 'https://api.github.com/search/repositories?q=stars:>1&sort=stars&order=desc&per_page=5'
    headers = {
        'User-Agent': 'Ru-bato',
        'Authorization': 'Bearer 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',
        'Accept': 'application/vnd.github.v3+json'
    }
    try:
        async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
            async with session.get(url, headers=headers, proxy="http://127.0.0.1:7890") as response:
                response.raise_for_status()  # 检查响应状态
                data = await response.json()
                return [
                    {
                        'title': item.get('name'),
                        'link': item.get('html_url'),
                        'source': 'GitHub'
                    }
                    for item in data.get('items', [])
                ]
    except Exception as e:
        print(f"Error fetching from GitHub: {e}")
        return []


# Get popular developer articles from Dev.to
# Reference: https://dev.to/guilhermecheng/how-to-use-devto-api-4p65
async def fetch_from_dev_to():
    url = 'https://dev.to/api/articles?per_page=5'
    try:
        async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
            async with session.get(url) as response:
                response.raise_for_status()  # 检查响应状态
                data = await response.json()
                return [
                    {
                        'title': item['title'],
                        'link': item['url'],
                        'source': 'Dev.to'
                    }
                    for item in data
                ]
    except Exception as e:
        print(f"Error fetching from Dev.to: {e}")
        return []


async def get_popular_code_examples(request):
    # Run the fetch functions concurrently
    tasks = [
        fetch_from_stackoverflow(),
        fetch_from_github(),
        fetch_from_dev_to(),
    ]

    results = await asyncio.gather(*tasks)
    # Flatten the results
    flattened_results = [item for sublist in results for item in sublist]

    return JsonResponse({'results': flattened_results})
