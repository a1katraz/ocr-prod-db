#!/usr/bin/python
# -*- coding: utf-8 -*-
import io
import os
from google.cloud import storage
from googletrans import Translator

translator = Translator()
translations = translator.translate(['जय', 'श्री', 'सीता  राम'], src='hi', dest='en')
for translation in translations:
    print(translation.origin, ' -> ', translation.text)