#!/usr/bin/env python

from nltk import *
import xml.etree.ElementTree as ET

root = ET.parse('sms_corpus.xml').getroot()

messages = [m.find('text') for m in root]