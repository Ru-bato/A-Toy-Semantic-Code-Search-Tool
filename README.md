# A Toy Semantic Code Search Tool

## 1. 项目背景

本项目允许用户在起始页面输入自然语言进行查询，系统能够智能地寻找有用的源代码示例、相关的在线学习材料、视频等，帮助用户提升编程能力。

本项目使用 `Web API` 获得数据，并对多个 `Web API` 在后端进行了集成。同时，项目也使用了多个 `Python` 和 `Typescript` 的库，并设置接口，让前端与后端能够通信，以实现功能。

## 2. 项目概述

### 2.1 项目地址

https://github.com/Ru-bato/A-Toy-Semantic-Code-Search-Tool

### 2.2 主要功能点简述

- 支持自然语言搜索
- 设置偏好的编程语言和筛选方式
- 根据多个来源的热门标签生成词云
- 点击词云中的标签，跳转到对应网页
- 展示多个来源的热门代码示例，点击可跳转
- 展示搜索结果，包括代码、仓库、问答、书籍、视频五个模块
- 支持登录、注册、收藏、历史记录（注：收藏、历史记录可以正常使用，但没有编写展示界面）

### 2.3 项目结构

- **前端结构**

![Frontend](images/frontend.png)

- **后端结构**

![Backend](images/backend.png)

### 2.4 技术栈

- **前端**

  - **Vue 3**
  - **Element Plus**
  - **TypeScript**
  - **Axios**

- **后端**

  - **Django**
  - **Django REST Framework**
  - **aiohttp**

- **自然语言处理**

  - **spaCy**

- **工具与环境**
  - **VS Code**
  - **Pycharm**

### 2.5 项目依赖

- **前端**

  - axios@1.7.7
  - element-plus@2.8.3
  - typescript@5.4.5
  - vite@5.4.8
  - vue-router@4.4.5
  - vue@3.5.8
  - vuex@4.0.2
  - wordcloud@1.2.2

- **后端**
  - aiohttp==3.9.3
  - Django==5.1.1
  - Flask==3.0.1
  - keras==3.2.0
  - pandas==2.2.1
  - requests==2.31.0
  - spacy==3.8.2

## 3. 功能模块实现

### 3.1 搜索模块

#### 3.1.1 模块简述

搜索模块是项目的核心模块，它承担了项目的最重要的搜索功能。

搜索模块分为`搜索框`、`设置`和`展示页面`三部分。
搜索框位于顶部栏，这是一个在不同页面的通用栏，因此在不同页面都可以进行搜索。
设置也位于顶部栏，可以设置偏好编程语言和筛选条件。可选的偏好编程语言包括`Javascript`, `Python`, `Java`, `C#`, `C++`, `C`, `Ruby`, `PHP`, `Go`, `None`（不限制）；筛选条件包括`Most popular`, `Newest`两项。
展示页面是搜索成功后会跳转到的页面。这里有 5 个展示框，分别用于展示`代码`、`仓库`、`问答`、`书籍`、`视频`，每一项展示内容都可以点击跳转到它的来源。

#### 3.1.2 设计与实现

##### 3.1.2.1 前端

通过`搜索框`的自然语言输入和`设置`的选择，点击搜索按钮时，以参数的形式传递给`展示页面`，代码如下：

```typescript
const handleSearch = () => {
  if (searchQuery.value) {
    router.replace({
      name: "searchResults",
      query: {
        q: searchQuery.value,
        languages: selectedLanguages.value,
        sort: selectedSort.value,
      },
    });
  }
};
```

`展示页面`接收数据并调用接口，将数据传给后端。这个接口继承了 5 个 API，对应展示页面的 5 个展示框的内容。发出请求后，前端通过接口获得数据，并分别展示在 5 个展示框中。代码如下：

```typescript
const fetchSearchResults = async () => {
  if (!searchQuery.value.trim() && selectedLanguages.value.length === 0) {
    console.warn("No search query or languages selected.");
    return; // 不发送请求
  }

  const languageParam =
    selectedLanguages.value.length > 0 &&
    !selectedLanguages.value.includes("none")
      ? `&languages=${selectedLanguages.value.join(",")}`
      : "";

  const response = await fetch(
    `${apiUrl}/search/integrated_search?query=${searchQuery.value}${languageParam}&sort=${sortOption.value}`
  );

  const data = await response.json();

  githubCodeResults.value = data.github_code;
  githubRepoResults.value = data.github_repositories;
  stackoverflowResults.value = data.stackoverflow;
  youtubeResults.value = data.youtube_tutorials;
  googleBooksResults.value = data.google_books;
};
```

##### 3.1.2.2 后端

后端接收到前端传来的信息时，首先需要调用`spaCy`自然语言处理库，用于关键词提取，提取出名词、动词和形容词作为关键词，以便进行更精确的搜索。

完成提取后，把关键词以及其他参数，传递给 5 个 API，分别是`GitHub Code`, `GitHub Repositories`/`Stack Overflow`, `YouTube`和`ariv`。

使用`aiohttp`库，通过`async`和`await`实现并发 API 请求。这样可以在等待某个 API 返回数据时，继续处理其他 API 的请求，从而显著提高数据获取的效率。此外，后端进行了适当的错误处理，这样某个 API 出错时，其他 API 的请求可以正常继续，前端也能看到对应的错误码。

代码如下：

```python
# extract keywords through natural language by spaCy
def extract_keywords(natural_query):
    doc = nlp(natural_query)
    keywords = [token.lemma_ for token in doc if token.pos_ in ('NOUN', 'VERB', 'ADJ')]
    return " ".join(keywords)


# async call function
async def fetch(session, url, headers=None, proxy=None):
    try:
        async with session.get(url, headers=headers, proxy=proxy) as response:
            response.raise_for_status()
            return await response.json()
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
    print(selected_languages)
    if not search_query:
        return JsonResponse({'error': 'No search query provided'}, status=400)

    search_keywords = extract_keywords(search_query)
    # 生成语言过滤字符串，确保每个语言都有独立的 language:
    language_filter = '+'.join([f'language:{lang}' for lang in selected_languages if lang and lang != 'none'])

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
    stackoverflow_url = f'https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q={search_keywords}' + (
        f'&tagged={"|".join(selected_languages)}' if selected_languages else '') + '&site=stackoverflow'
    # Google Books API
    google_books_url = f'https://www.googleapis.com/books/v1/volumes?q={search_keywords}' if search_keywords else None

    # YouTube API (ignore language)
    youtube_api_key = 'AIzaSyARMv3a48r16NNvJyZgq5KA18-xpKI89hM'
    youtube_url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={search_keywords}&key={youtube_api_key}'

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
        ]

        # Fetch all except Google Books API
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        # Delay for Google Books API
        await asyncio.sleep(1)

        # Fetch Google Books API
        google_response = await fetch(session, google_books_url, proxy=proxy)

    # 处理 API 请求结果
    github_code_response = responses[0] if not isinstance(responses[0], Exception) else {
        'error': 'GitHub Code API failed'}
    stackoverflow_response = responses[1] if not isinstance(responses[1], Exception) else {
        'error': 'StackOverflow API failed'}
    youtube_response = responses[2] if not isinstance(responses[2], Exception) else {'error': 'YouTube API failed'}
    github_repo_response = responses[3] if not isinstance(responses[3], Exception) else {
        'error': 'GitHub Repositories API failed'}
    google_books_response = google_response if not isinstance(google_response, Exception) else {
        'error': 'Google Books API failed'}

    result = {
        'github_code': github_code_response.get('items', []),
        'github_repositories': github_repo_response.get('items', []),
        'stackoverflow': stackoverflow_response.get('items', []),
        'youtube_tutorials': youtube_response.get('items', []),
        'google_books': google_books_response.get('items', []),
    }

    return JsonResponse(result)
```

将这些 API 集成在一起，通过`integrated_search`接口开放给前端。这样前端调用一个接口，即可获得 5 个 API 的结果。

### 3.2 词云模块

#### 3.2.1 模块简述

词云模块需要先调用 API，获得热词，然后返回给前端。前端调用`WordCloud`库，生成词云图。通过这样的方式，词云图里的每个热词都可以点击跳转到对应的来源。

#### 3.2.2 设计与实现

##### 3.2.2.1 前端

前端在页面加载时，通过接口获得后端提供的热词名称和链接，代码如下：

```typescript
const response = await axios.get(`${apiUrl}/wordcloud_generator/generate/`, {
  params: {
    width: 800,
    height: 600,
  },
});
```

然后创建一个`canvas`，调用`WordCloud`库，生成对应的词云图。这里的词云图通过参数设置，将形状展示为`心形`。此外，词云图点击链接可跳转。代码如下：

```typescript
const canvas = document.getElementById("wordcloud-canvas") as HTMLCanvasElement;
if (canvas) {
  const options = tags.value.map((tag) => [tag, Math.random() * 20]);
  canvas.width = 800;
  canvas.height = 500;
  WordCloud(canvas, {
    list: options,
    gridSize: 0,
    weightFactor: 2,
    shape: "cardioid",
    backgroundColor: "#efc2dd",
    origin: [400, 100],
    color: (word: any, weight: any) => {
      const colors = ["#FF5733", "#FFB833", "#33FF57", "#33B5FF", "#8E33FF"];
      return colors[Math.floor(Math.random() * colors.length)];
    },
    click: (item: any[]) => {
      const tag = item[0];
      window.open(`https://stackoverflow.com/tags/${tag}`, "_blank");
    },
    hover: (item: any[], dimension: any) => {
      if (item) {
        canvas.style.cursor = "pointer";
      } else {
        canvas.style.cursor = "default";
      }
    },
  });
} else {
  console.error("Canvas element not found");
}
```

##### 3.2.2.2 后端

后端调用`stackoverflow`的 API，获得热门`Tag`，返回给前端，代码如下：

```python
@api_view(['GET'])
def generate(request):
    if request.method == 'GET':
        response = requests.get('https://api.stackexchange.com/2.3/tags?site=stackoverflow&pagesize=100')

        width = int(request.GET.get('width', 800))
        height = int(request.GET.get('height', 800))  # 增加高度
        print("width=", width)
        print("height=", height)

        tags_data = response.json()
        tags = [tag['name'] for tag in tags_data['items']]

        text = ' '.join(tags)

        # mask = heart_shape_mask(width, height)
        mask = np.array(Image.open('img.png'))
        # Generate a word cloud in shape of LOVE
        wordcloud = WordCloud(
            width=width,
            height=height,
            background_color='red',
            max_font_size=10,
            mask=mask,
            contour_color='red',
            contour_width=5,
            repeat=True,
        ).generate(text)

        image = io.BytesIO()
        wordcloud.to_image().save(image, format='PNG')
        image.seek(0)
        encoded_image = base64.b64encode(image.getvalue()).decode('utf-8')

        return JsonResponse({'image': f'data:image/png;base64,{encoded_image}', 'tags': tags})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
```

### 3.3 热门代码模块

#### 3.3.1 模块简述

热门代码模块展示来自 3 个 API 的代码，同样在后端使用了集成 API，并通过 1 个接口供前端调用。
3 个 API 分别是`GitHub`, `StackOverflow`, `Dev.to`，以链接的形式展现，用户可以点击链接跳转到对应页面。

#### 3.3.2 设计与实现

##### 3.3.2.1 前端

前端调用接口，获得数据，展示在前端页面上。代码如下：

```typescript
const examplesResponse = await axios.get(`${apiUrl}/popular_code/get_popular/`)
    const examples = examplesResponse.data.results || []

    stackOverflowExamples.value = examples.filter(
      (example: { source: string }) => example.source === 'Stack Overflow'
    )
    gitHubExamples.value = examples.filter(
      (example: { source: string }) => example.source === 'GitHub'
    )
    devToExamples.value = examples.filter(
      (example: { source: string }) => example.source === 'Dev.to'
    )
  } catch (error) {
    console.error('Error generating word cloud or fetching examples:', error)
  } finally {
    loading.value = false // Stop loading
  }
```

##### 3.3.2.2 后端

后端集成 3 个 API，使用与 3.1.2.2 相同的技术，最后通过 1 个接口，供前端调用。代码如下：

```python
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
```

## 4. 项目截图

### 4.1 搜索模块

![alt text](images/image.png)
![alt text](images/image1.png)

### 4.2 词云模块

![alt text](images/image2.png)

### 4.3 热门代码模块

![alt text](images/image3.png)

### 4.4 登录

![alt text](images/image4.png)

### 4.5 注册

![alt text](images/image5.png)

## 5. Web API 使用说明

### 5.1 GitHub Code API

#### 说明

用于搜索代码示例。通过查询关键词和编程语言过滤，返回在 GitHub 上最受欢迎的代码片段。

#### 请求 URL

```
GET https://api.github.com/search/code?q={query}&sort=stars&order=desc
```

#### 参数

- `query`: 包含关键词和语言过滤器的搜索字符串。

#### 返回格式

- JSON 对象，包含搜索到的代码信息列表。

#### 示例

```json
{
  "total_count": 100,
  "items": [
    {
      "name": "example.py",
      "path": "repo/example.py",
      "url": "https://github.com/repo/example.py"
    }
  ]
}
```

### 5.2 GitHub Repositories API

#### 说明

用于搜索 GitHub 上的代码仓库，返回与关键词匹配的热门仓库。

#### 请求 URL

```
GET https://api.github.com/search/repositories?q={query}&sort=stars&order=desc
```

#### 参数

- `query`: 包含关键词和语言过滤器的搜索字符串。

#### 返回格式

- JSON 对象，包含搜索到的仓库信息列表。

#### 示例

```json
{
  "total_count": 50,
  "items": [
    {
      "name": "example-repo",
      "full_name": "user/example-repo",
      "html_url": "https://github.com/user/example-repo"
    }
  ]
}
```

### 5.3 StackOverflow API

#### 说明

用于从 StackOverflow 搜索相关问题。返回与用户查询匹配的问题列表。

#### 请求 URL

```
GET https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q={keywords}&tagged={languages}&site=stackoverflow
```

#### 参数

- `keywords`: 用户输入的关键词。
- `tagged`: 语言标签的列表，以`|`分隔。

#### 返回格式

- JSON 对象，包含匹配问题的列表。

#### 示例

```json
{
  "items": [
    {
      "title": "How to use Python for data analysis?",
      "link": "https://stackoverflow.com/questions/123456"
    }
  ]
}
```

### 5.4 Google Books API

#### 说明

用于搜索与关键词相关的书籍信息，帮助用户获取学习资源。

#### 请求 URL

```
GET https://www.googleapis.com/books/v1/volumes?q={keywords}
```

#### 参数

- `keywords`: 用户输入的关键词。

#### 返回格式

- JSON 对象，包含相关书籍的信息列表。

#### 示例

```json
{
  "items": [
    {
      "volumeInfo": {
        "title": "Learn Python the Hard Way",
        "infoLink": "https://books.google.com/books?id=12345"
      }
    }
  ]
}
```

### 5.5 YouTube API

#### 说明

用于搜索与用户查询匹配的 YouTube 视频，以提供视频教程。

#### 请求 URL

```
GET https://www.googleapis.com/youtube/v3/search?part=snippet&q={keywords}&key={api_key}
```

#### 参数

- `keywords`: 用户输入的关键词。
- `api_key`: YouTube API 密钥。

#### 返回格式

- JSON 对象，包含视频信息的列表。

#### 示例

```json
{
  "items": [
    {
      "id": {
        "videoId": "abcdefg"
      },
      "snippet": {
        "title": "Python Tutorial",
        "thumbnails": {
          "default": {
            "url": "https://img.youtube.com/vi/abcdefg/default.jpg"
          }
        }
      }
    }
  ]
}
```

### 5.6 Stack Overflow API

#### 说明

获取最新的热门问题。返回 Stack Overflow 上最活跃的问答列表。

#### 请求 URL

```
GET https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow&pagesize=5
```

#### 参数

- `order`: 排序方式（如`desc`）。
- `sort`: 根据活动排序。
- `site`: 指定为`stackoverflow`。
- `pagesize`: 每页返回的项目数量。

#### 返回格式

- JSON 对象，包含热门问题的信息列表。

#### 示例

```json
{
  "items": [
    {
      "title": "How to use async/await in JavaScript?",
      "link": "https://stackoverflow.com/questions/123456",
      "source": "Stack Overflow"
    }
  ]
}
```

### 5.7 GitHub API

#### 说明

获取在 GitHub 上最受欢迎的代码仓库。返回具有至少一个星标的仓库列表。

#### 请求 URL

```
GET https://api.github.com/search/repositories?q=stars:>1&sort=stars&order=desc&per_page=5
```

#### 参数

- `q`: 查询条件（如`stars:>1`）。
- `sort`: 排序方式（如`stars`）。
- `order`: 排序顺序（如`desc`）。
- `per_page`: 每页返回的仓库数量。

#### 返回格式

- JSON 对象，包含热门仓库的信息列表。

#### 示例

```json
{
  "items": [
    {
      "title": "example-repo",
      "link": "https://github.com/user/example-repo",
      "source": "GitHub"
    }
  ]
}
```

### 5.8 Dev.to API

#### 说明

获取流行的开发者文章。返回 Dev.to 平台上的热门文章列表。

#### 请求 URL

```
GET https://dev.to/api/articles?per_page=5
```

#### 参数

- `per_page`: 每页返回的文章数量。

#### 返回格式

- JSON 对象，包含热门文章的信息列表。

#### 示例

```json
{
  "items": [
    {
      "title": "Understanding Promises in JavaScript",
      "link": "https://dev.to/user/article-12345",
      "source": "Dev.to"
    }
  ]
}
```
