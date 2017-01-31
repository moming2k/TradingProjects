#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: start_virtual_desktop
# @Date: 2017-01-31
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


from xvfbwrapper import Xvfb

vdisplay = Xvfb(width=1366, height=768)
vdisplay.start()

vdisplay.stop()
