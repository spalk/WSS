class Page:
    """Page class description"""

    def __init__(self, url):
        self.url = url

    def get(self):
        return 'Page content from', self.url
