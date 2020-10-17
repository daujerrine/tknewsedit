"""
    tknewsedit: Tk Application for editing news

    Copyright (c) 2020 Anamitra Ghorui
    This file is part of tknewsedit

    tknewsedit is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    tknewsedit is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with tknewsedit.  If not, see <https://www.gnu.org/licenses/>.
"""

import datetime
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Generic record structure used for unifying data.
# Any record structure used in the database driver must have the elements
# listed over here.

class DatabaseRecord:
    def __init__(self, _id, title, date, content):
        self.id      = _id
        self.title   = title
        self.date    = date
        self.content = content

# Abstract class meant for implementing a database interface or driver for the
# feed editor system. 

class FeedDatabase:
    database_name = ""
    database_driver_version = ""

    def __init__(self):
        pass
    
    def fetch_all(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def add(self, record):
        pass

    def delete(self, record):
        pass

    def close(self):
        pass

class FeedEditorWindow:
    window_title = "Feed Editor"
    post_columns      = ('id', 'title', 'date', 'content')
    default_geometry  = '500x400+120+50'

    help_text = \
    """
Feed Editor
===========

This application is meant to edit RSS, ATOM and JSON feeds as well as update
feeds within an SQL database.

To edit an existing feed entry:
    -- Double click on that entry, or
    -- select the entry and click edit.

To create a new entry:
    -- Click on the new entry button.

To delete one or more entries:
    -- Select a range of entries, then click the delete button.

To commit changes to a file or a database:
    -- Click the commit changes button, or,
    -- click File on the menubar, and click Commit Session.

To Quit:
    -- Press the 'x' button, usually on the top of the main window, or
    -- click File on the menubar, and then click Quit.
"""

    class EditWindow:
        window_title = "Edit Post"

        def __init__(self, rootptr, existing_post = None):
            self.rootptr = rootptr
            self.window = Toplevel(self.rootptr.root)
            self.window.title(self.window_title + " - " + FeedEditorWindow.window_title)
            self.window.option_add('*tearOff', FALSE)
            self.edit_frame      = ttk.Frame(self.window, padding = '3 3 3 3')
            self.edit_frame_text = ttk.Frame(self.window, padding = '3 0 3 3')
            self.submit_frame    = ttk.Frame(self.window, padding = '3 0 3 3')

            ### Edit Frame

            self.title_label  = Label(self.edit_frame, text = "Post Title :")
            self.title_input  = Entry(self.edit_frame)
            self.date_label   = Label(self.edit_frame, text = "Post Date :")
            self.date_input   = Entry(self.edit_frame)
            self.date_today_active = IntVar();
            self.date_today   = Checkbutton(self.edit_frame, text = "Today", \
                                            variable = self.date_today_active,
                                            onvalue = 1, offvalue = 0,
                                            command = self.set_auto_date);
            self.content_label = Label(self.edit_frame, text = "Content :")

            self.title_label.grid(column = 0, row = 0, sticky = 'w');
            self.title_input.grid(column = 1, row = 0, sticky = 'ew', columnspan = 2);
            self.date_label.grid(column = 0, row = 1, sticky = 'w');
            self.date_input.grid(column = 1, row = 1, sticky = 'ew');
            self.date_today.grid(column = 2, row = 1, sticky = 'ew');
            self.content_label.grid(column = 0, row = 2, sticky = 'w');
            self.edit_frame.grid_columnconfigure(1, weight = 1)

            ### Edit Text Frame
            self.content_input = Text(self.edit_frame_text, width = 50, height = 10);
            self.editor_vscroll = ttk.Scrollbar(self.edit_frame_text,
                                                orient = 'vertical',
                                                command = self.content_input.yview)
            self.editor_hscroll = ttk.Scrollbar(self.edit_frame_text,
                                                orient = 'horizontal',
                                                command = self.content_input.xview)
            self.content_input.configure(yscrollcommand = self.editor_vscroll.set,
                                         xscrollcommand = self.editor_hscroll.set)
            self.content_input.grid(column = 0, row = 0, sticky = 'nsew')
            self.editor_vscroll.grid(column = 1, row = 0, sticky = 'ns')
            self.editor_hscroll.grid(column = 0, row = 1, sticky = 'ew')

            self.edit_frame_text.grid_columnconfigure(0, weight = 1)
            self.edit_frame_text.grid_rowconfigure(0, weight = 1)

            ### Submit Frame

            self.save_button   = Button(self.submit_frame, text = "Save",
                                        command = self.edit_entry_submit_close)
            self.cancel_button = Button(self.submit_frame, text = "Cancel",
                                        command = self.window.destroy)

            self.save_button.grid(column = 0, row = 0, sticky = 'e')
            self.cancel_button.grid(column = 1, row = 0, sticky = 'e')
            self.submit_frame.grid_columnconfigure(0, weight = 1)

            ### Pack Up

            self.edit_frame.pack(fill = 'both')
            self.edit_frame_text.pack(expand = 1, fill = 'both')
            self.submit_frame.pack(fill = 'x', side = 'right')

        def set_auto_date(self):
            if self.date_today_active.get():
                self.date_input.delete(0, 'end')
                self.date_input.insert(0, str(datetime.datetime.utcnow()));
                self.date_input.configure(state = 'readonly');
            else:
                self.date_input.configure(state = 'normal');

        def edit_entry_submit_close(self):
            try:
                new_post = Post(title   = self.title_input.get(),
                                date    = datetime.date(*map(int, self.date_input.get().split('-'))),
                                content = self.content_input.get('1.0', 'end'))
                db.session.add(new_post)
                self.rootptr.update_posts()
                self.rootptr.set_content_modified(True);
                self.window.destroy()
            except Exception as e:
                messagebox.showerror(title = "Error", \
                                     message = str(e));

    class HelpWindow:
        window_title = "Help"

        def __init__(self, rootptr):
            self.rootptr = rootptr
            self.rootptr = rootptr
            self.window = Toplevel(self.rootptr.root)
            self.window.title(self.window_title + " - " + FeedEditorWindow.window_title)
            self.window.option_add('*tearOff', FALSE)
            self.frame = ttk.Frame(self.window, padding = '3 3 3 3')
            self.help_message = Text(self.frame, font=("Serif", 10
            ))
            self.help_message.insert('1.0', FeedEditorWindow.help_text)
            self.help_message.configure(state = 'disabled')
            self.vscroll = ttk.Scrollbar(self.frame,
                                         orient = 'vertical',
                                         command = self.help_message.yview)
            self.hscroll = ttk.Scrollbar(self.frame,
                                         orient = 'horizontal',
                                         command = self.help_message.xview)
            self.help_message.configure(yscrollcommand = self.vscroll.set,
                                        xscrollcommand = self.hscroll.set)
            self.help_message.grid(column = 0, row = 0, sticky = 'nsew')
            self.vscroll.grid(column = 1, row = 0, sticky = 'ns')
            self.hscroll.grid(column = 0, row = 1, sticky = 'ew')

            self.frame.grid_columnconfigure(0, weight = 1)
            self.frame.grid_rowconfigure(0, weight = 1)
            self.frame.pack(expand = 1, fill = 'both');
            
    def __init__(self, db):
        self.content_changed = False
        self.db = db

        self.root = Tk()
        self.root.title(self.window_title)
        self.root.option_add('*tearOff', FALSE)
        self.root.geometry(self.default_geometry)

        self.main_frame   = ttk.Frame(self.root, padding = '3 3 3 12')
        self.top_frame    = ttk.Frame(self.main_frame, padding = '0 0 0 12')
        self.bottom_frame = ttk.Frame(self.main_frame)

        ### Top Frame

        self.menubar      = Menu(self.root)
        self.root['menu'] = self.menubar
        self.file_menu    = Menu(self.menubar)
        self.menubar.add_cascade(menu = self.file_menu, label = 'File')
        self.file_menu.add_command(label = "Commit Session", command = self.commit_session)
        self.file_menu.add_command(label = "Help", command = self.show_help)
        self.file_menu.add_command(label = "Close", command = self.root.destroy)

        self.edit_button = ttk.Button(self.top_frame,
                                      text = "Edit Entry",
                                      state = 'disabled')
        self.new_button = ttk.Button(self.top_frame,
                                     text = "New Entry",
                                     command = self.new_entry)
        self.commit_button = ttk.Button(self.top_frame,
                                        text = "Commit Changes",
                                        state = 'disabled',
                                        command = self.commit_session)
        self.revert_button = ttk.Button(self.top_frame,
                                        text = "Revert Changes",
                                        state = 'disabled',
                                        command = self.revert_session)
        self.edit_button.grid(row = 0, column = 0, padx = 2, pady = 2)
        self.new_button.grid(row = 0, column = 1, padx = 2, pady = 2)
        self.commit_button.grid(row = 0, column = 2, padx = 2, pady = 2)
        self.revert_button.grid(row = 0, column = 3, padx = 2, pady = 2)

        ### Bottom Frame

        self.table = ttk.Treeview(self.bottom_frame, \
                                  columns = self.post_columns, \
                                  selectmode = 'extended')
        self.table["show"] = "headings"
        self.table.heading('id',      text = "ID")
        self.table.heading('title',   text = "Title")
        self.table.heading('date',    text = "Date")
        self.table.heading('content', text = "Content")

        self.table.bind('<Double-1>', self.edit_entry)
        # tree.tag_bind('', '<<TreeviewSelect>>', callback = treeview_callback(tree))
        self.table_vscroll = ttk.Scrollbar(self.bottom_frame,
                                           orient = 'vertical',
                                           command = self.table.yview)
        self.table_hscroll = ttk.Scrollbar(self.bottom_frame,
                                           orient = 'horizontal',
                                           command = self.table.xview)
        self.table.configure(yscrollcommand = self.table_vscroll.set,
                             xscrollcommand = self.table_hscroll.set)
        self.table.grid(column = 0, row = 0, sticky = 'nsew')
        self.table_vscroll.grid(column = 1, row = 0, sticky = 'ns')
        self.table_hscroll.grid(column = 0, row = 1, sticky = 'ew')

        self.bottom_frame.grid_columnconfigure(0, weight = 1)
        self.bottom_frame.grid_rowconfigure(0, weight = 1)    

        ### Pack Up

        self.top_frame.pack(fill = 'x')
        self.bottom_frame.pack(expand = True, fill = 'both')
        self.main_frame.pack(expand = True, fill = 'both')
        self.update_posts()
        
        self.root.mainloop()

    def update_posts(self):
        iid = 0;
        self.table.delete(*self.table.get_children())
        for post in self.db.fetch_all():
            t = (str(post.id), post.title, post.date, post.content)
            self.table.insert("", iid, iid, values = t)
            iid += 1

    def commit_session(self):
        self.db.commit()
        self.set_content_modified(False);

    def revert_session(self):
        if messagebox.askyesno(title = "Warning", \
                               message = "Are you sure you want to revert all changes made?"):
            self.db.rollback()
            self.update_posts()
            self.set_content_modified(False);

    def set_content_modified(self, value):
        if value == True:
            self.commit_button.configure(state = 'enabled')
            self.revert_button.configure(state = 'enabled')
        elif value == False:
            self.commit_button.configure(state = 'disabled')
            self.revert_button.configure(state = 'disabled')

    def edit_entry(self, event):
        ## Get Selection from event
        self.edit_window = self.EditWindow(self)

    def new_entry(self):
        self.edit_window = self.EditWindow(self)

    def show_help(self):
        self.help_window = self.HelpWindow(self)

    def update_table(self, event):
        print(str(event))

if __name__ == '__main__':
    window = FeedEditorWindow(Flask_SQLAlchemyFeedDatabase(db, Post))
