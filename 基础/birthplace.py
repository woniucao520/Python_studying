# -*- coding: utf-8 -*-
import csv

import re
from lxml import etree
import os
import zipfile

startdir = "E:\\task\\"

z = zipfile.ZipFile('myresult.zip','w',zipfile.ZIP_DEFLATED)
for dirpath, dirnames, filenames in os.walk(startdir):
    # fpath = dirpath.replace(startdir,'')
    # fpath = fpath and fpath + os.sep or ''
    for filename in filenames:
        z.write(os.path.join(dirpath, filename))
        print ('压缩成功')
z.close()

