#  /user1/ptbc/di2443ou/bin/python3
# 27-04-2022
# DO
'''
This script generate a pdf file of original and corresponding annotated slides
INPUT = /work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/Results/SCNN/QPdata_withduodenum/
    - whitch each folder in the input should contain :
        * QPdata file
        * orginal slide (in format of tiff)
        * annotated slide (in format of tiff)

INTERMEDIATE FOLDER : /work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/Results/SCNN/img_jpg/
    - can be deleted at the last

OUTPUT : /work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/Results/SCNN/comb_modelv3.pdf
'''





from fpdf import FPDF
import os, sys
from PIL import Image
import pandas as pd
import os
import glob
import getpass

SNN = '/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/Results/SCNN/'
#QPdata_withduodenum = '/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/Results/SCNN/QPdata_withduodenum/'
input='/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/lame francois/grad_cam_whole_wsi/images/'

#title = 'Prediction Besançon slides '
title = 'grad cam whole wsi Besancon'

class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Calculate width of title and position
        w = self.get_string_width(title) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(119,136,153)
        self.set_fill_color(211,211,211)
        self.set_text_color(0,0,0)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w, 9, title, 1, 1, 'C', 1)
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self,name, ln):
        # Arial 12
        self.set_font('Arial', '', 12)
        # Background color
        self.set_fill_color(112, 128, 144)
        # Line break
        self.ln(ln)
        # Title
        self.cell(0, 6, f'Slide {name}', 0, 1, 'L', 1)



    def chapter_body(self, img_path,x, y):
        # Read text file
        sizew=150
        sizeh = 100
        pdf.image(img_path, x, y, w=sizew, h=sizeh)
        # Times 12
        self.set_font('Times', '', 12)

        # Line break
        self.ln()
        # Mention in italics
        self.set_font('', 'I')
        self.cell(0, 5, 'N {Green} S {Blue} T {Red} D {Yellow}')

    def print_chapter(self, name, ln, img_path, x, y):
        self.chapter_title(name, ln)
        self.chapter_body(img_path,x, y)



if __name__ == '__main__':
    '''try:
        os.mkdir(f'{SNN}/img_jpg')
    except:
        pass

    # import my images
    slides = os.listdir(QPdata_withduodenum)
    my_list = []
    for slide in slides:
        my_list.extend(os.listdir(f'{QPdata_withduodenum}{slide}'))


    qpdata, tif, org = [], [], []'''
    grad, org = [], []
    my_list = os.listdir(input)
    for item in my_list:
        if item.endswith('_2.jpg'):
            grad.append(item)
        else:
            org.append(item)
    temp1, temp2 = [], []

    '''if len(org) != len(slides):
        print('origin images does not equal to annotate images ! ')
        sys.exit()'''

    for i in range(len(grad)):
        temp1.append(os.path.join(f'{input}', grad[i]))
        temp2.append(os.path.join(f'{input}', org[i]))

    df = pd.DataFrame(columns=['tifs_org', 'tifs'])
    df['tifs_org'] = temp2
    df['tifs'] = temp1

    df.to_csv('testetst.csv')

    ######## define method to convert imgs into jpeg
    def tiff_jpeg(img, outpath, name):
        if img[-3:] == "tif" or img[-3:] == "bmp" :
               im = Image.open(img)
               out = im.convert("RGB")
               out.save(f'{outpath}/{name}.jpg', "JPEG", quality=90)

    ###### define pdf object
    pdf = PDF()
    pdf.set_title(title)
    pdf.set_author(getpass.getuser())

    for org, annot in zip(df['tifs_org'], df['tifs']):
        org_name = org.split('/')[-1].split('.')[0]
        annot_name = annot.split('/')[-1].split('.')[0]
        print(org_name)
        print(annot_name)
        #tiff_jpeg(org, f'{SNN}/img_jpg', org_name)
        #tiff_jpeg(annot, f'{SNN}/img_jpg', annot_name)
        pdf.add_page()
        pdf.print_chapter(f'{org_name}', 4, f'{input}{org_name}.jpg', x=25, y=45)
        pdf.print_chapter(f'{annot_name}',110, f'{input}{annot_name}.jpg', x=25, y=170)
        #pdf.print_chapter(2, 'THE PROS AND CONS', '20k_c2.txt')
    pdf.output(f'/work/shared/ptbc/CNN_Pancreas_V2/Donnees/project_kernel03_scan21000500/lame francois/grad_cam_whole_wsi/{title}.pdf', 'F')
