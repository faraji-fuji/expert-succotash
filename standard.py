import feedparser


class Standard:
    def __init__(self):
        pass

    def fetch_content(self, url):
        '''
        Get content from standard rss feed. Modify each post by adding a
        posted attribute.
        :param url: The URL to the RSS feed.
        Returns: a list of posts
        '''
        d = feedparser.parse(url)
        items = d.entries
        for item in items:
            item['is_posted'] = 'false'
        return items
