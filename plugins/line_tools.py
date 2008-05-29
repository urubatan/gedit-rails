# -*- coding: utf8 -*-
#  Line Tools Plugin
#
#  Copyright (C) 2007 Shaddy Zeineddine <shaddyz@users.sourceforge.net>
#  Copyright (C) 2005 Marcus Lunzenauer <mlunzena@uos.de>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gedit
import gtk

class LineToolsPlugin(gedit.Plugin):

  line_tools_str = """
    <ui>
      <menubar name="MenuBar">
        <menu name="EditMenu" action="Edit">
          <placeholder name="EditOps_6">
            <menu action="LineTools">
              <menuitem action="TrimLine"/>
              <menuitem action="ClearLine"/>
              <menuitem action="DeleteLine"/>
              <menuitem action="DeleteLine2"/>
              <menuitem action="DuplicateLine"/>
              <menuitem action="RaiseLine"/>
              <menuitem action="LowerLine"/>
              <menuitem action="CopyLine"/>
              <menuitem action="CutLine"/>
              <menuitem action="PasteLine"/>
              <menuitem action="ReplaceLine"/>
            </menu>
          </placeholder>
        </menu>
        <menu name="SearchMenu" action="Search">
          <placeholder name="SearchOps_6">
            <menu action="SetBookmark">
              <menuitem action="SetBookmark1"/>
              <menuitem action="SetBookmark2"/>
              <menuitem action="SetBookmark3"/>
              <menuitem action="SetBookmark4"/>
              <menuitem action="SetBookmark5"/>
              <menuitem action="SetBookmark6"/>
              <menuitem action="SetBookmark7"/>
              <menuitem action="SetBookmark8"/>
              <menuitem action="SetBookmark9"/>
              <menuitem action="SetBookmark0"/>
            </menu>
            <menu action="RecallBookmark">
              <menuitem action="RecallBookmark1"/>
              <menuitem action="RecallBookmark2"/>
              <menuitem action="RecallBookmark3"/>
              <menuitem action="RecallBookmark4"/>
              <menuitem action="RecallBookmark5"/>
              <menuitem action="RecallBookmark6"/>
              <menuitem action="RecallBookmark7"/>
              <menuitem action="RecallBookmark8"/>
              <menuitem action="RecallBookmark9"/>
              <menuitem action="RecallBookmark0"/>
            </menu>
          </placeholder>
        </menu>
      </menubar>
    </ui>
    """
  bookmarks = {}
  
  def __init__(self):
    gedit.Plugin.__init__(self)
    
  def activate(self, window):
    actions = [
      ('LineTools',           None, 'Line Tools'),
      ('TrimLine',            None, 'Trim Line',        '<Control>t',        'Remove characters between the cursor and the line end',                     self.trim_line),
      ('ClearLine',           None, 'Clear Line',       '<Control>b',        'Remove all the characters on the current line',                             self.clear_line),
      ('DeleteLine',          None, 'Kill Line Alt.',   '',                  'Completely remove the current line and resets cursor offset',               self.delete_line),
      ('DeleteLine2',         None, 'Kill Line',        '<Shift><Control>d', 'Completely remove the current line and retains cursor offset',              self.delete_line2),
      ('DuplicateLine',       None, 'Duplicate Line',   '<Control>d',        'Create a duplicate of the current line below the current line',             self.duplicate_line),
      ('RaiseLine',           None, 'Raise Line',       '<Control>m',        'Transpose the current line with the line above it',                         self.raise_line),
      ('LowerLine',           None, 'Lower Line',       '<Shift><Control>m', 'Transpose the current line with the line below it',                         self.lower_line),
      ('CopyLine',            None, 'Copy Line',        '<Shift><Control>c', 'Copy the contents of the current line to the clipboard',                    self.copy_line),
      ('CutLine',             None, 'Cut Line',         '<Shift><Control>x', 'Copy the contents of the current line to the clipboard and then remove it', self.cut_line),
      ('PasteLine',           None, 'Paste Line',       '<Shift><Control>v', 'Paste the contents of the clipboard to the current line',                   self.paste_line),
      ('ReplaceLine',         None, 'Replace Line',     '',                  'Paste the contents of the clipboard replacing the current line',            self.replace_line),
      ('SetBookmark',         None, 'Set Bookmark'),
      ('SetBookmark1',        None, 'Set Bookmark 1',   '<Control>!',        'Set a bookmark at the current line',                                       self.set_bookmark_1),
      ('SetBookmark2',        None, 'Set Bookmark 2',   '<Control>@',        'Set a bookmark at the current line',                                       self.set_bookmark_2),
      ('SetBookmark3',        None, 'Set Bookmark 3',   '<Control>#',        'Set a bookmark at the current line',                                       self.set_bookmark_3),
      ('SetBookmark4',        None, 'Set Bookmark 4',   '<Control>$',        'Set a bookmark at the current line',                                       self.set_bookmark_4),
      ('SetBookmark5',        None, 'Set Bookmark 5',   '<Control>%',        'Set a bookmark at the current line',                                       self.set_bookmark_5),
      ('SetBookmark6',        None, 'Set Bookmark 6',   '<Control>^',        'Set a bookmark at the current line',                                       self.set_bookmark_6),
      ('SetBookmark7',        None, 'Set Bookmark 7',   '<Control>&',        'Set a bookmark at the current line',                                       self.set_bookmark_7),
      ('SetBookmark8',        None, 'Set Bookmark 8',   '<Control>*',        'Set a bookmark at the current line',                                       self.set_bookmark_8),
      ('SetBookmark9',        None, 'Set Bookmark 9',   '<Control>(',        'Set a bookmark at the current line',                                       self.set_bookmark_9),
      ('SetBookmark0',        None, 'Set Bookmark 0',   '<Control>)',        'Set a bookmark at the current line',                                       self.set_bookmark_0),
      ('RecallBookmark',      None, 'Go to Bookmark'),
      ('RecallBookmark1',     None, 'Go to Bookmark 1', '<Control>1',        'Go to this bookmark',                                                       self.recall_bookmark_1),
      ('RecallBookmark2',     None, 'Go to Bookmark 2', '<Control>2',        'Go to this bookmark',                                                       self.recall_bookmark_2),
      ('RecallBookmark3',     None, 'Go to Bookmark 3', '<Control>3',        'Go to this bookmark',                                                       self.recall_bookmark_3),
      ('RecallBookmark4',     None, 'Go to Bookmark 4', '<Control>4',        'Go to this bookmark',                                                       self.recall_bookmark_4),
      ('RecallBookmark5',     None, 'Go to Bookmark 5', '<Control>5',        'Go to this bookmark',                                                       self.recall_bookmark_5),
      ('RecallBookmark6',     None, 'Go to Bookmark 6', '<Control>6',        'Go to this bookmark',                                                       self.recall_bookmark_6),
      ('RecallBookmark7',     None, 'Go to Bookmark 7', '<Control>7',        'Go to this bookmark',                                                       self.recall_bookmark_7),
      ('RecallBookmark8',     None, 'Go to Bookmark 8', '<Control>8',        'Go to this bookmark',                                                       self.recall_bookmark_8),
      ('RecallBookmark9',     None, 'Go to Bookmark 9', '<Control>9',        'Go to this bookmark',                                                       self.recall_bookmark_9),
      ('RecallBookmark0',     None, 'Go to Bookmark 0', '<Control>0',        'Go to this bookmark',                                                       self.recall_bookmark_0)
    ]
    windowdata = dict()
    window.set_data("LineToolsPluginWindowDataKey", windowdata)
    windowdata["action_group"] = gtk.ActionGroup("GeditLineToolsPluginActions")
    windowdata["action_group"].add_actions(actions, window)
    manager = window.get_ui_manager()
    manager.insert_action_group(windowdata["action_group"], -1)
    windowdata["ui_id"] = manager.add_ui_from_string(self.line_tools_str)
    window.set_data("LineToolsPluginInfo", windowdata)
    
  def deactivate(self, window):
    windowdata = window.get_data("LineToolsPluginWindowDataKey")
    manager = window.get_ui_manager()
    manager.remove_ui(windowdata["ui_id"])
    manager.remove_action_group(windowdata["action_group"])

  def update_ui(self, window):
    view = window.get_active_view()
    windowdata = window.get_data("LineToolsPluginWindowDataKey")
    windowdata["action_group"].set_sensitive(bool(view and view.get_editable()))
    
  def trim_line(self, action, window):
    doc = window.get_active_document()
    doc.begin_user_action()
    itstart = doc.get_iter_at_mark(doc.get_insert())
    is_end = itstart.ends_line()
    if is_end == False:
      itend = doc.get_iter_at_mark(doc.get_insert())
      itend.forward_to_line_end()
      doc.delete(itstart, itend)
    doc.end_user_action()
    
  def clear_line(self, action, window):
    doc = window.get_active_document()
    doc.begin_user_action()
    itstart = doc.get_iter_at_mark(doc.get_insert())
    itstart.set_line_offset(0);
    is_end = itstart.ends_line()
    if is_end == False:
      itend = doc.get_iter_at_mark(doc.get_insert())
      is_end = itend.ends_line()
      if is_end == False:
        itend.forward_to_line_end()
      doc.delete(itstart, itend)
    doc.end_user_action()
    
  def delete_line(self, action, window):
    doc = window.get_active_document()
    doc.begin_user_action()
    itstart = doc.get_iter_at_mark(doc.get_insert())
    itstart.set_line_offset(0)
    itend = doc.get_iter_at_mark(doc.get_insert())
    itend.forward_line()
    doc.delete(itstart, itend)
    doc.end_user_action()
    
  def delete_line2(self, action, window):
    doc = window.get_active_document()
    doc.begin_user_action()
    itstart = doc.get_iter_at_mark(doc.get_insert())
    offset = itstart.get_line_offset()
    itstart.set_line_offset(0)
    itend = doc.get_iter_at_mark(doc.get_insert())
    itend.forward_line()
    doc.delete(itstart, itend)
    itstart.set_line_offset(offset)
    doc.end_user_action()
    doc.place_cursor(itstart)
    
  def duplicate_line(self, action, window):
    doc = window.get_active_document()
    doc.begin_user_action()
    itstart = doc.get_iter_at_mark(doc.get_insert())
    itstart.set_line_offset(0);
    itend = doc.get_iter_at_mark(doc.get_insert())
    itend.forward_line()
    line = doc.get_slice(itstart, itend, True)
    doc.insert(itend, line)
    doc.end_user_action()
    
  def raise_line(self, action, window):
    doc = window.get_active_document()
    doc.begin_user_action()
    itstart = doc.get_iter_at_mark(doc.get_insert())
    itstart.set_line_offset(0);
    itstart.backward_line()
    itend = doc.get_iter_at_mark(doc.get_insert())
    itend.set_line_offset(0);
    line = doc.get_slice(itstart, itend, True)
    doc.delete(itstart, itend)
    itend.forward_line()
    doc.insert(itend, line)
    doc.end_user_action()
    
  def lower_line(self, action, window):
    doc = window.get_active_document()
    doc.begin_user_action()
    itstart = doc.get_iter_at_mark(doc.get_insert())
    itstart.forward_line()
    itend = doc.get_iter_at_mark(doc.get_insert())
    itend.forward_line()
    itend.forward_line()
    line = doc.get_slice(itstart, itend, True)
    doc.delete(itstart, itend)
    itstart.backward_line()
    doc.insert(itstart, line)
    doc.end_user_action()
    
  def copy_line(self, action, window):
    view = window.get_active_view()
    doc  = window.get_active_document()
    itstart = doc.get_iter_at_mark(doc.get_insert())
    offset = itstart.get_line_offset()
    itstart.set_line_offset(0)
    itend = doc.get_iter_at_mark(doc.get_insert())
    itend.forward_line()
    doc.begin_user_action()
    doc.select_range(itstart, itend)
    doc.copy_clipboard(view.get_clipboard(gtk.gdk.SELECTION_CLIPBOARD))
    itstart.set_line_offset(offset)
    doc.end_user_action()
    doc.place_cursor(itstart)
    
  def cut_line(self, action, window):
    view = window.get_active_view()
    doc  = window.get_active_document()
    itstart = doc.get_iter_at_mark(doc.get_insert())
    offset = itstart.get_line_offset()
    itstart.set_line_offset(0)
    itend = doc.get_iter_at_mark(doc.get_insert())
    itend.forward_line()
    doc.begin_user_action()
    doc.select_range(itstart, itend)
    doc.cut_clipboard(view.get_clipboard(gtk.gdk.SELECTION_CLIPBOARD), True)
    itstart = doc.get_iter_at_mark(doc.get_insert())
    itstart.set_line_offset(offset)
    doc.end_user_action()
    doc.place_cursor(itstart)
    
  def paste_line(self, action, window):
    view = window.get_active_view()
    doc = window.get_active_document()
    itstart = doc.get_iter_at_mark(doc.get_insert())
    offset = itstart.get_line_offset()
    itstart.set_line_offset(0)
    doc.begin_user_action()
    doc.paste_clipboard(view.get_clipboard(gtk.gdk.SELECTION_CLIPBOARD), itstart, True)
    doc.end_user_action()
    itstart = doc.get_iter_at_mark(doc.get_insert())
    itstart.backward_line()
    itstart.set_line_offset(offset)
    doc.place_cursor(itstart)
  
  def replace_line(self, action, window):
    view = window.get_active_view()
    doc = window.get_active_document()
    itstart = doc.get_iter_at_mark(doc.get_insert())
    offset = itstart.get_line_offset()
    itstart.set_line_offset(0)
    itend = doc.get_iter_at_mark(doc.get_insert())
    itend.forward_line()
    doc.begin_user_action()
    doc.delete(itstart, itend)
    doc.paste_clipboard(view.get_clipboard(gtk.gdk.SELECTION_CLIPBOARD), itstart, True)
    doc.end_user_action()
    itstart = doc.get_iter_at_mark(doc.get_insert())
    itstart.backward_line()
    itstart.set_line_offset(offset)
    doc.place_cursor(itstart)
  
  def set_bookmark(self, action, window, position):
    doc  = window.get_active_document()
    iterold = doc.get_iter_at_mark(doc.get_insert())
    try:
        markold = doc.get_mark(self.bookmarks[position])
        doc.move_mark(markold, iterold)
    except KeyError:
        self.bookmarks[position] = 'LineToolsBookmark' + `position`
        doc.create_mark(self.bookmarks[position], iterold, True)
  
  def recall_bookmark(self, action, window, position):
    try:
      doc  = window.get_active_document()
      markold = doc.get_mark(self.bookmarks[position])
      iterold = doc.get_iter_at_mark(markold)
      view = window.get_active_view()
      view.scroll_to_iter(iterold, 0, True)
      doc.place_cursor(iterold)
    except KeyError:
      return
  
  def set_bookmark_1(self, action, window):
    self.set_bookmark(action, window, 1)
  
  def set_bookmark_2(self, action, window):
    self.set_bookmark(action, window, 2)
  
  def set_bookmark_3(self, action, window):
    self.set_bookmark(action, window, 3)
  
  def set_bookmark_4(self, action, window):
    self.set_bookmark(action, window, 4)
  
  def set_bookmark_5(self, action, window):
    self.set_bookmark(action, window, 5)
  
  def set_bookmark_6(self, action, window):
    self.set_bookmark(action, window, 6)
  
  def set_bookmark_7(self, action, window):
    self.set_bookmark(action, window, 7)
  
  def set_bookmark_8(self, action, window):
    self.set_bookmark(action, window, 8)
  
  def set_bookmark_9(self, action, window):
    self.set_bookmark(action, window, 9)
  
  def set_bookmark_0(self, action, window):
    self.set_bookmark(action, window, 0)
  
  def recall_bookmark_1(self, action, window):
    self.recall_bookmark(action, window, 1)
  
  def recall_bookmark_2(self, action, window):
    self.recall_bookmark(action, window, 2)
  
  def recall_bookmark_3(self, action, window):
    self.recall_bookmark(action, window, 3)
  
  def recall_bookmark_4(self, action, window):
    self.recall_bookmark(action, window, 4)
  
  def recall_bookmark_5(self, action, window):
    self.recall_bookmark(action, window, 5)
  
  def recall_bookmark_6(self, action, window):
    self.recall_bookmark(action, window, 6)
  
  def recall_bookmark_7(self, action, window):
    self.recall_bookmark(action, window, 7)
  
  def recall_bookmark_8(self, action, window):
    self.recall_bookmark(action, window, 8)
  
  def recall_bookmark_9(self, action, window):
    self.recall_bookmark(action, window, 9)
  
  def recall_bookmark_0(self, action, window):
    self.recall_bookmark(action, window, 0)
