#!/usr/bin/env python
from acme_collectors.utils.constants import HEADERS
import re
from phantomjs import Phantom
from typing import Dict, List
from bs4 import BeautifulSoup

class CNNENGINE(object):
    """
    DESCRIPTION
    -----------
    Helper class to parse the contents from the CNN class

    PARAMETERS
    ----------
    :topic: given a non-empty and valid topic
    :size: an optional parameters with a default search size of 10

    EXAMPLE
    -------
    >>>
    >>>
    """
    def __init__(self, topic: str, size: int = 10):
        if not topic:
            raise AttributeError("Please provide a valid url.")

        self.encoded_puncts: Dict = {char: hex(ord(char)).replace('0x', '%') for char in re.findall(r'\W', topic)}
        self.topic: str = ''.join([self.encoded_puncts.get(char, char) for char in topic])

        self.query: str = f"https://www.cnn.com/search?size={size}&q={self.topic.lower()}"
        self.config: Dict = {'headers': HEADERS,
                             'url': self.query
                             }

        self.response: str = ""

    def cnn_browser(self, config: Dict = {}) -> str:
        """
        Description
        -----------
        Helper method to make query to the CNN Website

        Parameters
        ----------
        :config: an optional dictionary parameter

        Returns
        -------
        :return: a string of response
        """
        try:

            phantom_browser = Phantom()
            response: str = phantom_browser.download_page(conf=self.config if not config else config)
            return response

        except ConnectionError as e:
            raise ConnectionError(f"[ERROR] Unable to connect to the following url: {self.query}") from e

    def get_cnn_links(self, config: Dict = {}) -> tuple:
        """
        Description
        -----------
        Helper method to extract all the CNN's links

        Returns
        -------
        :return: a list of strings that contain CNN links
        """
        cnn_response: str = self.cnn_browser(config=config)
        soup = BeautifulSoup(cnn_response.encode('utf-8'))
        cnn_links: [str] = [a.get('href') for a in soup.find_all('a') if re.findall(r"www.cnn.com.*.html", a.get('href'))]
        next_page: List[str] = self.next_page(soup=soup)

        return (cnn_links, next_page)

    def parse_content(self, cnn_link: str) -> str:
        """
        Description
        -----------
        Helper method to parse the individual CNN page

        Parameters
        ----------
        :cnn_link: given a valid cnn link

        Returns
        -------
        :return: a string with the CNN contents
        """
        if not cnn_link:
            raise ValueError(f"Please provide the right CNN link {cnn_link}")

        cnn_response: str = self.cnn_browser()
        soup = BeautifulSoup(cnn_response.encode('utf-8'))

        return ' '.join([x.text for x in soup.find_all('div') if 'l-container' in x.get('class', '')])

    def traverse_page(self, depth: int = 30) -> List:
        """
        Description
        -----------
        Helper function to traverse the CNN links by the given depth

        Parameters
        ----------
        :depth: an optional depth parameter with default of 30

        Returns
        -------
        :return: a list of the CNN articles
        """

        cnn_articles: List = []
        for page in range(0, depth, 10):
            url: str = f"{self.query}&from={page}&page={round(page/10) + 1}"
            conf: Dict = {'url': url,
                          'headers': HEADERS
                          }

            cnn_links, next_page = self.get_cnn_links(config=conf)
            if not next_page:
                return cnn_articles

            for link in cnn_links:
                cnn_articles.append(self.parse_content(cnn_link=link))

        return cnn_articles

    def next_page(self, soup: BeautifulSoup) -> List:
        """
        Description
        -----------
        Helper method to index the next page

        Parameters
        ----------
        :soup: a beautiful soup object

        Returns
        -------
        :return: a list of string that contains the page numbers
        """
        if not isinstance(soup, BeautifulSoup):
            raise TypeError("Please provide a beautiful soup object.")

        return [x.text for x in soup.find_all('span') if 'SearchPageLink' in ' '.join(x.get('class', []))]

