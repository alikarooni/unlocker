#!/usr/bin/env python
"""
The MIT License (MIT)

Copyright (c) 2015-2017 Dave Parsons

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from __future__ import print_function
import os
import sys
import shutil
import tarfile
import zipfile
import time
import urllib
import requests

try:
    # For Python 3.0 and later
    # noinspection PyCompatibility
    from urllib.request import urlopen
    # noinspection PyCompatibility
    from html.parser import HTMLParser
    # noinspection PyCompatibility
    from urllib.request import urlretrieve
    # noinspection PyCompatibility
    from urllib.request import install_opener
except ImportError:
    # Fall back to Python 2
    # noinspection PyCompatibility
    from urllib2 import urlopen
    # noinspection PyCompatibility
    from HTMLParser import HTMLParser


# Parse the Fusion directory page
class CDSParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.reset()
        self.HTMLDATA = []

    def handle_data(self, data):
        # Build a list of numeric data from any element
        if data.find("\n") == -1:
            if data[0].isdigit():
                self.HTMLDATA.append(data)
                self.HTMLDATA.sort(key=lambda s: [int(u) for u in s.split('.')])

    def clean(self):
        self.HTMLDATA = []

if sys.version_info > (3, 0):
# Python 3 code in this block
    pass
else:
    # Python 2 code in this block
    class MyURLopener(urllib.FancyURLopener):
        http_error_default = urllib.URLopener.http_error_default

def convertpath(path):
    # OS path separator replacement function
    return path.replace(os.path.sep, '/')

def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration)) if duration>0 else 0
    percent = min(int(count*block_size*100/total_size),100)
    time_remaining = ((total_size - progress_size)/1024) / speed if speed > 0 else 0
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds remaining   " %
                    (percent, progress_size / (1024 * 1024), speed, time_remaining))
    sys.stdout.flush()

def CheckToolsFilesExists(dest):
    filesFound = os.path.exists(convertpath(dest + '/tools/darwin.iso')) & os.path.exists(convertpath(dest + '/tools/darwinPre15.iso'))
    askMsg = 'You already have downloaded the tools. Download again?[y/n]'

    if filesFound:
        while True:
            # Ask if the user want to download again
            if sys.version_info > (3, 0):
            # Python 3 code in this block
                userResponse = input(askMsg)
            else:
                # Python 2 code in this block
                userResponse = raw_input(askMsg)
            
            if str(userResponse).upper() == 'Y':
                return False
            elif str(userResponse).upper() == 'N':
                return True
            else:
                print('Must enter y or n. You pressed: ' + str(userResponse).upper())
    else:
        return False

def GetResponseFromUrl(url):
    try:
        # Try to read page
        if sys.version_info > (3, 0):
            # Python 3 code in this block
            req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
            response = urllib.request.urlopen( req )
            return response
        else:
            # Python 2 code in this block
            req = urllib.Request(url, headers={'User-Agent' : "Magic Browser"}) 
            response = urllib.urlopen( req )
            return response
    except:
        print('Couldn\'t read page')
        return False

# Function to download a file
def DownloadFile(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download {filename}, status code: {response.status_code}")

def main():
    # Check minimal Python version is 2.7
    if sys.version_info < (2, 7):
        sys.stderr.write('You need Python 2.7 or later\n')
        sys.exit(1)

    dest = os.getcwd()

    # Try local file check
    if(CheckToolsFilesExists(dest)):
        # User as already download the tools and chosen not doing again
        return

    # Re-create the tools folder
    shutil.rmtree(dest + '/tools', True)
    try:
        os.mkdir(dest + '/tools')
    except :
        pass

    base_url = "https://packages-prod.broadcom.com/tools/frozen/darwin/"
    iso_files = ["darwin.iso", "darwinPre15.iso"]

    # Download the darwin.iso and darwinPre15.iso files
    for iso in iso_files:
        file_url = base_url + iso
        DownloadFile(file_url, iso)

    # Move the ISO files to the tools folder
    shutil.move(convertpath(dest + '/' + iso_files[0]), convertpath(dest + '/tools/' + iso_files[0]))
    shutil.move(convertpath(dest + '/' + iso_files[1]), convertpath(dest + '/tools/' + iso_files[1]))
    print('Move the ISO files to the tools folder')

    print()

    print('Tools from frozen retrieved successfully')
    return

if __name__ == '__main__':
    main()
