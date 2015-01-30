#!/usr/bin/env python2.7
import sys, os
sys.path.append("/usr/lib/python2.7/dist-packages/")
import pygtk
pygtk.require('2.0')
import gtk

import subprocess

EXECUTABLE = "python"
PY_PATH = "./" # Where to find translations.py etc...
PY_SCRIPTS_PATH = "./" # Where to put scripts and where to create temp.py

FRAMERS = {"\"": "\"", "'": "'", "[": "]", "{": "}", "(": ")"}
STRINGERS = ["\"", "'"]

class Commander:
    def __init__(self, app_object, debug_mode = False):
        self.debug_mode = debug_mode
        self.app = app_object
        self.translated = {}
        translations = open(PY_PATH+"translations.txt").read().decode("utf-8")
        for l in translations.split("\n"):
            if " = " in l:
                rebol, hebrew = l.split(" = ")
                self.translated[hebrew] = rebol
        self.reset()
        # For an interactive shell...
        #self.py = subprocess.Popen([EXECUTABLE], stdin=subprocess.PIPE)
        #self.py.stdin.write("# coding=UTF-8"+"\n")
        
    def tokenize(self, text):
        SPACES = [" ","\t", "\n",",", ":"]
        BRACES = ["[", "]", "(", ")", "{", "}"]
        OPERATORS = list("+-/*^&%!=<>")
        i = 0
        in_string = ""
        tokens = []
        token = []
        if self.debug_mode:
            print "Tokenizing", text
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
        if self.debug_mode:
            for t in tokens:
                print t,
            print
        return tokens
                
    def reset(self):
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
        self.py.stdin.write(" ".join(out)+"\n")
        
    def translate(self, word):
        if word in self.translated:
            return self.translated[word]
        return word
        
    def process(self):
        self.entered_commands = ["# coding=UTF-8"]+self.translation_comments+self.entered_commands
        f = open(PY_SCRIPTS_PATH+"temp.py", "wb")
        f.write("\n".join(self.entered_commands))
        f.close()

    def run(self):
        subprocess.call([EXECUTABLE, PY_SCRIPTS_PATH+"temp.py"])


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
        button_process_and_run = gtk.Button("Process and Run")
        button_process_and_run.connect("clicked", self.process_and_run)
        hbox_buttons.pack_start(button_process_and_run, False, False, 0)
        vbox.pack_start(hbox_menu, False, False, 0)
        vbox.pack_start(self.vpaned, False, False, 0)
        vbox.pack_start(hbox_buttons, False, False, 0)
        self.window.add(vbox)
        self.window.show_all()
        self.current_file = ""
        
    def create_menu(self):
        menu_bar = gtk.MenuBar()
        file_menu = gtk.Menu()
        file_menu_item = gtk.MenuItem("File")
        file_menu_item.set_submenu(file_menu)
        menu_bar.append(file_menu_item)

        open_menu_item = gtk.MenuItem("Open")
        open_menu_item.connect("activate", self.execute_file_open)
        file_menu.append(open_menu_item)
        save_menu_item = gtk.MenuItem("Save")
        save_menu_item.connect("activate", self.execute_file_save)
        file_menu.append(save_menu_item)
        save_as_menu_item = gtk.MenuItem("Save As")
        save_as_menu_item.connect("activate", self.execute_file_save_as)
        file_menu.append(save_as_menu_item)
        menu_bar.show_all()
        return menu_bar

    def _select_file(self, title, action):
        dialog = gtk.FileChooserDialog(title,
                               None,
                               action,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        #dialog.set_current_name("My FIlename")

        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        dialog.add_filter(filter)
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
            self.textbuffer.set_text(text)
            f.close()

    def _save_current_file(self):
        f = open(self.current_file, "wb")
        s, e = self.textbuffer.get_bounds()
        text = self.textbuffer.get_text(s,e)
        f.write(text)
        f.close()

    def execute_file_save(self, widget=None, event=None):
        self._save_current_file()

    def execute_file_save_as(self, widget=None, event=None):
        filename = self._select_file("Save As..", gtk.FILE_CHOOSER_ACTION_SAVE)
        if filename:
            self.current_file = filename
            self._save_current_file()
        
    def _is_illegal(self, word):
        if word[0] in ["\"", "'"] and word[-1] in ["\"", "'"]:
            return False
        for c in word:
            if ord(c) > 127 or ord(c) < 9:
                return True
        return False

    def process_and_run(self, widget=None, event=None):
        s, e = self.textbuffer.get_bounds()
        text = self.textbuffer.get_text(s, e)
        lines = text.split("\n")
        self.commander.reset()        
        self.needing_translation = []
        translation_comments = []
        for l in lines:
            words = self.commander.tokenize(l.decode("utf-8"))
            out = []
            for word in words:
                pyword = self.commander.translate(word)
                if pyword == word and self._is_illegal(word):
                    if word not in self.needing_translation:
                        self.needing_translation.append(word)
                        pyword = "_word"+str(len(self.needing_translation))
                        translation_comments.append("# %s = %s" % (word, pyword))
                    else:
                        pyword = "_word"+str(self.needing_translation.index(word) + 1)
                out.append(pyword)
            self.commander.entered_commands.append("".join(out))
        self.commander.translation_comments = translation_comments[:]
        if self.debug_mode:
            print "\n".join(translation_comments)
            print "\n".join(self.commander.entered_commands)
        self.commander.process()
        self.commander.run()

    def run(self):
        self.commander.run()
        
    #def add_command_line_to_textscreen(self, text):
    #    self.textbuffer.insert_at_cursor(text+"\n")        

    def destroy(self, event=None):
        gtk.main_quit()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    app = App()
    app.main()
