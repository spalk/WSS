import urllib.request

import logging
logger = logging.getLogger('root')


class Page:
    """Page class description"""

    def __init__(self, url):
        self.url = url

    def get(self):
        logger.debug('Getting page source from: ' + self.url)
        page = urllib.request.urlopen(self.url)
        return page.read()
