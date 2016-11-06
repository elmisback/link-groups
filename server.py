from bottle import run, static_file, request, get
from lxml import html
import requests

def _get_title(url):
    try:
        page = requests.get(url, timeout=2)
    except requests.exceptions.MissingSchema as err:
        print err
        return None
    except requests.exceptions.Timeout as err:
        print err
        return None
    except requests.exceptions.RequestException as err:
        raise err
    results = html.fromstring(page.content).xpath('//head/title')
    title = results[0].text if results else None
    print title
    return title

@get('/get/page-title')
def page_title():
    return {'title': _get_title(request.params.url)}

#@route('/post/is-valid-url', method='POST')
#def is_valid_url():
#    """HACK: We'll call it valid if we can get a title."""
#    return (_get_title(request.forms.url) is not None)

@get('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

run(host='localhost', port=8080, debug=True)
