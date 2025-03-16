import os
import sys
import subprocess
import ast
from tkinter import *
from tkinter import filedialog, messagebox, ttk, simpledialog
from tkcode import CodeEditor
import keyboard
def auto_close_brackets(event, editor):
    char = event.char
    pairs = {'"': '"', "'": "'", '(': ')', '{': '}', '[': ']'}
    if char in pairs:
        editor.insert("insert", pairs[char])
        editor.mark_set("insert", "insert-1c")
    elif char == '\n':
        current_line = editor.get("insert linestart", "insert lineend")
        if current_line.strip().endswith(":"):
            editor.insert("insert", "\n    ")
            return "break"
    return None

def manage_snippets():
    snippets = load_snippets()

    def add_snippet():
        snippet_frame = Frame(snippet_manager, bg="gray20")
        ln.config(font=("Cascadia Code", 10))  # Make line numbers font smaller
        ln_scrollbar = Scrollbar(app, orient=VERTICAL, command=ln.yview)
        ln_scrollbar.pack(side=LEFT, fill=Y)
        ln.config(yscrollcommand=ln_scrollbar.set)
        snippet_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        Label(snippet_frame, text="Snippet Name:", bg="gray20", fg="white").grid(row=0, column=0, sticky=W, pady=5)
        Entry(snippet_frame, textvariable=snippet_name, bg="gray30", fg="white").grid(row=0, column=1, sticky=EW, pady=5)

        Label(snippet_frame, text="Snippet Code:", bg="gray20", fg="white").grid(row=1, column=0, sticky=NW, pady=5)
        snippet_code = Text(snippet_frame, height=10, bg="gray30", fg="white")
        snippet_code.grid(row=1, column=1, sticky=NSEW, pady=5)

        button_frame = Frame(snippet_frame, bg="gray20")
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        Button(button_frame, text="Add", command=save_new_snippet, bg="gray30", fg="white").pack(side=LEFT, padx=5)
        Button(button_frame, text="Delete", command=delete_snippet, bg="gray30", fg="white").pack(side=LEFT, padx=5)
        Button(button_frame, text="Insert", command=insert_snippet, bg="gray30", fg="white").pack(side=LEFT, padx=5)

        snippet_listbox = Listbox(snippet_frame, bg="gray30", fg="white")
        snippet_listbox.grid(row=3, column=0, columnspan=2, sticky=NSEW, pady=5)

        snippet_frame.grid_rowconfigure(1, weight=1)
        snippet_frame.grid_rowconfigure(3, weight=1)
        snippet_frame.grid_columnconfigure(1, weight=1)
        name = snippet_name.get()
        code = snippet_code.get("1.0", END).strip()
        if name and code:
            snippets[name] = code
            save_snippets(snippets)
            update_snippet_list()
            snippet_name.set("")
            snippet_code.delete("1.0", END)

    def save_new_snippet():
        name = snippet_name.get()
        code = snippet_code.get("1.0", END).strip()
        def add_snippet():
            name = snippet_name.get()
            code = snippet_code.get("1.0", END).strip()
            if not name:
                messagebox.showwarning("Warning", "Snippet Name cannot be empty.")
                return
            if not code:
                messagebox.showwarning("Warning", "Snippet Code cannot be empty.")
                return
            snippets[name] = code
            save_snippets(snippets)
            update_snippet_list()
            snippet_name.set("")
            snippet_code.delete("1.0", END)

        snippet_listbox = Listbox(snippet_manager, bg="gray30", fg="white")
        snippet_listbox.pack(fill=BOTH, padx=5, pady=5, expand=True)

        scrollbar = Scrollbar(snippet_manager, orient=VERTICAL, command=snippet_listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        snippet_listbox.config(yscrollcommand=scrollbar.set)
        if name and code:
            snippets[name] = code
            save_snippets(snippets)
            update_snippet_list()
            snippet_name.set("")
            snippet_code.delete("1.0", END)

    def delete_snippet():
        selected = snippet_listbox.curselection()
        if selected:
            name = snippet_listbox.get(selected)
            del snippets[name]
            save_snippets(snippets)
            update_snippet_list()

    def insert_snippet():
        selected = snippet_listbox.curselection()
        if selected:
            name = snippet_listbox.get(selected)
            editor.insert(INSERT, snippets[name])

    def update_snippet_list():
        snippet_listbox.delete(0, END)
        for name in snippets:
            snippet_listbox.insert(END, name)

    snippet_manager = Toplevel(app)
    snippet_manager.title("Snippets Manager")
    snippet_manager.geometry("400x300")
    snippet_manager.configure(bg="gray20")

    snippet_name = StringVar()
    Entry(snippet_manager, textvariable=snippet_name, bg="gray30", fg="white").pack(fill=X, padx=5, pady=5)

    snippet_code = Text(snippet_manager, height=10, bg="gray30", fg="white")
    snippet_code.pack(fill=BOTH, padx=5, pady=5, expand=True)

    button_frame = Frame(snippet_manager, bg="gray20")
    button_frame.pack(fill=X, padx=5, pady=5)

    Button(button_frame, text="Add", command=add_snippet, bg="gray30", fg="white").pack(side=LEFT, padx=5, pady=5)
    Button(button_frame, text="Delete", command=delete_snippet, bg="gray30", fg="white").pack(side=LEFT, padx=5, pady=5)
    Button(button_frame, text="Insert", command=insert_snippet, bg="gray30", fg="white").pack(side=LEFT, padx=5, pady=5)

    snippet_listbox = Listbox(snippet_manager, bg="gray30", fg="white")
    snippet_listbox.pack(fill=BOTH, padx=5, pady=5, expand=True)
    update_snippet_list()
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # Path for bundled app
else:
    base_path = os.path.dirname(os.path.abspath(__file__))  # Path for script

app = Tk()
app.title("Py Hurts My Arm - Pro")
ico = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "py.ico")
app.iconbitmap(ico)
filepath = None
blockcursor = False

# Initialize Code Editor
editor = CodeEditor(app, highlighter="good", font=("Cascadia Code", 11), bg="black", undo=True, blockcursor=blockcursor, language="python")
editor = CodeEditor(app, highlighter="good", font=("Cascadia Code", 11), bg="black", undo=True, blockcursor=blockcursor, language="python")
ln = Text(app, width=3, bg="gray20", fg="white", state="disabled", height=20, font=("Cascadia Code", 11))
from tkinter.simpledialog import askinteger
ln_scrollbar = Scrollbar(app, orient=VERTICAL, command=ln.yview)
ln_scrollbar.pack(side=LEFT, fill=Y)
ln.config(yscrollcommand=ln_scrollbar.set)

def up(event=None):
    ln.config(state="normal")
    ln.delete("1.0", "end")
    line_numbers = "\n".join(map(str, range(1, editor.get("1.0", "end").count("\n") + 1)))
    ln.insert("1.0", line_numbers)
    ln.config(state="disabled")
    editor.yview_moveto(ln.yview()[0])

# Bind the <<Modified>> event to the up function
editor.bind("<<Modified>>", up)

# Auto-Save Function
def auto_save():
    global filepath
    if filepath:
        with open(filepath, "w", encoding='utf-8') as file:
            file.write(editor.get(1.0, END))
    # Schedule auto-save every 1 millisecond (1000 ms)
    app.after(1, auto_save)
from tkinter.simpledialog import askinteger

def jump_to_line():
    line_number = askinteger("Jump to Line", "Enter line number:", minvalue=1, maxvalue=10000)
    if line_number is not None:
        editor.mark_set("insert", f"{line_number}.0")  # Move the cursor to the beginning of the specified line
        editor.see(f"{line_number}.0")  # Ensure the line is visible

# Menu Option for Jump to Line
# Menu Bar
menubar = Menu(app)

# Open File Function
def openf(event=None):
    global filepath
    filepath = filedialog.askopenfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("HTML Files", "*.html"), ("All Files", "*.*")])
    if filepath:
        _, path = os.path.splitext(filepath)
        path = path.lower()
        with open(filepath, "r") as file:
            editor.delete(1.0, END)
            editor.insert(1.0, file.read())
        if path == ".css":
            editor.config(language="css")
        elif path == ".js":
            editor.config(language="javascript")
        elif path == ".sh":
            editor.config(language="bash")
        elif path == ".md":
            editor.config(language="markdown")
        elif path == ".txt":
            editor.config(language="plaintext")
        elif path == ".bat":
            editor.config(language="batch")
        else:
            editor.config(language="python")
def jump_to_line():
    line_number = askinteger("Jump to Line", "Enter line number:", minvalue=1, maxvalue=10000)
    if line_number is not None:
        total_lines = int(editor.index('end-1c').split('.')[0])
        if line_number > total_lines:
            line_number = total_lines
        elif line_number < 1:
            line_number = 1
        editor.mark_set("insert", f"{line_number}.0")  # Move the cursor to the beginning of the specified line
        editor.see(f"{line_number}.0")  # Ensure the line is visible
        ln.yview_moveto((line_number - 1) / total_lines)  # Scroll line numbers
        editor.yview_moveto((line_number - 1) / total_lines)  # Scroll code editor
        editor.config(language="json")

# Save File Function
def savef(event=None):
    global filepath
    if filepath:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(editor.get(1.0, END))
    else:
        filepath = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        
    snippets = load_snippets()

snippets_file = os.path.join(base_path, "snippets.json")

def load_snippets():
    if os.path.exists(snippets_file):
        with open(snippets_file, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                def manage_snippets():
                    snippets = load_snippets()

                    def add_snippet():
                        name = snippet_name.get()
                        code = snippet_code.get("1.0", END).strip()
                        if name and code:
                            snippets[name] = code
                            save_snippets(snippets)
                            update_snippet_list()
                            snippet_name.set("")
                            snippet_code.delete("1.0", END)

                    def delete_snippet():
                        selected = snippet_listbox.curselection()
                        if selected:
                            name = snippet_listbox.get(selected)
                            del snippets[name]
                            save_snippets(snippets)
                            update_snippet_list()

                    def insert_snippet():
                        selected = snippet_listbox.curselection()
                        if selected:
                            name = snippet_listbox.get(selected)
                            editor.insert(INSERT, snippets[name])

                    def update_snippet_list():
                        snippet_listbox.delete(0, END)
                        for name in snippets:
                            snippet_listbox.insert(END, name)

                    snippet_manager = Toplevel(app)
                    snippet_manager.title("Snippets Manager")
                    snippet_manager.geometry("400x300")

                    snippet_name = StringVar()
                    Entry(snippet_manager, textvariable=snippet_name).pack(fill=X, padx=5, pady=5)

                    snippet_code = Text(snippet_manager, height=10)
                    snippet_code.pack(fill=BOTH, padx=5, pady=5, expand=True)

                    button_frame = Frame(snippet_manager)
                    button_frame.pack(fill=X, padx=5, pady=5)

                    Button(button_frame, text="Add", command=add_snippet).pack(side=LEFT, padx=5, pady=5)
                    Button(button_frame, text="Delete", command=delete_snippet).pack(side=LEFT, padx=5, pady=5)
                    Button(button_frame, text="Insert", command=insert_snippet).pack(side=LEFT, padx=5, pady=5)

                    snippet_listbox = Listbox(snippet_manager)
                    snippet_listbox.pack(fill=BOTH, padx=5, pady=5, expand=True)
                    update_snippet_list()
                return {}
    return {}

def save_snippets(snippets):
    with open(snippets_file, "w", encoding="utf-8") as file:
        json.dump(snippets, file, indent=4)

def manage_snippets():
    snippets = load_snippets()

    def add_snippet():
        name = snippet_name.get()
        code = snippet_code.get("1.0", END).strip()
        if name and code:
            snippets[name] = code
            save_snippets(snippets)
            update_snippet_list()
            snippet_name.set("")
            snippet_code.delete("1.0", END)

    def delete_snippet():
        selected = snippet_listbox.curselection()
        if selected:
            name = snippet_listbox.get(selected)
            del snippets[name]
            save_snippets(snippets)
            update_snippet_list()

    def insert_snippet():
        selected = snippet_listbox.curselection()
        if selected:
            name = snippet_listbox.get(selected)
            editor.insert(INSERT, snippets[name])

    def update_snippet_list():
        snippet_listbox.delete(0, END)
        for name in snippets:
            snippet_listbox.insert(END, name)

    snippet_manager = Toplevel(app)
    snippet_manager.title("Snippets Manager")
    snippet_manager.geometry("400x300")

    snippet_name = StringVar()
    Entry(snippet_manager, textvariable=snippet_name).pack(fill=X, padx=5, pady=5)

    snippet_code = Text(snippet_manager, height=10)
    snippet_code.pack(fill=BOTH, padx=5, pady=5, expand=True)

    button_frame = Frame(snippet_manager)
    button_frame.pack(fill=X, padx=5, pady=5)

    Button(button_frame, text="Add", command=add_snippet).pack(side=LEFT, padx=5, pady=5)
    Button(button_frame, text="Delete", command=delete_snippet).pack(side=LEFT, padx=5, pady=5)
    Button(button_frame, text="Insert", command=insert_snippet).pack(side=LEFT, padx=5, pady=5)

    snippet_listbox = Listbox(snippet_manager)
    snippet_listbox.pack(fill=BOTH, padx=5, pady=5, expand=True)
    update_snippet_list()

# Run Function

def run(event=None):
    global filepath
    if not filepath:
        messagebox.showerror("Error", "Please open or save a file before running it.")
    else:
        # Ensure embedded Python exists
        
        # Run script using embedded Python
        process = subprocess.Popen(["python", filepath], creationflags=subprocess.CREATE_NEW_CONSOLE)
        start_time = time.time()

        while time.time() - start_time < 10:
            app.update()
        
        if keyboard.is_pressed("ctrl+shift+c"):
            process.kill()

# Compile to EXE Function (Fixing the issue)
def compiler(event=None):
    try:
        subprocess.run(["auto-py-to-exe"], check=True)
        messagebox.showinfo("Success", "auto-py-to-exe has been launched.\nFollow the GUI to create your EXE file.")
    except FileNotFoundError:
        messagebox.showerror("Error", "auto-py-to-exe is not installed.\nInstall it using: pip install auto-py-to-exe")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to open auto-py-to-exe: {e}")
# Error Detection Function
import traceback
import json
from tkinter import Scrollbar
import time

def detect_errors(event=None):
    global filepath
    if not filepath:
        messagebox.showerror("Error", "Please open or save a file before checking for errors.")
    else:
        try:
            with open(filepath, "r") as file:
                code = file.read()
                ast.parse(code)  # Try to parse the code for syntax errors
            exec(code)  # Try to execute the code to catch runtime errors
            messagebox.showinfo("Success", "No errors detected.")
        except Exception as e:
            error_message = traceback.format_exception_only(type(e), e)[0].strip()
            tb = traceback.extract_tb(sys.exc_info()[2])[-1]
            lineno = tb.lineno
            error_message += f" on line {lineno}"
            messagebox.showerror("Error", f"Error detected:\n{error_message}")

# File Menu
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=openf)
filemenu.add_command(label="Save", command=savef)
filemenu.add_separator()
filemenu.add_command(label="Compiler", command=compiler)
filemenu.add_separator()
filemenu.add_command(label="Quit", command=lambda: app.quit())
menubar.add_cascade(label="File", menu=filemenu)

# Edit Menu
editmenu = Menu(menubar, tearoff=0)
def undo():
    try:
        editor.edit_undo()
    except TclError:
        print("Nothing to undo.")
def redo():
    try:
        editor.edit_redo()
    except TclError:
        print("Nothing to redo.")

editmenu.add_command(label="Undo", command=undo)
editmenu.add_command(label="Redo", command=redo)
editmenu.add_separator()
editmenu.add_command(label="Copy", command=lambda: editor.event_generate("<<Copy>>"))
editmenu.add_command(label="Cut", command=lambda: editor.event_generate("<<Cut>>"))
editmenu.add_command(label="Paste", command=lambda: editor.event_generate("<<Paste>>"))
menubar.add_cascade(label="Edit", menu=editmenu)

# View Menu
viewmenu = Menu(menubar, tearoff=0)

# Create the "Themes" submenu
themes = Menu(viewmenu, tearoff=0)
themes.add_command(label="Dracula", command=lambda: editor.config(highlighter="dracula"))
themes.add_command(label="Better Default", command=lambda: editor.config(highlighter="good"))
themes.add_command(label="Azure", command=lambda: editor.config(highlighter="azure"))
themes.add_command(label="Monokai+", command=lambda: editor.config(highlighter="monokai-plus-plus"))
themes.add_command(label="Monokai", command=lambda: editor.config(highlighter="monokai"))
themes.add_command(label="Mariana", command=lambda: editor.config(highlighter="mariana"))
themes.add_command(label="Vs code", command=lambda: editor.config(highlighter="vscode"))
viewmenu.add_cascade(label="Theme", menu=themes)
print()
def toggle(event=None):
    global blockcursor
    blockcursor = not blockcursor
    editor.config(blockcursor=blockcursor)

viewmenu.add_command(label="Toggle Block Cursor", command=toggle)
viewmenu.add_command(label="Jump to Line", command=jump_to_line)
viewmenu.add_separator()

# Configure Menu
index = 0
themess = ["dracula", "good", "azure", "monokai", "monokai-plus-plus", "mariana"]
def toggle_theme(event=None):
    global index
    index = (index + 1) % len(themess)
    editor.config(highlighter=themess[index])

def auto_indent(event):
    current_line = editor.get("insert linestart", "insert lineend")
    if current_line.strip().endswith(":"):
        editor.insert("insert", "\n    ")
        return "break"

editor.bind("<Return>", auto_indent)
def repl(event=None):
    os.system("start output/repl.exe")
def key_binds():
    keys = Tk()
    binds = ttk.Treeview(keys, columns=("Key", "Function"), show="headings")
    binds.heading("Key", text="Key")
    binds.heading("Function", text="Function")
    binds.insert("", END, values=("Ctrl+Z", "Undo"))
    binds.insert("", END, values=("Ctrl+Y", "Redo"))
    binds.insert("", END, values=("Ctrl+O", "Open File"))
    binds.insert("", END, values=("Ctrl+S", "Save File"))
    binds.insert("", END, values=("Ctrl+Shift+B", "Toggle Block Cursor"))
    binds.insert("", END, values=("Ctrl+Shift+T", "Toggle Theme"))
    binds.insert("", END, values=("Ctrl+C", "Copy"))
    binds.insert("", END, values=("Ctrl+X", "Cut"))
    binds.insert("", END, values=("Ctrl+V", "Paste"))
    binds.insert("", END, values=("Ctrl+Shift+R", "Run"))
    binds.insert("", END, values=("Ctrl+Shift+C", "Compile to EXE"))
    binds.insert("", END, values=("Ctrl+Shift+E", "Detect Errors"))
    binds.insert("", END, values=("Ctrl+Shift+K", "REPL"))
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(keys, orient="vertical", command=binds.yview)
    binds.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    binds.pack()
    keys.mainloop()
viewmenu.add_command(label="Key Binds", command=key_binds)


menubar.add_cascade(label="View", menu=viewmenu)

# Configure main window
app.config(menu=menubar)
up()
# Key Bindings
app.bind("<Control-o>", openf)
app.bind("<Control-s>", savef)
app.bind("<Control-Shift-B>", toggle)
app.bind("<Control-Shift-T>", toggle_theme)

app.bind("<Control-Shift-R>", run)
app.bind("<Control-Shift-C>", compiler)

# Terminal Function
def open_terminal(event=None):
    subprocess.Popen(f"start cmd \k cd {base_path}", shell=True)

app.bind("<Control-Shift-T>", open_terminal)
app.bind("<Control-Shift-E>", detect_errors)
app.bind("<Control-Shift-K>", repl)
def bothh(event=None):
    auto_close_brackets(event, editor)
    up()
editor.bind("<Key>", bothh)

# Run Button
frame = Frame(app)
Label(frame, text="                                               ").grid(row=0, column=0)
runbtn = Button(frame, text=" ▶", command=run, width=3, fg="#2bff44", bg="#14131a")
runbtn.grid(row=0, column=1)
Label(frame, text=" ").grid(row=0, column=2)
detect_e_button = Button(frame, text="❌", command=detect_errors, width=3, fg="red", bg="#14131a")
detect_e_button.grid(row=0, column=3)
Label(frame, text=" ").grid(row=0, column=4)
r_button = Button(frame, text=">_", command=repl, width=3, fg="orange", bg="#14131a", font=("Cascadia Code", 8, "bold"))
r_button.grid(row=0, column=5)
Label(frame, text="       ").grid(row=1, column=0)
frame.pack(fill="x")
# Editor Pack
ln.pack(side="left", fill="y")
editor.pack(fill="both", expand=True)
# Start Auto-Save
auto_save()


editmenu.add_separator()
editmenu.add_command(label="Snippets Manager", command=manage_snippets)
toggle_line_number = True
def toggle_line_numbers():
    global toggle_line_number
    toggle_line_number = not toggle_line_number
    if toggle_line_number:
        ln_scrollbar.pack(side=LEFT, fill=Y)
        ln.pack(side="left", fill="y")
        editor.pack(side="right", fill="both", expand=True)
    else:
        ln.pack_forget()
        ln_scrollbar.pack_forget()
def change_font_size():
    size = askinteger("Font Size", "Enter new font size:", minvalue=6, maxvalue=72)
    if size:
        editor.config(font=("Cascadia Code", size))
        ln.config(font=("Cascadia Code", size))
def template(code):
    editor.insert(index=1.0, content=code)
templatemenu = Menu(editmenu, tearoff=0)
templatemenu.add_command(label="Flask WebApp", command=lambda: template("from flask import *\napp = Flask(__init__)\n@app.route('/')\napp.run(debug=True)"))
templatemenu.add_command(label="tkinter app", command=lambda: template("from tkinter import *\napp = Tk()\napp.title('test')\nlabel = Label(app, text='hello world')\nlabel.pack()\n app.mainloop()"))
templatemenu.add_command(label="pygame window", command=lambda: template("""import pygame

# Initialize Pygame
pygame.init()

# Set window size
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set window title
pygame.display.set_caption("My Pygame Window")

# Colors
WHITE = (255, 255, 255)
# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Close window when "X" is clicked
            running = False

    # Fill the screen with white
    screen.fill(WHITE)

    # Update display
    pygame.display.flip()

# Quit Pygame properly
pygame.quit()
"""))
templatemenu.add_command(label="string methods", command=lambda:template(""""""))
templatemenu.add_command(label="class object", command=lambda: template("from time import sleep\nclass main:\n  def __init__(self):\n   print('hello world')\nsleep(2)\nif __name__ == '__main__':\n   main()"))
templatemenu.add_command(label="calculator", command=lambda: template("""def calculator(a, b, operation):\n    if operation == \"plus\":\n        return a + b\n    elif operation == \"minus\":\n        return a - b\n    elif operation == \"multiply\":\n        return a * b\n    elif operation == \"divide\":\n        return a / b if b != 0 else \"Cannot divide by zero\"\n    elif operation == \"absolute\":\n        return abs(a), abs(b)\n    elif operation == \"power\":\n        return a ** b\n    else:\n        return \"Invalid operation\"\n"""""))
viewmenu.add_command(label="Change Font Size", command=change_font_size)
viewmenu.add_command(label="toggle line numbers", command=toggle_line_numbers)
editmenu.add_cascade(menu=templatemenu, label="Template")
# Main Loop
app.mainloop()
