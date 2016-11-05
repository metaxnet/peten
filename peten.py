# coding=UTF-8
from gi import pygtkcompat
pygtkcompat.enable() 
pygtkcompat.enable_gtk(version='3.0')

import sys, os
sys.path.append("/usr/lib/python2.7/dist-packages/")
import pygtk
import gtk

import subprocess

EXECUTABLE = "python3"
#EXECUTABLE = "C:\Python34\python.exe"
PY_PATH = os.path.join(".","") # Where to find translations.py etc...
PY_SCRIPTS_PATH = os.path.join(".","") # Where to put scripts and where to create temp.py

FRAMERS = {"\"": "\"", "'": "'", "[": "]", "{": "}", "(": ")"}
STRINGERS = ["\"", "'"]

COMMENTS_BEGIN = "### PETEN TRANSLATION COMMENTS ###"
COMMENTS_END = "### END OF TRANSLATION COMMENTS ###"
DUMMY_COMMENT = "# "+ "המונח_בעברית"+ " = " + "python_or_english_translation"

NEWLINE = os.linesep #"\r\n"

class Commander:
    def __init__(self, app_object, debug_mode = False):
        self.debug_mode = debug_mode
        self.app = app_object
        self.dictionary_files = []
        self.reset()
        # For an interactive shell...
        #self.py = subprocess.Popen([EXECUTABLE], stdin=subprocess.PIPE)
        #self.py.stdin.write("# coding=UTF-8"+"\n")
        
    def tokenize(self, text, debug_mode = False):
        SPACES = [" ","\t", "\r", "\n",",", ":", ";"]
        BRACES = ["[", "]", "(", ")", "{", "}"]
        OPERATORS = list("+-/*^&%!=<>")
        COMMENTS = ["#"]
        i = 0
        in_string = ""
        in_comment = ""
        tokens = []
        token = []
        if debug_mode:
            print(text)
        while i < len(text):
            #If we're inside an open string, add char to current token
            if in_string:
                token.append(text[i])
                #Check if char closes the string. If so - we're not in string anymore
                if text[i] == in_string:
                    in_string = ""
                    tokens.append("".join(token))
                    token = []
                elif text[i] == "\\" and i < len(text)-1:
                    token.append(text[i+1])
                    i = i + 1
                i = i + 1
            elif in_comment:
                token.append(text[i])
                if text[i] == "\n":
                    tokens.append("".join(token))
                    token = []
                    in_comment = ""
                i = i + 1
            elif text[i] in COMMENTS:
                if token:
                    tokens.append("".join(token))                   
                token = [text[i]]
                in_comment = text[i]
                i = i + 1
            elif text[i] in ["\"", "'"]:
                if token:
                    tokens.append("".join(token))
                token = [text[i]]
                in_string = text[i]
                i = i + 1
            elif text[i] in SPACES + BRACES + OPERATORS + ["."]:
                if token:
                    tokens.append("".join(token))
                tokens.append(text[i])
                token = []
                i = i + 1
            else:
                token.append(text[i])
                i = i + 1
                
        if token:
            tokens.append("".join(token))
        if debug_mode:
            print (tokens)
        return tokens

    def _update_translations_with_hebrew_and_code(self, hebrew, code, debug_mode = False):
        if hebrew not in self.translated.keys() and code not in self.translated.values():
            self.translated[hebrew] = code
            return True
        elif hebrew in self.translated.keys() and self.translated[hebrew] == code:
            pass
            return True
        elif hebrew in self.translated.keys() and code in self.translated.values():
            if debug_mode:
                print ("I have a translation for", hebrew, "and", code, "is already taken!")
            return False
        elif hebrew in self.translated.keys() and code not in self.translated.values():
            if debug_mode:
                print ("I have a translation for", hebrew, "-", self.translated[hebrew], ". You suggested", code, ".")
            return False
        elif hebrew not in self.translated.keys():
            existing = [x for x in self.translated if self.translated[x] == code][0]
            if debug_mode:
                print ("Python", code, "was already used to translate", existing, ".")
            return False

    def _update_translations_from_file(self, filename):
        translations = open(filename, "rb").read().decode("utf-8")
        for l in translations.split(NEWLINE):
            if " = " in l:
                code, hebrew = l.split(" = ")
                if not self._update_translations_with_hebrew_and_code(hebrew, code):
                    return False
        return True

    def update_translations_from_comments(self, text, debug_mode=False):
        lines = text.split("\n")
        comments_section_flag = False
        for l in lines:
            if l == COMMENTS_BEGIN:
                comments_section_flag = True
            elif l == COMMENTS_END:
                comments_section_flag = False
            elif comments_section_flag:
                items = l.split(" ")
                if len(items) == 4 and items[0] == "#" and items[2] == "=":
                     if debug_mode:
                         print ("Updating!", items[1], items[3])
                     self._update_translations_with_hebrew_and_code(items[1], items[3])
            

        
    def add_dictionary_file(self, filename):
        if filename not in self.dictionary_files:
             self.dictionary_files.append(filename)
                
    def reset(self):
        self.translated = {}
        self._update_translations_from_file(PY_PATH+"translations.txt")
        self.all_ok = True
        for filename in self.dictionary_files:
            try:
                if not self._update_translations_from_file(filename):
                    self.all_ok = False
                    return 
            except:
                self.all_ok = False
                return
        #
        self.translation_comments = []
        self.entered_commands = []
        
    def handle_command_line(self, text):
        words = self.tokenize(text)
        out = []
        for word in words:
            pyword = self.translate(word)
            out.append(pyword)
        self.entered_commands.append(" ".join(out))
        #
        self.py.stdin.write(" ".join(out)+NEWLINE)
        
    def get_translation_dic(self):
        return self.translated

    def translate(self, word, debug_mode=False):
        if word in self.translated:
            return self.translated[word]
        if word in " +-=%*/.()[]{}:!,<>0123456789":
            return word
        elif word and word[0] in "\"\'" and word[-1] in "\"\'":
            return word
        if debug_mode:
            print ("Got", word, [word], "not in:", end="")
            for k in self.translated.keys():
                print (k, [k], end="")
            print ()
        return word
        
    def _is_illegal(self, word):
        if word[0] in ["#"]:
            return False
        if word[0] in ["\"", "'"] and word[-1] in ["\"", "'"]:
            return False
        for c in word:
            if ord(c) > 127 or ord(c) < 9:
                return True
        return False

    def process(self, filename=None):
        if not filename:
            filename = PY_SCRIPTS_PATH+"temp.py"
        if "# coding=UTF-8" in self.entered_commands:
            self.entered_commands.remove("# coding=UTF-8")
        self.entered_commands = ["# coding=UTF-8"]+self.entered_commands+self.translation_comments
        f = open(filename, "wb")
        new_text = NEWLINE.join(self.entered_commands)
        f.write(bytes(new_text,"utf8"))
        f.close()

    def run(self, filename=None):
        print("Run")
        if not filename:
            filename = PY_SCRIPTS_PATH+"temp.py"
        subprocess.call([EXECUTABLE, filename])
        print("Done")


test_data = [
    { 'column0' : 'test00', 'column1' : 'test01', 'f': '#EEFFDD', 'b': '#EEEEEE' },
    { 'column0' : 'test10', 'column1' : 'test11', 'f': '#FF0000', 'b': '#C9C9C9' },
    { 'column0' : 'test20', 'column1' : 'test21', 'f': '#00FF00', 'b': '#FF0000' }]

class TranslationstWindow(gtk.Window):
    def __init__(self, dictionary):
        gtk.Window.__init__(self)
        scrolled = gtk.ScrolledWindow()
        # create list storage        
        store = gtk.ListStore(str, str, str, str)
        words = [x for x in dictionary.keys()]
        words.sort()
        for word in words:
            store.append([word, dictionary[word], '#FFEEF0', '#FFFFFF'])
        treeview = gtk.TreeView(store)

        # define columns
        column0 = gtk.TreeViewColumn("Python", gtk.CellRendererText(), text=1, background=2)        
        treeview.append_column(column0)            
        column1 = gtk.TreeViewColumn("Hebrew", gtk.CellRendererText(), text=0, background=3)        
        treeview.append_column(column1)

        scrolled.add_with_viewport(treeview)
        self.add(scrolled)
        self.connect("destroy", lambda w: gtk.main_quit())
        self.connect("delete_event", lambda w, e: gtk.main_quit())
        self.show_all()


class App:
    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode
        self.commander = Commander(self, self.debug_mode)
        self.window = gtk.Window()
        self.window.connect("destroy", self.destroy)
        hbox_menu = gtk.HBox()
        menu = self.create_menu()
        hbox_menu.pack_start(menu, False, False, 0)
        vbox = gtk.VBox()
        self.textbuffer = gtk.TextBuffer()
        self.textview = gtk.TextView()
        self.textview.set_buffer(self.textbuffer)
        self.scrolled2 = gtk.ScrolledWindow()
        self.scrolled2.set_size_request(800, 600)
        self.scrolled2.add_with_viewport(self.textview)
        self.vpaned = gtk.VPaned()
        self.vpaned.add2(self.scrolled2)
        hbox_buttons = gtk.HBox()
        button_process = gtk.Button("לעבד")
        button_process.connect("clicked", self.process)
        button_process_and_run = gtk.Button("לעבד ולהריץ")
        button_process_and_run.connect("clicked", self.process_and_run)
        button_show_translations = gtk.Button("להציג מילון")
        button_show_translations.connect("clicked", self.show_translations)
        hbox_buttons.pack_start(button_process, False, False, 0)
        hbox_buttons.pack_start(button_process_and_run, False, False, 0)
        hbox_buttons.pack_start(button_show_translations, False, False, 0)
        vbox.pack_start(hbox_menu, False, False, 0)
        vbox.pack_start(self.vpaned, False, False, 0)
        vbox.pack_start(hbox_buttons, False, False, 0)
        self.window.add(vbox)
        self.window.show_all()
        self.current_file = ""
        
    def create_menu(self):
        menu_bar = gtk.MenuBar()
        file_menu = gtk.Menu()
        file_menu_item = gtk.MenuItem("קובץ")
        file_menu_item.set_submenu(file_menu)
        menu_bar.append(file_menu_item)

        open_menu_item = gtk.MenuItem("לפתוח")
        open_menu_item.connect("activate", self.execute_file_open)
        file_menu.append(open_menu_item)
        save_menu_item = gtk.MenuItem("לשמור")
        save_menu_item.connect("activate", self.execute_file_save)
        file_menu.append(save_menu_item)
        save_as_menu_item = gtk.MenuItem("לשמור בשם")
        save_as_menu_item.connect("activate", self.execute_file_save_as)
        file_menu.append(save_as_menu_item)
        menu_bar.show_all()
        return menu_bar


    # File Operations
    def _select_file(self, title, action):
        dialog = gtk.FileChooserDialog(title,
                               None,
                               action,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        #dialog.set_current_name("My FIlename")

        ff = gtk.FileFilter()
        ff.set_name("All files")
        ff.add_pattern("*")
        dialog.add_filter(ff)
        response = dialog.run()
        filename = ""
        if response == gtk.RESPONSE_OK:
             filename = dialog.get_filename()        
        dialog.destroy()
        return filename
        
    def execute_file_open(self, widget=None, event=None):
        filename = self._select_file("Open...", gtk.FILE_CHOOSER_ACTION_OPEN)
        if filename:
            self.current_file = filename
            f = open(self.current_file, "rb")
            text = f.read()
            self.textbuffer.set_text(text.decode("utf8"))
            f.close()

    def _save_current_file(self):
        f = open(self.current_file, "w")
        s, e = self.textbuffer.get_bounds()
        text = self.textbuffer.get_text(s,e, False)
        f.write(text)
        f.close()

    def execute_file_save(self, widget=None, event=None):
        self._save_current_file()

    def execute_file_save_as(self, widget=None, event=None):
        filename = self._select_file("Save As..", gtk.FILE_CHOOSER_ACTION_SAVE)
        if filename:
            self.current_file = filename
            self._save_current_file()        

    # Processing & Running
    def get_text(self):
        s, e = self.textbuffer.get_bounds()
        text = self.textbuffer.get_text(s, e, False)
        return text

    def translate(self, text, debug_mode=False):
        self.commander.reset()
        if debug_mode:
            print (len(self.commander.translated.keys()), "Words in dictionary")
        try:
            translations_text = open(self.current_file+".translations", "rb").read().decode("utf8")
            self.commander.update_translations_from_comments(translations_text)
            translation_comments = translations_text.split(NEWLINE)
        except:
            translations_text = NEWLINE.join([COMMENTS_BEGIN] + [DUMMY_COMMENT] + [COMMENTS_END])
            f = open(self.current_file+".translations", "w")
            f.write(translations_text)
            f.close()
            translation_comments = []

        if debug_mode:
            print (len(self.commander.translated.keys()), "Words in dictionary after update")
            for k in self.commander.translated.keys():
                print (k, self.commander.translated[k])

        lines = text.split(NEWLINE)
        needing_translation = []
        translation_comments = []
        translation_comments_index = len(self.commander.translated.keys())
        for l in lines:
            words = self.commander.tokenize(l) #.decode("utf-8"))
            out = []
            for word in words:
                pyword = self.commander.translate(word)
                if pyword == word and self.commander._is_illegal(word):
                    if debug_mode:
                        print ("Translating", word)
                    if word not in needing_translation:
                        needing_translation.append(word)
                        pyword = "_word"+str(translation_comments_index)
                        translation_comments_index = translation_comments_index +1
                        translation_comments.append("# %s = %s" % (word, pyword))
                        self.commander.translated[word] = pyword
                    else:
                        pyword = "_word"+str(needing_translation.index(word) + 1)
                out.append(pyword)
            self.commander.entered_commands.append("".join(out))
        self.commander.translation_comments = translation_comments[:]
        if debug_mode:
            print (NEWLINE.join(translation_comments))
            print (NEWLINE.join(self.commander.entered_commands))

    def process(self, widget=None, event=None):
        text = self.get_text()
        self.translate(text)
        outfile = None
        if self.current_file.endswith(".peten"):
            outfile = self.current_file.replace(".peten", ".py")
        self.commander.process(outfile)

    def process_and_run(self, widget=None, event=None):
        text = self.get_text()
        self.translate(text)
        outfile = None
        if self.current_file.endswith(".peten"):
            outfile = self.current_file.replace(".peten", ".py")
        self.commander.process(outfile)
        self.commander.run(outfile)

    def run(self):
        outfile = None
        if self.current_file.endswith(".peten"):
            outfile = self.current_file.replace(".peten", ".py")
        self.commander.run(outfile)

    def show_translations(self, event=None):
        self.translations = TranslationstWindow(self.commander.get_translation_dic())

    def destroy(self, event=None):
        gtk.main_quit()

    def main(self):
        gtk.main()

def process_and_run_no_GUI(filename, debug_mode=True):
    commander = Commander(None, debug_mode)        
    text = open(filename, "r").read()
    try:
        translations_text = open(filename+".translations", "r").read()
        commander.update_translations_from_comments(translations_text)
        translation_comments = translations_text.split(NEWLINE)
    except:
        text = "".join([COMMENTS_BEGIN] + [DUMMY_COMMENT] + [COMMENTS_END])
        f = open(filename+".translations", "w")#
    
        f.write(text)
        f.close()
        translation_comments = []

    needing_translation = []
    lines = str(text).split(NEWLINE)
    for l in lines:
        print (l, type(l))
        words = commander.tokenize(l) #.decode("utf-8"))
        print ("WORDS:"+NEWLINE, words)
        pyline = []
        for word in words:
            pyword = commander.translate(word)
            if pyword == word and commander._is_illegal(word):
                if word not in needing_translation:
                    needing_translation.append(word)
                    pyword = "_word"+str(len(needing_translation))
                    translation_comments.append("# %s = %s" % (word, pyword))
                else:
                    pyword = "_word"+str(needing_translation.index(word) + 1)
            pyline.append(pyword)
        commander.entered_commands.append("".join(pyline))
    if COMMENTS_BEGIN not in translation_comments:
        commander.translation_comments = [COMMENTS_BEGIN] + translation_comments[:] + [COMMENTS_END]
    if debug_mode:
        print (NEWLINE.join(commander.entered_commands))
        print (NEWLINE.join(translation_comments))
    outfile = None
    if filename.endswith(".peten"):
        outfile = filename.replace(".peten", ".py")
    commander.process(outfile)
    commander.run(outfile)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        app = App(True)
        app.main()
    else:
        process_and_run_no_GUI(sys.argv[1])
