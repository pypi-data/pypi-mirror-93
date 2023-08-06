import tkinter as tk
import tkinter.filedialog as fd
import os
import uuid
import configparser
from CipherLib.encryption import *
from CipherLib.stegano import *
from CipherLib.audiostegano import *

class StegGui():
    def __init__(self):
        self.master = tk.Tk()
        self.master.resizable(False, False)
        self.master.title('C1ph3r T00lz')
        self.statuslabel = tk.StringVar()
        self.ofilelabel = tk.StringVar()
        width = 500
        height = 450
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width//2) - (width//2)
        y = (screen_height//2) - (height//2)
        self.master.geometry(f'{width}x{height}+{x}+{y}')
        tk.Label(self.master, text="Image/Audio File").grid(row=0)
        tk.Label(self.master, text="Data File").grid(row=1)
        tk.Label(self.master, text="Encryption Key").grid(row=2)
        tk.Label(self.master, text="Status").grid(row=3)
        tk.Label(self.master, text="Output File").grid(row=4)

        self.var1 = tk.IntVar(self.master)
        self.cb = tk.Checkbutton(self.master, text="View File", variable=self.var1, onvalue = 1, offvalue = 0, command = self._readfile)
        self.cb.grid(row=5, column = 0, sticky=tk.NW)
        self.cur_status = tk.Label(self.master, textvariable=self.statuslabel)
        self.cur_status.grid(row=3, column = 1, sticky=tk.W, columnspan = 3)
        self.ofilel = tk.Label(self.master, textvariable=self.ofilelabel)
        self.ofilel.grid(row=4, column = 1, sticky=tk.W, columnspan = 3)
        self.sbar = tk.Scrollbar(self.master)
        self.sbar.grid(row=5, column = 3, sticky = tk.W)
        self.mlist = tk.Listbox(self.master, yscrollcommand=self.sbar.set)
        self.mlist.grid(row = 5, column = 1, columnspa = 2, sticky = tk.W)
        self.sbar.config(command = self.mlist.yview)

        self.ifilepath = tk.Entry(self.master)
        self.filepath = tk.Entry(self.master)
        self.keyentry = tk.Entry(self.master, show = '*')

        self.ifilepath.grid(row=0, column=1, columnspan = 2, sticky = tk.W)
        self.filepath.grid(row=1, column=1, columnspan = 2, sticky = tk.W)
        self.keyentry.grid(row=2, column=1, columnspan = 2, sticky = tk.W)

        tk.Button(self.master, text = 'Browse', command = self.openembedfile).grid(row=0, column =3, sticky=tk.W)
        tk.Button(self.master, text = 'Browse', command = self.opendatafile).grid(row=1, column =3, sticky=tk.W)

        tk.Button(self.master, text='Encrypt', command=self._encryptfile).grid(row=10, column = 1, sticky=tk.W, pady = 4)
        tk.Button(self.master, text='Embed', command=self._embedfile).grid(row=11, column = 1, sticky=tk.W, pady = 4)
        tk.Button(self.master, text='Encrypt and Embed', command=self.enc_and_embed).grid(row=12, column = 1, sticky=tk.W, pady = 4)

        tk.Button(self.master, text='Decrypt', command=self._decryptfile).grid(row=10, column = 2, sticky=tk.W, pady = 4)
        tk.Button(self.master, text='Extract', command=self._extractfile).grid(row=11, column = 2, sticky=tk.W, pady = 4)
        tk.Button(self.master, text='Extract and Decrypt', command=self.extract_and_decrypt).grid(row=12, column=2, sticky=tk.W, pady=4)
        tk.Button(self.master, text='Quit', command=self.master.quit).grid(row=13, column=1, sticky=tk.W, pady=4)
        tk.mainloop()

    def openembedfile(self):
        self.ifilepath.delete(0, tk.END)
        ifabspath = fd.askopenfilename(
                filetypes = [
                    ('Accepted Formats', '.wav .jpg .jpeg .gif .png'),
                    ],
                title = 'Please choose Image/Audio File'
                )
        self.ifilepath.insert(tk.END, ifabspath)

    def opendatafile(self):
        self.filepath.delete(0, tk.END)
        fabspath = fd.askopenfilename(title = 'Please choose Data File')
        self.filepath.insert(tk.END, fabspath)
        self._readfile()

    def _readfile(self):
        fabspath = self.filepath.get()
        self.mlist.delete(0, tk.END)
        if self.var1.get() == 1:
            f = open(fabspath, 'rb')
            c = f.read()
            f.close()
            self.mlist.insert(tk.END, *c.splitlines())

    def _encryptfile(self):
        self.cur_status.config(bg='red')
        fabspath = self.filepath.get()
        key = self.keyentry.get()
        self.statuslabel.set('Encrypting File')
        encryptfile(key, fabspath, fabspath)
        self.statuslabel.set('Encrypted!')
        self.cur_status.config(bg='green')
        ofilename = os.path.basename(fabspath)
        self.ofilelabel.set(f'{ofilename}')
        self._readfile()

    def _decryptfile(self):
        self.cur_status.config(bg='red')
        key = self.keyentry.get()
        fabspath = self.filepath.get()
        self.statuslabel.set('Decrypting File...')
        decryptfile(key, fabspath, fabspath)
        self.statuslabel.set('Decrypted!')
        self.cur_status.config(bg='green')
        ofilename = os.path.basename(fabspath)
        self.ofilelabel.set(f'{ofilename}')
        self._readfile()

    def _embedfile(self):
        self.cur_status.config(bg='red')
        fabspath = self.filepath.get()
        ifabspath = self.ifilepath.get()
        ifileinfo = os.path.basename(ifabspath).split('.')
        ofilename = ifileinfo[0]+'_'+str(uuid.uuid4())
        fdir = os.path.dirname(ifabspath)
        self.statuslabel.set('Embedding Encrypted File')
        if ifileinfo[1].lower() in ['jpg', 'jpeg', 'gif', 'png']:
            ofilename += '.png'
            embed_data_from_file(ifabspath, fabspath, ofilename)
        else:
            ofilename += '.wav'
            embed_file_to_wave(ifabspath, fabspath, ofilename)
        os.remove(fabspath)
        self.statuslabel.set('Data Embedded!')
        self.ofilelabel.set(f'{ofilename}')
        self.cur_status.config(bg='green')
        self.filepath.delete(0, tk.END)
        self.ifilepath.delete(0, tk.END)
        self.mlist.delete(0, tk.END)
        ofpath = os.path.join(fdir, ofilename)
        self.ifilepath.insert(tk.END, ofpath)

    def _extractfile(self):
        self.cur_status.config(bg='red')
        ifabspath = self.ifilepath.get()
        ifileinfo = os.path.basename(ifabspath).split('.')
        f = fd.asksaveasfile('wb')
        self.filepath.delete(0, tk.END)
        self.filepath.insert(tk.END, f.name)
        fabspath = self.filepath.get()
        self.statuslabel.set('Extracting Data...')
        if ifileinfo[1].lower() == 'wav':
            data = extract_data_from_wave(ifabspath)
        else:
            data = extract_data_from_image(ifabspath)
            
        os.remove(ifabspath)
        self.statuslabel.set('Extraction Done!')
        f.write(data)
        f.close()
        self.cur_status.config(bg='green')
        ofilename = os.path.basename(fabspath)
        self.ofilelabel.set(f'{ofilename}')
        self._readfile()
        self.ifilepath.delete(0, tk.END)

    def enc_and_embed(self):
        self.cur_status.config(bg='red')
        self._encryptfile()
        self._embedfile()

    def extract_and_decrypt(self):
        self.cur_status.config(bg='red')
        self._extractfile()
        self._decryptfile()

def main():
    steg = StegGui()
