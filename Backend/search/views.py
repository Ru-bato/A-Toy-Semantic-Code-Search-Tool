import aiohttp
import asyncio
import spacy
import xmltodict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# load spaCy NLP model
nlp = spacy.load("en_core_web_sm")


# def split_terms(text):
#     # 使用正则表达式将"deep learning"替换为"deep learning"
#     replacements = {
#         r'\bdeeplearning\b': 'deep learning',
#         r'\bmachinelearning\b': 'machine learning',
#         r'\bdatabsse\b': 'data base',
#     }
#
#     for pattern, replacement in replacements.items():
#         text = re.sub(pattern, replacement, text)
#
#     return text


# extract keywords through natural language by spaCy
def extract_keywords(natural_query):
    # processed_query = split_terms(natural_query)

    doc = nlp(natural_query)
    keywords = [token.lemma_ for token in doc if token.pos_ in ('NOUN', 'VERB', 'ADJ')]

    return " ".join(keywords)


# async call function
async def fetch(session, url, headers=None, proxy=None):
    try:
        async with session.get(url, headers=headers, proxy=proxy) as response:
            response.raise_for_status()
            content_type = response.headers.get('Content-Type', '')
            if 'application/atom+xml' in content_type:
                # 处理 XML 响应
                xml_content = await response.text()
                return xmltodict.parse(xml_content)  # 解析 XML
            elif 'application/json' in content_type:
                # 处理 JSON 响应
                return await response.json()
            else:
                return {'error': f'Unexpected Content-Type: {content_type}'}
    except aiohttp.ClientResponseError as e:
        print(f'HTTP Error: {e.status}, message: {e.message}, url: {url}')
        return {'error': f'HTTP Error: {e.status}, message: {e.message}, url: {url}'}
    except aiohttp.ClientConnectorError as e:
        print(f'Connection Error: {str(e)}, url: {url}')
        return {'error': f'Connection Error: {str(e)}, url: {url}'}
    except Exception as e:
        print(f'Unexpected Error: {str(e)}, url: {url}')
        return {'error': f'Unexpected Error: {str(e)}, url: {url}'}


@csrf_exempt
async def integrated_search(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'GET method required'}, status=405)

    search_query = request.GET.get('query', '')
    selected_languages = request.GET.getlist('languages')
    selected_languages = [lang.strip() for lang in selected_languages if lang.strip()]

    def format_languages(selected_languages):
        formatted_languages = []
        for lang in selected_languages:
            cleaned_lang = lang.strip()
            if cleaned_lang:  # 确保非空
                formatted_languages.append(f'language:{cleaned_lang};')
        return '+'.join(formatted_languages)

    # language_filter = format_languages(selected_languages)
    print(selected_languages)
    if not search_query:
        return JsonResponse({'error': 'No search query provided'}, status=400)

    search_keywords = extract_keywords(search_query)
    print('qu', search_keywords)

    # 生成语言过滤字符串，确保每个语言都有独立的 language:
    language_filter = '+'.join(
        [f'language:{lang.strip()}' for lang in ','.join(selected_languages).split(',') if lang.strip()]
    )

    # 格式化搜索关键词，确保没有空格
    search_query = f"{search_keywords}" + (f"+{language_filter}" if language_filter else "")
    print(search_query)
    if not search_query.strip():  # 如果生成的搜索查询为空
        return JsonResponse({'error': 'Search query cannot be empty'}, status=400)

    # GitHub Code API URL
    github_code_url = f'https://api.github.com/search/code?q={search_query}&sort=stars&order=desc'

    # GitHub Repositories API URL
    github_repo_url = f'https://api.github.com/search/repositories?q={search_query}&sort=stars&order=desc'

    # StackOverflow API
    tagged_languages = [lang for lang in selected_languages if lang]  # 去掉空值
    stackoverflow_url = f'https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q={search_keywords}' + (
        f'&tagged={"&".join(tagged_languages).replace(",", ";")}' if tagged_languages else '') + '&site=stackoverflow'

    # # Google Books API
    # google_books_url = f'https://www.googleapis.com/books/v1/volumes?q={search_keywords}' if search_keywords else None

    # ArXiv API
    arxiv_url = f'http://export.arxiv.org/api/query?search_query={search_keywords}&start=0&max_results=10'

    print(stackoverflow_url)
    # YouTube API (ignore language)
    youtube_api_key = 'AIzaSyDKluleDSzp3X1ASjItx9L5yNwgEZ9Kudg'
    youtube_url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={search_keywords}&key={youtube_api_key}&maxResults=6'

    print(github_repo_url)
    github_headers = {
        'User-Agent': 'Ru-bato',
        'Authorization': 'Bearer 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',
        'Accept': 'application/vnd.github.v3+json',
    }
    stackoverflow_headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
    }
    proxy = "http://127.0.0.1:7890"

    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch(session, github_code_url, headers=github_headers, proxy=proxy),
            fetch(session, stackoverflow_url, headers=stackoverflow_headers, proxy=proxy),
            fetch(session, youtube_url, proxy=proxy),
            fetch(session, github_repo_url, headers=github_headers, proxy=proxy),
            fetch(session, arxiv_url, proxy=proxy),
        ]

        # Fetch all except Google Books API
        responses = await asyncio.gather(*tasks, return_exceptions=True)

    # 处理 API 请求结果
    github_code_response = responses[0] if not isinstance(responses[0], Exception) else {
        'error': 'GitHub Code API failed'}
    stackoverflow_response = responses[1] if not isinstance(responses[1], Exception) else {
        'error': 'StackOverflow API failed'}
    youtube_response = responses[2] if not isinstance(responses[2], Exception) else {'error': 'YouTube API failed'}
    github_repo_response = responses[3] if not isinstance(responses[3], Exception) else {
        'error': 'GitHub Repositories API failed'}
    arxiv_response = responses[4] if not isinstance(responses[4], Exception) else {
        'error': 'ArXiv API failed'}

    # 特判 ArXiv 的响应
    if 'feed' in arxiv_response and 'entry' in arxiv_response['feed']:
        arxiv_entries = arxiv_response['feed']['entry']
    else:
        arxiv_entries = []  # 如果没有符合格式的条目，返回空列表

    result = {
        'github_code': github_code_response.get('items', []),
        'github_repositories': github_repo_response.get('items', []),
        'stackoverflow': stackoverflow_response.get('items', []),
        'youtube_tutorials': youtube_response.get('items', []),
        'arxiv_results': arxiv_entries,  # 使用特判后的结果
    }

    return JsonResponse(result)
