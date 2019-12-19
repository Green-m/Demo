#!/bin/sh

find /usr/share/doc/python3-impacket/examples/*.py |xargs -I _ basename _ .py|xargs -I {} ln -s /usr/share/impacket/script /usr/bin/impacket-{}
