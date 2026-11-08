import json
import os

import requests

ALLOWED_ORIGIN = 'https://ninamarie-nd.github.io'
VISION_URL = 'https://vision.googleapis.com/v1/images:annotate'
MAX_IMAGE_CHARS = 6000000  # about 4.5 MB of base64 image data


def _headers(origin):
    return {
        'Access-Control-Allow-Origin': origin if origin == ALLOWED_ORIGIN else 'null',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Vary': 'Origin',
        'Content-Type': 'application/json',
    }


def read_label(request):
    origin = request.headers.get('Origin', '')
    if request.method == 'OPTIONS':
        return ('', 204, _headers(origin))
    if origin != ALLOWED_ORIGIN:
        return (json.dumps({'error': 'origin not allowed'}), 403, _headers(origin))

    body = request.get_json(silent=True) or {}
    image = body.get('image', '')
    if ',' in image:
        image = image.split(',', 1)[1]
    if not image:
        return (json.dumps({'error': 'no image'}), 400, _headers(origin))
    if len(image) > MAX_IMAGE_CHARS:
        return (json.dumps({'error': 'image too large'}), 413, _headers(origin))

    payload = {
        'requests': [{
            'image': {'content': image},
            'features': [{'type': 'DOCUMENT_TEXT_DETECTION'}],
        }]
    }
    resp = requests.post(
        VISION_URL,
        headers={'x-goog-api-key': os.environ['VISION_API_KEY']},
        json=payload,
        timeout=25,
    )
    result = resp.json().get('responses', [{}])[0]
    if resp.status_code != 200 or 'error' in result:
        return (json.dumps({'error': 'vision request failed'}), 502, _headers(origin))
    text = (result.get('fullTextAnnotation') or {}).get('text', '')
    return (json.dumps({'text': text}), 200, _headers(origin))
