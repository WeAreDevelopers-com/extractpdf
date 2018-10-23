# -*- coding: utf-8 -*-
import unittest
import os
import os.path

from extractpdf.downloader import Downloader

class DownloaderTest(unittest.TestCase):
    def test_parse_filename(self):
        filename = Downloader.parse_filename("https://arxiv.org/pdf/1708.03615.pdf")
        self.assertEqual(filename, '1708.03615.pdf')

    def test_downloader_can_download_empty_params(self):
        self.assertRaises(TypeError, Downloader)
 
    def test_downloader_can_download_file(self):
        dl = Downloader("https://arxiv.org/pdf/1708.03615.pdf")
        self.assertEqual(dl.filename, "1708.03615.pdf")
        self.assertTrue(os.path.isfile(dl.full_path))

    def test_downloader_handles_invalid_urls(self):
        self.assertRaises(RuntimeError, Downloader, "https://arxiv.org/pdf/")
