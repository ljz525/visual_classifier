from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import glob

class VCapp:

    def __init__(self):
        self.root = Tk()
        self.root.title('Visual Classifier')

        # select the image path
        self.path = StringVar()
        self.path.set(os.path.abspath('.'))

        self.frame1_open_folder = Frame(self.root)
        self.frame1_open_folder.pack()
        b1 = Button(self.frame1_open_folder,text='Select directory',command=self.selectPath).pack(side='left')
        self.text_folder = Entry(self.frame1_open_folder,textvariable=self.path,state='readonly').pack(side='left')

        # read all the images in the folder
        b2 = Button(self.frame1_open_folder,text='Open',command=self.openPath).pack(side='left')

        # # path of the results  # not finished yet
        # self.results_path = StringVar()
        # self.results_path.set(os.path.abspath('.'))
        # self.frame3_results_path = Frame(self.root)
        # self.frame3_results_path.pack()
        # b3 = Button(self.frame3_results_path,text='Results path',command=self.selectPathResults).pack(side='left')
        # self.text_path_results = Entry(self.frame3_results_path,textvariable=self.results_path,state='readonly').pack(side='left')
        # b4 = Button(self.frame3_results_path,text='Open',command=self.readResults).pack(side='left')
        
        # buttons
        self.frame2_classification = Frame(self.root)
        self.frame2_classification.pack()

        self.ii = 0
        b_true = Button(self.frame2_classification,text='True',command=self.clickTrue).pack(side='left')
        b_false = Button(self.frame2_classification,text='False',command=self.clickFalse).pack(side='left')
        b_other = Button(self.frame2_classification,text='Other',command=self.clickOther).pack(side='left')

        # 上一张
        back = Button(self.root,text='back←',command=self.back).pack()

        # quit Button
        b_quit = Button(self.root,text='Quit',command=self.saveAndQuit)
        b_quit.pack()

        self.root.mainloop()
        self.file.close()
        self.root.destroy()


    def selectPath(self):
        path_ = filedialog.askdirectory()
        if path_ == '':
            self.path.get()
        else:
            path_ = path_.replace('/','\\')
            self.path.set(path_)

    def createResultsFile(self):  # run in openPath
        # first create the results.txt if there isn't one
        if os.path.exists(self.dir+'\\'+'results.txt')==False:
            self.file = open(self.dir+'\\'+'results.txt','w')
            self.ok_list = []
        else:
            # read the file names which was already classified
            file = open(self.dir+'\\'+'results.txt','r')
            lines = file.readlines()
            file.close()
            self.ok_list = []
            for line in lines:
                self.ok_list.append(line.split()[0])
            # then open the file as 'a' mode
            self.file = open(self.dir+'\\'+'results.txt','a')

    def openPath(self):
        self.dir = os.path.dirname(self.path.get()+'\\')
        self.createResultsFile()
        # read jpg and png files
        self.imglist = glob.glob(self.path.get()+'\*.jpg')+glob.glob(self.path.get()+'\*.png')
        # delete the file names which was already classified
        # print(self.imglist)
        for jj in range(len(self.imglist)):
            if self.imglist[jj] in self.ok_list:
                self.imglist[jj] = ''
        self.imglist = list(filter(None, self.imglist))
        self.img_num = len(self.imglist)
        # print(self.img_num)
        if self.img_num == 0:
            self.file.close()
            self.root.quit()
        else:
            self.openfile()
        
    def openfile(self):
        # filepath = filedialog.askopenfilename(filetypes=[(('JPG','*.jpg')),(('PNG','*,png'))])
        filepath = self.imglist[self.ii]
        img_open = Image.open(filepath)
        self.show_name = Label(self.root,text='%s'%filepath)
        self.show_name.pack()
        self.image = ImageTk.PhotoImage(img_open)
        self.label_img = Label(self.root,image=self.image)
        self.label_img.pack()

    def clickTrue(self):
        self.file.write(self.imglist[self.ii]+'    '+'True'+'\n')
        self.label_img.destroy()
        self.show_name.destroy()
        self.ii += 1
        if self.ii < self.img_num:
            self.openfile()
        else:
            self.saveAndQuit()

    def clickFalse(self):
        self.file.write(self.imglist[self.ii]+'    '+'False'+'\n')
        self.label_img.destroy()
        self.show_name.destroy()
        self.ii += 1
        if self.ii < self.img_num:
            self.openfile()
        else:
            self.saveAndQuit()

    def clickOther(self):
        self.file.write(self.imglist[self.ii]+'    '+'Other'+'\n')
        self.label_img.destroy()
        self.show_name.destroy()
        self.ii += 1
        if self.ii < self.img_num:
            self.openfile()
        else:
            self.saveAndQuit()

    def back(self):
        self.ii -= 1
        # close the file, read it, delete the last line, then write back
        self.file.close()
        file = open(self.dir+'\\'+'results.txt','r')
        lines = file.readlines()
        file.close()
        self.file = open(self.dir+'\\'+'results.txt','w')
        self.file.writelines(lines[:-1])
        # back to last image
        self.label_img.destroy()
        self.show_name.destroy()
        self.openfile()

    def saveAndQuit(self):
        self.file.close()
        self.root.quit()


app = VCapp()