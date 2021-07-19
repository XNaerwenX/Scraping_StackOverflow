import requests
from bs4 import BeautifulSoup
import pprint

res = requests.get('https://stackoverflow.com/questions')
soup = BeautifulSoup(res.text, 'html.parser')

questions = soup.select('.summary')
views = soup.select('.views')


def sort_qs_by_views(question_list):
    return sorted(question_list, key=lambda k: k['views'], reverse=True)


def create_custom_question_list(questions, views):
    st_ov = []
    for idx, item in enumerate(questions):
        # getting rid of extra info in '.summary' that we don't need by selecting
        # the ".question-hyperlink" (sub)class inside '.summary'
        title = item.select_one(".question-hyperlink").getText()
        # grabbing the links (which all start with: <a href="/questions/11227809/why-blah-blah?,
        # so I added 'https://stackoverflow.com' for them to be interactive)
        href = 'https://stackoverflow.com' + \
            item.select_one(".question-hyperlink").get('href', None)
        # '.views' looks like this (<div class="views" title="8 views">8 views</div>), so
        # to strip it of everything but "X view(s)" we grab
        # only the ['title'] attribute
        view = views[idx].attrs['title']
        if len(view):
            # getting rid of the word "view(s)" so that only a number remains
            points = view.replace("s", '').replace(" view", '')
            if int(points) > 10:
                st_ov.append(
                    {'title': title, 'link': href, 'views': int(points)})
    return sort_qs_by_views(st_ov)


pprint.pprint(create_custom_question_list(questions, views))
