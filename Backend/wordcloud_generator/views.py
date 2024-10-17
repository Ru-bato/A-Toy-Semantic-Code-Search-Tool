import base64
import io

import numpy as np
import requests
from PIL import Image
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from wordcloud import WordCloud


def index(request):
    return render(request, 'wordcloud_generator/index.html')


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


# Create a mask in shape of LOVE
def heart_shape_mask(width, height):
    import numpy as np

    x = np.linspace(-1.5, 1.5, width)
    y = np.linspace(-1.5, 1.5, height)
    X, Y = np.meshgrid(x, y)
    Z = (X ** 2 + (Y - np.sqrt(np.abs(X))) ** 2 - 1) ** 3 - X ** 2 * (Y - np.sqrt(np.abs(X))) ** 3

    heart_mask = (Z < 0).astype(np.uint8) * 255
    return heart_mask
