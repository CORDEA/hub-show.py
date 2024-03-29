#!/usr/bin/env python
# encoding:utf-8
#
# Copyright 2016 Yoshihiro Tanaka
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import requests
import time

from optparse import OptionParser

__version__ = "1.0.0"


def optSettings():
    usage = "hub-show :token :owner/:repo " \
            "[--base-url :url] [-m --mode :(pull|issue)] [--with-body]"

    version = __version__
    parser = OptionParser(usage=usage, version=version)

    parser.add_option(
        "--base-url",
        action="store",
        type="str",
        dest="base_url",
        default="https://api.github.com")

    parser.add_option(
        "--with-body", action="store_true", dest="body", default=False)

    parser.add_option(
        "-m",
        "--mode",
        action="store",
        type="str",
        dest="mode",
        default="pull")

    return parser.parse_args()


class BgColor:
    GRN = "\033[1;42m"
    RED = "\033[1;41m"
    END = "\033[1;m"


class FontColor:
    GRN = "\033[1;32m"
    END = "\033[1;m"


class HubShow:
    def __init__(self, options, args):

        token = args[0]
        repo = args[1]
        base_url = options.base_url

        self.with_body = options.body

        seg = "repos/"

        self.headers = {
            "Accept": "application/vnd.github.full+json",
            "Authorization": "token " + token
        }

        self.url = base_url + seg + repo

    def pull(self):
        r = requests.get(self.url + "/pulls", headers=self.headers)
        json = r.json()

        for j in json:
            assign = ""
            if "assignee" in j and j["assignee"]:
                assign = j["assignee"]["login"].encode('utf-8')
            url = j["url"]
            creator = ""
            if "user" in j:
                creator = j["user"]["login"].encode('utf-8')
            title = j["title"].encode('utf-8')
            body = j["body"].encode('utf-8')
            time.sleep(0.1)
            com = requests.get(j["comments_url"], headers=self.headers)
            time.sleep(0.1)
            rev = requests.get(j["review_comments_url"], headers=self.headers)

            print BgColor.GRN + "# " + title + BgColor.END
            print url
            print " created by " + FontColor.GRN + creator + FontColor.END
            if assign:
                print " assignee " + FontColor.GRN + assign + FontColor.END
            print " issue comments " + str(len(com.json()))
            print " review comments " + str(len(rev.json()))
            if self.with_body:
                for b in body.split("\n"):
                    print "\t" + b
            print

    def issue(self):
        r = requests.get(self.url + "/issues", headers=self.headers)
        json = r.json()

        for j in json:
            assign = ""
            if "assignee" in j and j["assignee"]:
                assign = j["assignee"]["login"].encode('utf-8')
            url = j["url"]
            creator = ""
            if "user" in j:
                creator = j["user"]["login"].encode('utf-8')
            title = j["title"].encode('utf-8')
            body = j["body"].encode('utf-8')
            comments = j["comments"]

            print BgColor.RED + "# " + title + BgColor.END
            print url
            print " created by " + FontColor.GRN + creator + FontColor.END
            if assign:
                print " assignee " + FontColor.GRN + assign + FontColor.END
            print " comments " + str(comments)
            if self.with_body:
                for b in body.split("\n"):
                    print "\t" + b
            print


if __name__ == '__main__':
    options, args = optSettings()
    pr = HubShow(options, args)
    if options.mode == "pull":
        pr.pull()
    elif options.mode == "issue":
        pr.issue()
