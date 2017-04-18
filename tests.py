# -*- coding: UTF-8 -*-

# See file COPYING distributed with unf for copyright and license.

import unittest
import unf

# test source is 
# https://raw.githubusercontent.com/IQSS/UNF/master/doc/unf_examples.txt
# with help from the UNF R package (version 2.0.5)

class TestUNFs(unittest.TestCase):

    def test_missing(self):
        u = unf.UNF(None)
        self.assertEqual(u.unf, 'cJ6AyISHokEeHuTfufIqhg==')
        return

    def test_string(self):
        u = unf.UNF('A character String')
        self.assertEqual(u.unf, 'FYqU7uBl885eHMbpco1ooA==')
        return

    def test_long_string(self):
        u = unf.UNF('A quite long character string, so long that the ' + \
                    'number of characters in it happens to be more ' + \
                    'than the default cutoff limit of 128.')
        self.assertEqual(u.unf, '/BoSlfcIlsmQ+GHu5gxwEw==')
        return

    def test_unicode(self):
        u = unf.UNF(u'på Færøerne')
        self.assertEqual(u.unf, 'KHM6bKVaVaxWDDsmyerfDA==')
        return

    def test_empty_string(self):
        u = unf.UNF('')
        self.assertEqual(u.unf, 'ECtRuXZaVqPomffPDuOOUg==')
        return

# eof
