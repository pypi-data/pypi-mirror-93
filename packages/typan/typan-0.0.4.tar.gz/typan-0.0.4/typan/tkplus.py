import tkinter

class FlatButton(tkinter.Button):
    def __init__(self,master,*args,**kwargs):
        super().__init__(master,bd=0,borderwidth=0,*args,**kwargs)

def center_tk_window(self,w=500,h=500):
    ws = self.winfo_screenwidth()
    hs = self.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    self.geometry("%dx%d+%d+%d" % (w,h,x,y))

setattr(tkinter.Tk,"set_size",center_tk_window)