# -*- coding: utf-8 -*-

import subprocess
import requests


def get_newest():
    try:
        data = requests.get('https://raw.githubusercontent.com/Emberium/SphereLogger/master/version.txt')
        return data.text.replace('\n', '')

    except requests.exceptions.ConnectionError:
        return False


def get_current():
    with open('version.txt') as version_file:
        return version_file.read().replace('\n', '')


def update():
    subprocess.call(["git", "pull", "origin", "master"])
    return get_newest()

if __name__ == '__main__':
    print('[-*- Checking version information... -*-]')

    newest = get_newest()
    current = get_current()

    if newest != current:
        print('[-*- Updating from %s to %s... -*-]' % (current, newest))
        update()

        print('[-*- Successful updated to %s -*-]' % newest)

    else:
        print("[-*- You are already updated to newest version. -*-]")
