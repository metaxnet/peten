#!/usr/bin/env python2.7
import sys, os
sys.path.append("/usr/lib/python2.7/dist-packages/")
import pygtk
pygtk.require('2.0')
import gtk

#import subprocess

#EXECUTABLE = "python"
PY_PATH = "./" # Where to find translations.py etc...
#PY_SCRIPTS_PATH = "./" # Where to put scripts and where to create temp.py
JS_SCRIPTS_PATH = "/home/lifman/Phaser/game/"

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
                english, hebrew = l.split(" = ")
                self.translated[hebrew] = english
        self.reset()

    def _split_text_find_comments_and_strings(self, text):
        STRINGERS = ["\"", "'"]
        COMMENTS = ["//", "/*", "*/"]
        opener = ""
        out = []
        i = 0
        length = len(text)
        tokens = []
        token = []
        while i < length:
            if opener:
                if opener == "/*":
                    while (i < length - 1) and text[i:i+2] != "*/":
                       token.append(text[i])
                       i = i + 1
                    if (i < length -1):
                       tokens.append("".join(token)+"*/")
                       token = []
                       i = i + 2
                elif opener == "//":
                    while (i < length) and text[i] != "\n":
                       token.append(text[i])
                       i = i + 1
                    if (i < length):
                       tokens.append("".join(token)+"\n")
                       token = []
                       i = i + 1
                elif opener == "\"":
                    while (i < length) and (text[i] != "\"" or (text[i]=="\"" and token[-1]=="\\")):
                       token.append(text[i])
                       i = i + 1
                    if (i < length):
                       tokens.append("".join(token)+"\"")
                       token = []
                       i = i + 1
                elif opener == "\'":
                    while (i < length) and (text[i] != "\'" or (text[i]=="\'" and token[-1]=="\\")):
                       token.append(text[i])
                       i = i + 1
                    if (i < length):
                       tokens.append("".join(token)+"\'")
                       token = []
                       i = i + 1
                opener = ""
            else:
                if (i < length - 1) and text[i:i+2] == "/*":
                    tokens.append("".join(token))
                    opener = "/*"
                    token = ["/*"]
                    i = i + 2
                elif (i < length - 1) and text[i:i+2] == "//":
                    tokens.append("".join(token))                       
                    opener = "//"
                    token = ["//"]
                    i = i + 2
                elif (i < length) and text[i] == "\"":
                    tokens.append("".join(token))                      
                    opener = "\""
                    token = ["\""]
                    i = i + 1
                elif (i < length) and text[i] == "\'":
                    tokens.append("".join(token))                       
                    opener = "\'"
                    token = ["\'"]
                    i = i + 1
                else:
                    token.append(text[i])
                    i = i + 1
        tokens.append("".join(token))
        for token in tokens:
            print "{{{"+token+"}}}"
        return tokens
        
    def tokenize(self, text):
        SPACES = [" ","\t", "\n",",", ":"]
        BRACES = ["[", "]", "(", ")", "{", "}"]
        OPERATORS = list("+-/*^&%!=<>")
        COMMENTS = ["//", "/*", "*/"]
        i = 0
        in_string = ""
        in_comment = ""
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
        if self.debug_mode:
            #for t in tokens:
            #    print t,
            #print
            print tokens
        return tokens
                
    def reset(self):
        self.translation_comments = []
        self.entered_commands = []
        
    def handle_command_line(self, text):
        words = self.tokenize(text)
        out = []
        for word in words:
            jsword = self.translate(word)
            out.append(jsword)
        self.entered_commands.append(" ".join(out))
        #
        self.py.stdin.write(" ".join(out)+"\n")
        
    def translate(self, word):
        if word in self.translated:
            return self.translated[word]
        return word
        
    def process(self, filename):
        #if "# coding=UTF-8" in self.entered_commands:
        #    self.entered_commands.remove("# coding=UTF-8")
        self.entered_commands = self.translation_comments+self.entered_commands
        f = open(JS_SCRIPTS_PATH+filename, "wb")
        f.write("\n".join(self.entered_commands))
        f.close()

    def run(self):
        pass
        #subprocess.call([EXECUTABLE, PY_SCRIPTS_PATH+"temp.py"])


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
        agr = gtk.AccelGroup()
        self.window.add_accel_group(agr)            
        menu_bar = gtk.MenuBar()
        file_menu = gtk.Menu()
        file_menu_item = gtk.MenuItem("File")
        file_menu_item.set_submenu(file_menu)
        menu_bar.append(file_menu_item)

        open_menu_item = gtk.MenuItem("Open")
        open_menu_item.connect("activate", self.execute_file_open)
        file_menu.append(open_menu_item)
        save_menu_item = gtk.MenuItem("Save")
        key, mod = gtk.accelerator_parse("<Control>S")
        save_menu_item.add_accelerator("activate", agr, key, 
            mod, gtk.ACCEL_VISIBLE)        
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

        ffilter = gtk.FileFilter()
        ffilter.set_name("All files")
        ffilter.add_pattern("*")
        dialog.add_filter(ffilter)
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
            self.window.set_title(filename)
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
        if word[0] in ["#"]:
            return False
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

        print self.commander._split_text_find_comments_and_strings(text)

        for l in lines:
            words = self.commander.tokenize(l.decode("utf-8"))
            out = []
            for word in words:
                pyword = self.commander.translate(word)
                if pyword == word and self._is_illegal(word):
                    if word not in self.needing_translation:
                        self.needing_translation.append(word)
                        pyword = "_word"+str(len(self.needing_translation))
                        translation_comments.append("// %s = %s" % (word, pyword))
                    else:
                        pyword = "_word"+str(self.needing_translation.index(word) + 1)
                out.append(pyword)
            self.commander.entered_commands.append("".join(out))
        self.commander.translation_comments = translation_comments[:]
        if self.debug_mode:
            print "\n".join(translation_comments)
            print "\n".join(self.commander.entered_commands)
        filename = self.current_file.split("/")[-1].replace(".heb","")
        self.commander.process(filename)
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
    app = App(True)
    app.main()
