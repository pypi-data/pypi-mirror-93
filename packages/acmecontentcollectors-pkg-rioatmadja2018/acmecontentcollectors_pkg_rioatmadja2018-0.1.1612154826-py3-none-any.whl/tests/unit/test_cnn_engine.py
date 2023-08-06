#!/usr/bin/env python
from unittest import TestCase
import pytest
import os
from acme_collectors.engines.cnn_engine import CNNENGINE
from typing import List

class TestCNNEngine(TestCase):

    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master', reason='Local Test' )
    def test_cnn_links(self):
        cnn_engine = CNNENGINE(topic='Islamic State')
        links, pages = cnn_engine.get_cnn_links()

        return self.assertListEqual([len(links), len(pages)], [21, 5])


    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master', reason='Local Test')
    def test_cnn_traverse_page(self):
        cnn_engine = CNNENGINE(topic='Islamic State')
        cnn_articles: List[str] = cnn_engine.traverse_page(depth=20)

        return self.assertEqual(len(cnn_articles), 42)
