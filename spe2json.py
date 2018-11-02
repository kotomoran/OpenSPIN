from docx import Document
from docx.shared import Inches
from PIL import Image, ImageDraw, ImageFont
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

import SPINLib
import xlrd
import os
import io

spenames=[]

# Указываем папку в которой производить поиск
#path='D:/MailCloud/Python/core_pic/'
path = os.path.abspath(os.curdir) #текущая папка

# собирается список всех spe в папке path
for rootdir, dirs, files in os.walk(path):
    for file in files:
        if((file.split('.')[-1]) in ['spe']):
            #print (os.path.join(rootdir, file))
            spenames.append(os.path.join(rootdir, file))
            sp=SPINLib.spectr()
            sp.open_spe(os.path.join(rootdir, file))
            sp.save()
