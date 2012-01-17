'''
Techniques for getting and modifying clipboard information through Tk.
'''
from Tkinter import Tk
cb=Tk()
orgString = cb.selection_get(selection = "CLIPBOARD")
print ""
print "ClipboardContents:  ", orgString
orgString = orgString.replace(",",";")
'''
orgList = list(orgString)
commaCount = orgString.count(",")
print "Number of Commas:  ",commaCount
if commaCount != 0:
    for x in range(0,commaCount):
        commaLoc = orgString.find(",")
        orgList[commaLoc] = ";"
        orgString = "".join(orgList)
orgString = "".join(orgList)
'''
print "New String:  ", orgString
cb.clipboard_clear
cb.clipboard_append(orgString)
print "Clipboard replaced!"
