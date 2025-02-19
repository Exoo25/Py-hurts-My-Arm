from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkcode import CodeEditor
from tkinter import ttk
import os
import sys
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # Path for bundled app
else:
    base_path = os.path.dirname(os.path.abspath(__file__))  # Path for script
app = Tk()
app.title("Py Hurts My Arm")
ico = ico = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "py.ico")
app.iconbitmap(ico)
app.geometry("800x600")
filepath = None
blockcursor = False
# Initialize Code Editor
editor = CodeEditor(app, highlighter="good", font=("Cascadia Code", 13), bg="black", undo=True, blockcursor=blockcursor, language="python")

# Menu Bar
menubar = Menu(app)
def auto_indent(event):
    current_line = editor.get("insert linestart", "insert lineend")
    if current_line.strip().endswith(":"):
        editor.insert("insert", "\n    ")
        return "break"
# Open File Function
def openf(event=None):
    global filepath
    filepath = filedialog.askopenfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
    _, path = os.name(filepath)
    if filepath:
        with open(filepath, "r") as file:
            editor.delete(1.0, END)
            editor.insert(1.0, file.read())
    editor.config(language="python")
    if path == ".html":
        editor.config(language="html")
    

# Save File Function
def savef(event=None):
    global filepath
    if filepath:
        with open(filepath, "w") as file:
            file.write(editor.get(1.0, END))
    else:
        filepath = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if filepath:
            with open(filepath, "w") as file:
                file.write(editor.get(1.0, END))

# Run Function
def run(event=None):
    global filepath
    if not filepath:
        messagebox.showerror("Error", "Please open or save a file before running it.")
    else:
        os.startfile(filepath)

# File Menu
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=openf)
filemenu.add_command(label="Save", command=savef)
filemenu.add_separator()
filemenu.add_command(label="Quit", command=lambda: app.quit())
menubar.add_cascade(label="File", menu=filemenu)

# Edit Menu
editmenu = Menu(menubar, tearoff=0)
def undo():
    try:
        # Check if there is an undo history
        if editor.index("1.0") != editor.index("insert"):  # If there's an undo history
            editor.edit_undo()
        else:
            print("Nothing to undo.")
    except TclError:
        # Handle TclError if nothing to undo
        print("Nothing to undo.")
def redo():
    try:
        # Check if there is a redo history
        editor.edit_redo()
    except TclError:
        # Handle TclError if nothing to redo
        print("Nothing to redo.")


editmenu.add_command(label="Undo", command=undo)
editmenu.add_command(label="Redo", command=redo)
editmenu.add_separator()
editmenu.add_command(label="Copy", command=lambda: editor.event_generate("<<Copy>>"))
editmenu.add_command(label="Cut", command=lambda: editor.event_generate("<<Cut>>"))
editmenu.add_command(label="Paste", command=lambda: editor.event_generate("<<Paste>>"))
menubar.add_cascade(label="Edit", menu=editmenu)
viewmenu = Menu(menubar, tearoff=0)

# Create the "Themes" submenu
themes = Menu(viewmenu, tearoff=0)
themes.add_command(label="Dracula", command=lambda:
                   editor.config(highlighter="dracula")
                   )
themes.add_command(label="VS Code", command=lambda:
                   editor.config(highlighter="good")
                   )
themes.add_command(label="Azure", command=lambda:
                   editor.config(highlighter="azure")
                   )
themes.add_command(label="Monokai+", command=lambda:
                   editor.config(highlighter="monokai-plus-plus")
                   )
themes.add_command(label="Monokai", command=lambda:
                   editor.config(highlighter="monokai")
                   )
themes.add_command(label="Mariana", command=lambda:
                   editor.config(highlighter="mariana")
                   )
# Add the "Themes" submenu to the "View" menu
viewmenu.add_cascade(label="Theme", menu=themes)
viewmenu.add_separator()
def toggle(event=None):
    global blockcursor
    blockcursor = not blockcursor
    editor.config(blockcursor=blockcursor)

viewmenu.add_command(label="Toggle Block Cursor", command=toggle)


# Add the "View" menu to the main menu bar
menubar.add_cascade(label="View", menu=viewmenu)
# Configure Menu
index = 0
themess = ["dracula", "good", "azure", "monokai", "monokai-plus-plus", "mariana"]
def toggle_theme(event=None):
    global index
    index = (index + 1) % len(themess)
    editor.config(highlighter=themess[index])
def key_binds():
    keys = Tk()
    binds = ttk.Treeview(keys,columns=("Key", "Function"), show="headings")
    binds.heading("Key", text="Key")
    binds.heading("Function", text="Function")
    binds.insert("", END, values=("Ctrl+Z", "Undo"))
    binds.insert("", END, values=("Ctrl+Y", "Redo"))
    binds.insert("", END, values=("Ctrl+O", "Open File"))
    binds.insert("", END, values=("Ctrl+S", "Save File"))
    binds.insert("", END, values=("Ctrl+Shift+B", "Toggle Block Cursor"))
    binds.insert("", END, values=("Ctrl+Shift+T", "Toogle Theme"))
    binds.insert("", END, values=("Ctrl+C", "Copy"))
    binds.insert("", END, values=("Ctrl+X", "Cut"))
    binds.insert("", END, values=("Ctrl+V", "Paste"))
    binds.insert("", END, values=("Ctrl+Shift-R", "Run"))
    binds.pack()
    keys.mainloop()
viewmenu.add_command(label="Key Binds", command=key_binds)
app.config(menu=menubar)

app.bind("<Control-o>", openf)
app.bind("<Control-s>", savef)
app.bind("<Control-Shift-B>", toggle)
app.bind("<Control-Shift-T>", toggle_theme)
app.bind("<Control-Shift-R>", run)
app.bind("<Key-Release>", auto_indent)
runbtn = Button(app, text="      ▶️", command=run, width=3)
runbtn.pack()

editor.pack(fill=BOTH, expand=True)

# Main Loop
app.mainloop()
