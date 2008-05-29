# Copyright (C) 2006 - Elias Holzer <holzer at inf dot fu-berlin dot de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# This plugin allows you to use auto completion like you're used to it in any
# "better" console. Write the first few characters of a word you've already
# written in your text and hit <Tab>. If there are more possibilities hit
# <Tab> more times to go through the results.
# Press <Ctrl><Tab> to iterate backwards in the case you you've gone too far.
# Say you wrote a word and want to write a tabulator afterwards hit <Tab> twice.
# If you cycled through a few words, found the one you were looking for and want
# to write a tabulator, hit a key like <Shift> or <Alt> and <Tab> twice
# afterwards.
# The last word you've chosen will be the first word in the next run. Words
# you've never used will be in lexical order.

# Parts of this plugin are based on the work of Guillaume Chazarain
# (http://guichaz.free.fr/gedit-completion), especially the regular 
# expressions found in the complete_word method in the Completion class.

import gedit
import gtk
from gtk import gdk
import re
import types

class AutoCompletionPlugin(gedit.Plugin):
  
  # A list of (handler_id, view) tuples
  handler_ids = []
  
  def __init__(self):
    gedit.Plugin.__init__(self)
    
  def activate(self, window):
    # Start auto completion for the active view
    view = window.get_active_view()
    self.setup_auto_completion(view)
  
  def deactivate(self, window):
    # Disconnect all handlers which have been connected by this plugin
    for (handler_id, view) in self.handler_ids:
      view.disconnect(handler_id)
    
  def update_ui(self, window):
    # Start auto completion for the active view
    view = window.get_active_view()
    self.setup_auto_completion(view)
        
  # Starts auto completion for a given view
  def setup_auto_completion(self, view):
    if type(view) != types.NoneType:
      if getattr(view, 'completion_instance', False) == False:
        setattr(view, 'completion_instance', Completion())
        handler_id = view.connect(
          'key-press-event',
          view.completion_instance.complete_word)
        self.handler_ids.append((handler_id, view))    

class Completion:
  
  # Seperators were taken from Guillaume Chazarain
  separators  = re.escape("&\"'{([-|`)]} .,;:!?/^$\n\r*+#=<>	")
  
  def __init__(self):
    # Each word has a key to order it
    self.keys        = {}
    self.key_counter = 1
    self.reset()
    return
    
  def reset(self):
    # Boolean value. True if there are more possibilities.
    self.cycle      = False
    self.words      = []
    self.word_i     = 0
    self.last_word  = None

  def complete_word(self, view, event):
    if ((event.type == gtk.gdk.KEY_PRESS)
    and (event.keyval == gtk.gdk.keyval_from_name('Tab'))):
      # Parts of the following code were taken from the Completion Plugin
      # of Guillaume Chazarain found at http://guichaz.free.fr/gedit-completion
      buffer      = view.get_buffer()
      iter_cursor = buffer.get_iter_at_mark(buffer.get_insert())
      iter_line   = iter_cursor.copy()
      iter_word   = iter_cursor.copy()
      
      iter_line.set_line_offset(0)
      line        = buffer.get_text(iter_line, iter_cursor)
      
      if not self.cycle:
        match       = re.search("[^%s]+$" % self.separators, line)
        if not match:
          return False
          
        word        = match.group()
        if not word:
          return False
        
        self.line_index = iter_cursor.get_line_index() - len(word)
          
        text        = buffer.get_text(
                        buffer.get_start_iter(), buffer.get_end_iter())
        self.words  = re.findall("(?:\A|[%(sep)s])(%(word)s[^%(sep)s]+)" %
                        {
                          "sep":  self.separators,
                          "word": re.escape(word)
                        },
                        text)
        
        self.words[:] = frozenset(self.words)
        self.words.sort()
        self.words.sort(key=self.get_key, reverse=True)
        self.words.append(word)
      
      if len(self.words) > 1:
        if self.cycle:
          if event.get_state() == gtk.gdk.CONTROL_MASK:
            self.word_i -= 1
            if self.word_i < 0:
              self.word_i = len(self.words) - 1
          else:
            self.word_i += 1
            if self.word_i >= len(self.words):
              self.word_i = 0
        iter_word.set_line_index(self.line_index)
        buffer.delete(iter_word, iter_cursor)
        buffer.insert_at_cursor(self.words[self.word_i])
      elif len(self.words) == 1:
        if self.cycle:
          self.reset()
          return False
        iter_word.set_line_index(self.line_index)
        buffer.delete(iter_word, iter_cursor)
        buffer.insert_at_cursor(self.words[0])
      else:
        if self.cycle:
          self.reset()
          return False
      
      self.last_word  = self.words[self.word_i]
      self.cycle      = True
      return True
    elif ((event.type == gtk.gdk.KEY_PRESS)
    and ((event.keyval == gtk.gdk.keyval_from_name('Control_L'))
    or (event.keyval == gtk.gdk.keyval_from_name('Control_R')))):
      return False
    else:
      if self.cycle:
        self.update_key(self.last_word)
      self.reset()
      return False
      
  def get_key(self, word):
    if self.keys.has_key(word):
      ret = self.keys[word]
    else:
      ret = 0
    return ret
    
  def update_key(self, word):
    self.keys[word] = self.key_counter
    self.key_counter += 1
