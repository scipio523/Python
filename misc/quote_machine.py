import urllib
import re
from Tkinter import *

class Application(Frame):

	def __init__(self,master):
                """Initialize the Frame"""
                Frame.__init__(self,master)
		self.grid()
		self.create_widgets()

	def create_widgets(self):
                self.instruction=Label(self,text="Enter a ticker symbol: ")
                self.instruction.grid(row=0,column=0,columnspan=2,sticky=E)

                self.symbol=Entry(self,width=7)
                self.symbol.grid(row=0,column=2,sticky=E)

                self.button=Button(self,text="Submit",command=self.get_quote)
                self.button.grid(row=1,column=0,sticky=W)

                self.text=Text(self,width=20,height=3,wrap=WORD)
                self.text.grid(row=2,column=0,columnspan=3,sticky=E)

        def get_quote(self):
                symbol=self.symbol.get()
                url="http://www.google.com/finance?q="+str(symbol)
                htmlfile=urllib.urlopen(url)
                htmltext=htmlfile.read()
                regex='<span id="ref_[^.]*_l">(.+?)</span>'
                pattern=re.compile(regex)
                price=re.findall(pattern,htmltext)
                self.text.delete(0.0,END)
                self.text.insert(0.0,symbol.upper()+" Price: "+price[0])

root=Tk()
root.title("Quote Machine")
root.geometry("170x100")
app=Application(root)
root.mainloop()
                
