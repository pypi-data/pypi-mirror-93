''' Preview Window for SVG files '''

import sys
import os
import io
import subprocess
import queue
import threading
import time
import tkinter as tk

try:
    import cairosvg
    from PIL import Image, ImageTk
except ImportError:
    hasPIL = False
else:
    hasPIL = True
    

try:
    ipython = get_ipython()
except NameError:
    ipython = None
#else:
    # Let ipython handle TK event loop
    # so window doesn't block execution
    # in interactive mode
#    ipython.magic('gui tk')



class SVGPreview:
    ''' TK Window for displaying SVG '''
    def __init__(self, root, svgdata=None):
        self.root = root
        if svgdata:
            png = cairosvg.svg2png(bytestring=svgdata)
            self.tkimage = ImageTk.PhotoImage(Image.open(io.BytesIO(png)))
            self.label = tk.Label(self.root, image=self.tkimage)
        else:
            self.label = tk.Label(self.root)
        self.label.pack(expand=True, fill='both')
        
    def update(self, svgdata):
        png = cairosvg.svg2png(bytestring=svgdata)
        im = Image.open(io.BytesIO(png))
        self.root.geometry('{}x{}'.format(*im.size))
        self.tkimage = ImageTk.PhotoImage(im)
        self.label.config(image=self.tkimage)


# Need to handle if fig.preview window is closed
# but not None yet...
        

def display(svgdata: bytes, window=None) -> None:
    print('DISPLAY')
    if hasPIL:
        try:
            window.update(svgdata)
        except (AttributeError, tk.TclError):
            app = tk.Tk()
            print('app created')
            window = SVGPreview(app, svgdata)
            if ipython is None:
                print('starting mainloop')
                app.mainloop()  # Will block, so don't run in ipython mode
                return None     # And window isn't saved
        return window
        
    else:
        # No PIL, open in default viewer for OS
        handle, path = tempfile.mkstemp(suffix='.svg')
        with os.fdopen(handle, 'w') as f:
            f.write(svgdata.decode())

        if sys.platform == 'win32':
            os.startfile(path)
        else:
            cmd = 'open' if sys.platform == 'darwin' else 'xdg-open'
            subprocess.call([cmd, path])
        return None  # No TK window was generated
