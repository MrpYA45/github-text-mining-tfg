#!/usr/bin/env python3

from setuptools import setup

from gtmprocessing.data.modeldownloader import ModelDownloader

setup()
ModelDownloader.get_zsc()
ModelDownloader.get_sa()
ModelDownloader.get_summ()
