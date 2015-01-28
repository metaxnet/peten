#!/usr/bin/env python2.7
import sys, os
sys.path.append("/usr/lib/python2.7/dist-packages/")
import pygtk
pygtk.require('2.0')
import gtk

#import pango

import subprocess

#SAMPLE = "print ''.join('%(pre)s%(num)s %(bot)s on the wall, %(nul)s %(bot)s,\n%(tak)s\n' % (lambda c,b:  {'pre':['','%s %s on the wall.\n\n' % (c,b)][abs(cmp(c,'Ninety-nine'))], 'num':c, 'nul':c.lower(), 'bot':b, 'tak':['Go to the store and buy some more... Ninety-nine %s.' % b,'Take one down, pass it around,'][abs(cmp(x,0))]  })((lambda x,o: [(['Twenty','Thirty','Forty','Fifty', 'Sixty','Seventy','Eighty','Ninety'][x/10-2]+'-'+o.lower()).replace('-no more',''), o][int(x<20)])(x, ['No more','One','Two', 'Three','Four','Five','Six','Seven','Eight', 'Nine','Ten','Eleven','Twelve','Thirteen','Fourteen', 'Fifteen','Sixteen','Seventeen','Eighteen','Nineteen'][[x,x%10][int(x>=20)]]),'bottle%s of beer' % ['','s'][abs(cmp(x,1))])  for x in xrange(99,-1,-1))"

PY_PATH = "/home/lifman/metaxnet/Peten/"
PY_SCRIPTS_PATH = "/home/lifman/metaxnet/Peten/"

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
        self.py = subprocess.Popen(['python'], stdin=subprocess.PIPE)
        self.py.stdin.write("# coding=UTF-8"+"\n")
        
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
        self.entered_commands = ["# coding=UTF-8"]+self.entered_commands
        f = open(PY_SCRIPTS_PATH+"temp.py", "wb")
        f.write("\n".join(self.entered_commands))
        f.close()

    def run(self):
        subprocess.call(["python", PY_SCRIPTS_PATH+"temp.py"])


class App:
    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode
        self.commander = Commander(self, self.debug_mode)
        self.window = gtk.Window()
        self.window.connect("destroy", self.destroy)
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
        hbox_buttons.pack_start(button_process_and_run, 0,0,False)
        vbox.pack_start(self.vpaned, 0,0,False)
        vbox.pack_start(hbox_buttons, 0,0,False)
        self.window.add(vbox)
        self.window.show_all()
        
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
        for l in lines:
            words = self.commander.tokenize(l.decode("utf-8"))
            out = []
            for word in words:
                pyword = self.commander.translate(word)
                if pyword == word and self._is_illegal(word):
                    if word not in self.needing_translation:
                        self.needing_translation.append(word)
                        pyword = "_word"+str(len(self.needing_translation))
                    else:
                        pyword = "_word"+str(self.needing_translation.index(word) + 1)
                out.append(pyword)
            self.commander.entered_commands.append("".join(out))
        if self.debug_mode:
            print "\n".join(self.commander.entered_commands)
        self.commander.process()
        self.commander.run()

    def run(self):
        self.commander.run()
        
    def add_command_line_to_textscreen(self, text):
        self.textbuffer.insert_at_cursor(text+"\n")        

    def destroy(self, event=None):
        gtk.main_quit()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    app = App()
    app.main()
