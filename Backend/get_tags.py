import requests


def get_stackoverflow_tags():
    url = "https://api.stackexchange.com/2.3/tags?order=desc&sort=popular&site=stackoverflow"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        tags = [tag['name'] for tag in data['items']]
        return tags
    else:
        print("Error:", response.status_code)
        return []


tags = get_stackoverflow_tags()
print(tags)