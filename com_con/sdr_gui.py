#!/usr/bin/env python

import wx
import time
import threading

class colored_text_box(wx.Panel):
    def __init__(self, parent, text):
        wx.Panel.__init__(self, parent, -1)

        self.SetBackgroundColour(wx.Colour(red=0x00,green=0x00,blue=0xff))

        self.text_label = wx.StaticText(self, -1, text, style=wx.ALIGN_CENTER)
        
        text_font = self.text_label.GetFont()
        text_font.SetPointSize(16)
        text_font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.text_label.SetFont(text_font)

        self.box = wx.GridSizer(1,1,0,0)
        
        self.box.Add(self.text_label, 0, wx.ALIGN_CENTER|wx.ALL, 2)

        self.SetSizer(self.box)

    def set_text(self, text):
        self.text_label.SetLabel(str(text))
        self.box.Layout()

    def set_used(self):
        self.SetBackgroundColour(wx.Colour(red=0xff, green=0x00, blue=0x00))

    def set_free(self):
        self.SetBackgroundColour(wx.Colour(red=0x00, green=0xff, blue=0x00))

class al_dialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, "For Al")
        
        panel = wx.Panel(self, -1, style=wx.BORDER_SUNKEN)

        text = "One day the text here will\nbe written using fortan\nand displayed with python.\nJust for you, Al"
        
        text_label = wx.StaticText(panel, -1, text, style = wx.ALIGN_CENTER)
        text_font = text_label.GetFont()
        text_font.SetPointSize(14)
        text_label.SetFont(text_font)

        ok_button = wx.Button(self, -1, "Ok")

        big_box = wx.BoxSizer(wx.VERTICAL)
        display_box = wx.FlexGridSizer(2,2,2,2)

        display_box.Add(wx.Size(0, 0), 0)
        display_box.Add(wx.Size(400, 0), 0)
        display_box.Add(wx.Size(0,190),0)
        display_box.Add(text_label, 0, wx.ALIGN_CENTER, 0)
        
        panel.SetSizer(display_box)

        big_box.Add(panel, 0, wx.EXPAND, 0)
        big_box.Add(wx.Size(0,15), 0)
        big_box.Add(ok_button, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        
        self.Bind(wx.EVT_BUTTON, self.ok, id=ok_button.GetId())

        self.SetSizer(big_box)
        
        self.ShowModal()
        self.Destroy()

    def ok(self, event):
        self.Close()

class demo_dialog(wx.Dialog):
    def __init__(self, parent, event_handler):
        wx.Dialog.__init__(self, parent, -1, 'Demo Guide')
        
        self.event_handler = event_handler

        display_panel = wx.Panel(self, -1, style=wx.BORDER_SUNKEN)
        
        self.text = ['Welcome to the Demo\nClick Next to move on',
                     'This is the tour through the GUI.\nThis GUI is serves as an interface\nto a time base controller. The\nController handles all the\nnecessary coordination functions\nof the system with time threads.',
                     'This is the View Spectrum Panel.\nThis panel allows an operator to\nkeep an eye on the results\nof the DSA engine.',
                     'This is the Graphical Spectrum\nPanel. This panel allows an\noperator to quickly see\nthe spectral usage.',
                     'This is the Manage DSA Panel.\nThis panel allows an operator to\nmake requests for a frequency\nrelease a frequency orto change\nthe currently emphasised skill.',
                     'This is the Add User Panel.\nThis panel allows an operator to\nadd a new team to the system,\nthe id for the team will be\nautomatically generated.',
                     'This is the View Current Users\nPanel. This panel keeps an\noperator up to date on what\nteams are registered, where\nthey are, and what\ntheir skills are.']


        self.position = 0
        self.text_display = wx.StaticText(display_panel, -1, self.text[self.position],style = wx.ALIGN_CENTER)
        text_font = self.text_display.GetFont()
        text_font.SetPointSize(16)
        self.text_display.SetFont(text_font)

        button_panel = wx.Panel(self, -1)

        self.prev_button = wx.Button(button_panel, -1,"<-Previous")
        quit_button = wx.Button(button_panel, -1, "Quit")
        self.next_button = wx.Button(button_panel, -1,"Next->")

        self.prev_button.Disable()

        button_panel.Bind(wx.EVT_BUTTON, self.quit, id=quit_button.GetId())
        button_panel.Bind(wx.EVT_BUTTON, self.button_handler, id=self.prev_button.GetId())
        button_panel.Bind(wx.EVT_BUTTON, self.button_handler, id=self.next_button.GetId())

        big_box = wx.BoxSizer(wx.VERTICAL)
        self.display_box = wx.FlexGridSizer(2,2,2,2)
        button_box = wx.GridSizer(1,3,2,2)

        self.display_box.Add(wx.Size(0, 0), 0)
        self.display_box.Add(wx.Size(400, 0), 0)
        self.display_box.Add(wx.Size(0,190),0)
        self.display_box.Add(self.text_display, 0, wx.ALIGN_CENTER, 0)

        
        display_panel.SetSizer(self.display_box)

        button_box.Add(self.prev_button, 0, wx.EXPAND, 0)
        button_box.Add(quit_button, 0, wx.EXPAND, 0)
        button_box.Add(self.next_button, 0, wx.EXPAND, 0)

        button_panel.SetSizer(button_box)

        big_box.Add(display_panel, 0, wx.EXPAND|wx.ALL, 5)
        big_box.Add(button_panel, 0, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(big_box)

        self.ShowModal()
        self.Destroy()

    def quit(self, event):
        self.Close()

    def button_handler(self, event):
        event_id = event.GetId()
        
        if event_id == self.prev_button.GetId():
            self.position -= 1
        elif event_id == self.next_button.GetId():
            self. position += 1

        if self.position == 0:
            self.prev_button.Enable(False)
            self.next_button.Enable(True)
        elif self.position > 0 and self.position < len(self.text)-1:
            self.prev_button.Enable(True)
            self.next_button.Enable(True)
        elif self.position == len(self.text)-1:
            self.prev_button.Enable(True)
            self.next_button.Enable(False)


        self.text_display.SetLabel(self.text[self.position])

        self.display_box.Layout()

        self.event_handler(self.position - 1)

class gui(wx.Frame):
    def __init__(self, set_new_users, make_freq_requests, release_freq, set_emphasis, get_freq_data, get_user_data, get_geoloc_data):
        wx.Frame.__init__(self, None, -1, 'SDR HQ', size = (700,600),
                          style = wx.DEFAULT_FRAME_STYLE)

        self.panels = {}
        self.ids = {}

        self.users = []
        self.freq_data = []

        self.main_panel_start = True

        self.timer = wx.Timer(self, -1)
        self.timer.Start(1000)

        self.lock = threading.Lock()
        
        #Menus
        ##########################################################################
        menubar = wx.MenuBar()

        file_menu = wx.Menu()
        quit_action = wx.MenuItem(file_menu, -1, '&Quit\tCtrl+Q')
        file_menu.AppendItem(quit_action)

        dsa_menu = wx.Menu()
        spectrum_action = wx.MenuItem(dsa_menu, -1, "View &Spectral Use\tCtrl+S")
        manage_action = wx.MenuItem(dsa_menu, -1, "&Manage Spectrum\tCtrl+M")
        graphic_action = wx.MenuItem(dsa_menu, -1, "&Graphic Spectrum\tCtrl+G")

        dsa_menu.AppendItem(spectrum_action)
        dsa_menu.AppendItem(manage_action)
        dsa_menu.AppendItem(graphic_action)

        user_menu = wx.Menu()
        new_action = wx.MenuItem(user_menu, -1, "&Add New User\tCtrl+A")
        current_action = wx.MenuItem(user_menu, -1, "View Current &Users\tCtrl+U")

        user_menu.AppendItem(new_action)
        user_menu.AppendItem(current_action)

        help_menu = wx.Menu()
        about_action = wx.MenuItem(help_menu, -1, '&About\tCtrl+B')
        demo_action = wx.MenuItem(help_menu, -1, '&Demo\tCtrl+D')
        al_action = wx.MenuItem(help_menu, -1, 'A&l\tCtrl+L')

        help_menu.AppendItem(about_action)
        help_menu.AppendItem(demo_action)
        help_menu.AppendItem(al_action)

        menubar.Append(file_menu, '&File')
        menubar.Append(dsa_menu, '&DSA')
        menubar.Append(user_menu, '&User')
        menubar.Append(help_menu, '&Help')
    
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.quit, id=quit_action.GetId())
        self.Bind(wx.EVT_MENU, self.panel_show, id=spectrum_action.GetId())
        self.Bind(wx.EVT_MENU, self.panel_show, id=manage_action.GetId())
        self.Bind(wx.EVT_MENU, self.panel_show, id=graphic_action.GetId())
        self.Bind(wx.EVT_MENU, self.panel_show, id=new_action.GetId())
        self.Bind(wx.EVT_MENU, self.panel_show, id=current_action.GetId())
        self.Bind(wx.EVT_MENU, self.about_handler, id=about_action.GetId())
        self.Bind(wx.EVT_MENU, self.demo, id=demo_action.GetId())
        self.Bind(wx.EVT_MENU, self.al_handler, id=al_action.GetId())


        #Main Panel
        ##########################################################################
        main_panel = wx.Panel(self, -1)

        main_tag = wx.StaticText(main_panel, -1, 'Welcome to the SDR09 GUI')
        main_tag_font = main_tag.GetFont()
        main_tag_font.SetWeight(wx.FONTWEIGHT_BOLD)
        main_tag_font.SetDefaultEncoding(wx.FONTENCODING_DEFAULT)
        main_tag_font.SetFamily(wx.FONTFAMILY_DECORATIVE)
        main_tag_font.SetPointSize(32)
        main_tag.SetFont(main_tag_font)

        main_subtag = wx.StaticText(main_panel, -1, "What should the subtag say?")
        main_subtag_font = main_subtag.GetFont()
        main_subtag_font.SetDefaultEncoding(wx.FONTENCODING_DEFAULT)
        main_subtag_font.SetFamily(wx.FONTFAMILY_DECORATIVE)
        main_subtag_font.SetPointSize(28)
        main_subtag.SetFont(main_subtag_font)

        main_demo_button = wx.Button(main_panel, -1, "Demo")
        main_demo_button_font = main_demo_button.GetFont()
        main_demo_button_font.SetEncoding(wx.FONTENCODING_DEFAULT)
        main_demo_button_font.SetFamily(wx.FONTFAMILY_DECORATIVE)
        main_demo_button_font.SetPointSize(28)
        main_demo_button.SetFont(main_demo_button_font)
                
        main_box = wx.GridSizer(3,2, 2, 2)
        
        main_box.Add(main_tag, 0, wx.ALIGN_CENTER|wx.ALL, 15)
        main_box.Add(wx.Size(0,200), 0)
        main_box.Add(main_subtag, 0, wx.ALIGN_CENTER|wx.ALL, 15)
        main_box.Add(wx.Size(0,100), 0)
        main_box.Add(main_demo_button, 0, wx.ALIGN_CENTER|wx.ALL, 15)
        main_box.Add(wx.Size(0,100), 0)

        main_panel.SetSizer(main_box)
        
        main_panel.Bind(wx.EVT_BUTTON, self.demo, id=main_demo_button.GetId())
        
        main_panel.Show(self.main_panel_start)

        
        self.panels[-1] = main_panel

        #Spectrum Panel
        ##########################################################################
        spectrum_panel = wx.Panel(self, -1)

        spectrum_tag = wx.StaticText(spectrum_panel, -1, "Spectral Use")
        spectrum_tag_font = spectrum_tag.GetFont()
        spectrum_tag_font.SetPointSize(16)
        spectrum_tag.SetFont(spectrum_tag_font)

        spectrum_box1 = wx.BoxSizer(wx.VERTICAL)
        spectrum_box2 = wx.FlexGridSizer(15,3,2,2)
        
        spectrum_freq_label = wx.StaticText(spectrum_panel, -1, "Center Frequency")
        spectrum_user_label = wx.StaticText(spectrum_panel, -1, "Occuping User")
        spectrum_time_label = wx.StaticText(spectrum_panel, -1, "Timeout Value")

        spectrum_freq_label_font = spectrum_freq_label.GetFont()
        spectrum_freq_label_font.SetPointSize(12)
        spectrum_freq_label.SetFont(spectrum_freq_label_font)

        spectrum_user_label_font = spectrum_user_label.GetFont()
        spectrum_user_label_font.SetPointSize(12)
        spectrum_user_label.SetFont(spectrum_user_label_font)

        spectrum_time_label_font = spectrum_time_label.GetFont()
        spectrum_time_label_font.SetPointSize(12)
        spectrum_time_label.SetFont(spectrum_time_label_font)

        spectrum_box2.Add(spectrum_freq_label, 0, wx.ALIGN_CENTER, 0)
        spectrum_box2.Add(spectrum_user_label, 0, wx.ALIGN_CENTER, 0)
        spectrum_box2.Add(spectrum_time_label, 0, wx.ALIGN_CENTER, 0)

        self.spectrum_ctrl = []
        for i in range(14):
            tmp = {}
            tmp['freq'] = wx.TextCtrl(spectrum_panel, -1, '', style=wx.TE_READONLY|wx.TE_CENTER)
            tmp['user'] = wx.TextCtrl(spectrum_panel, -1, '', style=wx.TE_READONLY|wx.TE_CENTER)
            tmp['time'] = wx.TextCtrl(spectrum_panel, -1, '', style=wx.TE_READONLY|wx.TE_CENTER)
            
            spectrum_box2.Add(tmp['freq'], 0, wx.EXPAND, 0)
            spectrum_box2.Add(tmp['user'], 0, wx.EXPAND, 0)
            spectrum_box2.Add(tmp['time'], 0, wx.EXPAND, 0)

            self.spectrum_ctrl.append(tmp)

        spectrum_space = 225
        spectrum_box2.Add(wx.Size(spectrum_space,0),0)
        spectrum_box2.Add(wx.Size(spectrum_space,0),0)
        spectrum_box2.Add(wx.Size(spectrum_space,0),0)

        spectrum_box1.Add(spectrum_tag, 0, wx.ALL, 0)
        spectrum_box1.Add(wx.Size(0,25), 0)
        spectrum_box1.Add(spectrum_box2, 0, wx.EXPAND|wx.ALL, 7)

        spectrum_panel.SetSizer(spectrum_box1)
        
        spectrum_panel.Show(not(self.main_panel_start))

        self.panels[spectrum_action.GetId()] = spectrum_panel

        #Graphic Panel
        ##########################################################################
        graphic_panel = wx.Panel(self, -1)
        
        graphic_tag = wx.StaticText(graphic_panel, -1, 'Graphical Spectrum View')
        graphic_tag_font = graphic_tag.GetFont()
        graphic_tag_font.SetPointSize(16)
        graphic_tag.SetFont(graphic_tag_font)

        graphic_box2 = wx.FlexGridSizer(5,5,4,4)
        graphic_vert_space = 100
        graphic_hori_space = 169

        self.graphic_ctrl = []
        j = 0
        for i in range(15):
            if j < 4:
                tmp = colored_text_box(graphic_panel,'')
                graphic_box2.Add(tmp, 0, wx.EXPAND|wx.ALIGN_CENTER, 0)
                self.graphic_ctrl.append(tmp)
                j += 1
            else:
                j = 0
                graphic_box2.Add(wx.Size(0,graphic_vert_space), 0)


        graphic_box2.Add(wx.Size(0,0), 0)

        tmp = colored_text_box(graphic_panel, '')
        graphic_box2.Add(tmp, 0, wx.EXPAND|wx.ALIGN_CENTER, 0)
        self.graphic_ctrl.append(tmp)
        
        tmp = colored_text_box(graphic_panel, '')
        graphic_box2.Add(tmp, 0, wx.EXPAND|wx.ALIGN_CENTER, 0)
        self.graphic_ctrl.append(tmp)

        graphic_box2.Add(wx.Size(0,graphic_vert_space), 0)
        graphic_box2.Add(wx.Size(0, 0), 0)
                
        graphic_box2.Add(wx.Size(graphic_hori_space, 0), 0)
        graphic_box2.Add(wx.Size(graphic_hori_space, 0), 0)                
        graphic_box2.Add(wx.Size(graphic_hori_space, 0), 0)
        graphic_box2.Add(wx.Size(graphic_hori_space, 0), 0)
        graphic_box2.Add(wx.Size(0, 0), 0)

        graphic_box1 = wx.BoxSizer(wx.VERTICAL)

        graphic_box1.Add(graphic_tag, 0, wx.ALL, 5)
        graphic_box1.Add(wx.Size(0, 25), 0)
        graphic_box1.Add(graphic_box2, 0, wx.EXPAND|wx.ALL, 5)

        graphic_panel.SetSizer(graphic_box1)
        
        graphic_panel.Show(False)

        self.panels[graphic_action.GetId()] = graphic_panel

        #Manage Panel
        ##########################################################################
        manage_panel = wx.Panel(self, -1)

        manage_request_tag = wx.StaticText(manage_panel, -1, "Request Frequency")
        manage_request_label = wx.StaticText(manage_panel, -1, "Enter Id of Requesting Team:")
        self.manage_request_ctrl = wx.TextCtrl(manage_panel, -1, '', style=wx.TE_PROCESS_ENTER)
        manage_request_button = wx.Button(manage_panel, -1, "Submit Request")

        manage_release_tag = wx.StaticText(manage_panel, -1, "Release Frequency")
        manage_release_label = wx.StaticText(manage_panel, -1, "Enter Frequency to Release:")
        self.manage_release_ctrl = wx.TextCtrl(manage_panel, -1, '', style=wx.TE_PROCESS_ENTER)
        manage_release_button = wx.Button(manage_panel, -1, "Submit Release")

        manage_emphasis_tag = wx.StaticText(manage_panel, -1, "Set Skill Emphasis")
        manage_emphasis_label = wx.StaticText(manage_panel, -1, "Enter Emphasis:")
        self.manage_emphasis_ctrl = wx.TextCtrl(manage_panel, -1, '', style=wx.TE_PROCESS_ENTER)
        manage_emphasis_button = wx.Button(manage_panel, -1, "Set Emphasis")

        manage_tag_font = manage_request_tag.GetFont()
        manage_tag_font.SetPointSize(16)
        manage_tag_font.SetUnderlined(True)

        manage_request_tag.SetFont(manage_tag_font)
        manage_release_tag.SetFont(manage_tag_font)
        manage_emphasis_tag.SetFont(manage_tag_font)

        manage_label_font = manage_request_label.GetFont()
        manage_label_font.SetPointSize(12)

        manage_request_label.SetFont(manage_label_font)
        manage_release_label.SetFont(manage_label_font)
        manage_emphasis_label.SetFont(manage_label_font)
        
        manage_front_space = 5

        manage_box = wx.FlexGridSizer(10, 5, 4, 4)
        
        manage_box.Add(wx.Size(0,50), 0)
        manage_box.Add(wx.Size(225,0), 0)
        manage_box.Add(wx.Size(250,0), 0)
        manage_box.Add(wx.Size(200,0), 0)
        manage_box.Add(wx.Size(0,0), 0)

        manage_box.Add(wx.Size(manage_front_space,0), 0)
        manage_box.Add(manage_request_tag, 0, wx.ALL, 0)
        manage_box.Add(wx.Size(0,0), 0)
        manage_box.Add(wx.Size(0,0), 0)
        manage_box.Add(wx.Size(0,0), 0)

        manage_box.Add(wx.Size(manage_front_space,0), 20)
        manage_box.Add(manage_request_label, 0, wx.ALIGN_CENTER, 0)
        manage_box.Add(self.manage_request_ctrl, 0, wx.EXPAND, 0)
        manage_box.Add(manage_request_button, 0, wx.EXPAND|wx.ALL, 2)
        manage_box.Add(wx.Size(0,0), 0)

        manage_box.Add(wx.Size(0,75), 0)
        manage_box.Add(wx.Size(0,0), 0)
        manage_box.Add(wx.Size(0,0), 0)
        manage_box.Add(wx.Size(0,0), 0)
        manage_box.Add(wx.Size(0,0), 0)

        manage_box.Add(wx.Size(manage_front_space,0), 0)
        manage_box.Add(manage_release_tag, 0, wx.ALL, 0)
        manage_box.Add(wx.Size(0,0), 0)
        manage_box.Add(wx.Size(0,0), 0)
        manage_box.Add(wx.Size(0,0), 0)

        manage_box.Add(wx.Size(manage_front_space,0), 20)
        manage_box.Add(manage_release_label, 0, wx.ALIGN_CENTER, 0)
        manage_box.Add(self.manage_release_ctrl, 0, wx.EXPAND, 0)
        manage_box.Add(manage_release_button, 0, wx.EXPAND|wx.ALL, 2)
        manage_box.Add(wx.Size(0,0), 0)

        manage_box.Add(wx.Size(0,75), 0)
        manage_box.Add(wx.Size(0,0), 0)
        manage_box.Add(wx.Size(0,0), 0)
        manage_box.Add(wx.Size(0,0), 0)
        manage_box.Add(wx.Size(0,0), 0)

        manage_box.Add(wx.Size(manage_front_space,0), 0)
        manage_box.Add(manage_emphasis_tag, 0, wx.ALL, 0)
        manage_box.Add(wx.Size(0,0), 0)
        manage_box.Add(wx.Size(0,0), 0)
        manage_box.Add(wx.Size(0,0), 0)

        manage_box.Add(wx.Size(manage_front_space,0), 20)
        manage_box.Add(manage_emphasis_label, 0, wx.ALIGN_CENTER, 0)
        manage_box.Add(self.manage_emphasis_ctrl, 1, wx.EXPAND, 0)
        manage_box.Add(manage_emphasis_button, 0, wx.EXPAND|wx.ALL, 2)
        manage_box.Add(wx.Size(0,0), 0)

        manage_box.Add(wx.Size(0,50), 0)
        manage_box.Add(wx.Size(0,0), 0)
        manage_box.Add(wx.Size(0,0), 0)
        manage_box.Add(wx.Size(0,0), 0)
        manage_box.Add(wx.Size(0,0), 0)

        manage_panel.SetSizer(manage_box)

        manage_panel.Bind(wx.EVT_BUTTON, self.request_frequency, id=manage_request_button.GetId())
        manage_panel.Bind(wx.EVT_TEXT_ENTER, self.request_frequency, id=self.manage_request_ctrl.GetId())
        
        manage_panel.Bind(wx.EVT_BUTTON, self.release_frequency, id=manage_release_button.GetId())
        manage_panel.Bind(wx.EVT_TEXT_ENTER, self.release_frequency, id=self.manage_release_ctrl.GetId())

        manage_panel.Bind(wx.EVT_BUTTON, self.set_emphasis, id=manage_emphasis_button.GetId())
        manage_panel.Bind(wx.EVT_TEXT_ENTER, self.set_emphasis, id=self.manage_emphasis_ctrl.GetId())

        manage_panel.Show(False)

        self.panels[manage_action.GetId()] = manage_panel
        
        #New Panel (New User Panel)
        ##########################################################################
        new_panel = wx.Panel(self, -1)
    
        new_tag = wx.StaticText(new_panel, -1, "Add New User")
        
        new_name_label = wx.StaticText(new_panel, -1, "Enter Team Name:")
        self.new_name_ctrl = wx.TextCtrl(new_panel, -1, '', style=wx.TE_PROCESS_ENTER)

        new_skill_label = wx.StaticText(new_panel, -1, "Enter Team Skill:")
        self.new_skill_ctrl = wx.TextCtrl(new_panel, -1, '', style=wx.TE_PROCESS_ENTER)

        new_id_label = wx.StaticText(new_panel, -1, "Team Id:")
        self.new_id_ctrl = wx.TextCtrl(new_panel, -1, '1', style=wx.TE_READONLY)

        self.new_notification_label = wx.StaticText(new_panel, -1, '', style=wx.ALIGN_CENTER)
        new_button = wx.Button(new_panel, -1, "Add User")

        new_tag_font = new_tag.GetFont()
        new_tag_font.SetPointSize(16)
        new_tag.SetFont(new_tag_font)

        label_font = new_name_label.GetFont()
        label_font.SetPointSize(12)

        new_name_label.SetFont(label_font)
        new_skill_label.SetFont(label_font)
        new_id_label.SetFont(label_font)
    
        self.new_notification_label.SetFont(label_font)
        new_button.SetFont(label_font)


        new_box = wx.FlexGridSizer(9, 3, 0, 0)
        
        new_box.Add(new_tag, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        new_box.Add(wx.Size(350,50), 0)
        new_box.Add(wx.Size(0,0), 0)

        new_box.Add(wx.Size(300,75), 0)
        new_box.Add(wx.Size(0,0), 0)
        new_box.Add(wx.Size(0,0), 0)

        new_box.Add(new_name_label, 0, wx.ALIGN_CENTER, 0)
        new_box.Add(self.new_name_ctrl, 0, wx.EXPAND, 0)
        new_box.Add(wx.Size(0,0), 0)

        new_box.Add(wx.Size(0,60), 0)
        new_box.Add(wx.Size(0,0), 0)
        new_box.Add(wx.Size(0,0), 0)

        new_box.Add(new_skill_label, 0, wx.ALIGN_CENTER, 0)
        new_box.Add(self.new_skill_ctrl, 0, wx.EXPAND, 0)
        new_box.Add(wx.Size(0,0), 0)

        new_box.Add(wx.Size(0,60), 0)
        new_box.Add(wx.Size(0,0), 0)
        new_box.Add(wx.Size(0,0), 0)

        new_box.Add(new_id_label, 0, wx.ALIGN_CENTER, 0)
        new_box.Add(self.new_id_ctrl, 0, wx.EXPAND, 0)
        new_box.Add(wx.Size(0,0), 0)

        new_box.Add(wx.Size(0,50), 0)
        new_box.Add(wx.Size(0,0), 0)
        new_box.Add(wx.Size(0,0), 0)

        new_box.Add(self.new_notification_label, 0, wx.ALIGN_CENTER, 0)
        new_box.Add(new_button, 0 , wx.EXPAND|wx.ALL, 80)
        new_box.Add(wx.Size(0,250), 0)        
        
        new_panel.SetSizer(new_box)

        new_panel.Bind(wx.EVT_BUTTON, self.add_user, id=new_button.GetId())
        new_panel.Bind(wx.EVT_TEXT_ENTER, self.add_user, id=self.new_name_ctrl.GetId())
        new_panel.Bind(wx.EVT_TEXT_ENTER, self.add_user, id=self.new_skill_ctrl.GetId())
        new_panel.Bind(wx.EVT_TEXT, self.clear_new_notification, id=self.new_name_ctrl.GetId())
        new_panel.Bind(wx.EVT_TEXT, self.clear_new_notification, id=self.new_skill_ctrl.GetId())

        new_panel.Show(False)
        
        self.panels[new_action.GetId()] = new_panel

        #Current Panel (Current User Panel)
        ##########################################################################
        current_panel = wx.Panel(self, -1)
        
        current_box = wx.FlexGridSizer(22, 5, 1, 1)

        current_name_label = wx.StaticText(current_panel, -1, 'Name')
        current_id_label = wx.StaticText(current_panel, -1, 'Id')
        current_skill_label = wx.StaticText(current_panel, -1, 'Skill')
        current_lat_label = wx.StaticText(current_panel, -1, 'Latitude')
        current_lon_label = wx.StaticText(current_panel, -1, 'Longitude')
        
        label_font = current_name_label.GetFont()
        label_font.SetPointSize(12)
        
        current_name_label.SetFont(label_font)
        current_id_label.SetFont(label_font)
        current_skill_label.SetFont(label_font)
        current_lat_label.SetFont(label_font)
        current_lon_label.SetFont(label_font)

        current_box.Add(current_name_label, 0, wx.ALIGN_CENTER, 0)
        current_box.Add(current_id_label, 0, wx.ALIGN_CENTER, 0)
        current_box.Add(current_skill_label, 0, wx.ALIGN_CENTER, 0)
        current_box.Add(current_lat_label, 0, wx.ALIGN_CENTER, 0)
        current_box.Add(current_lon_label, 0, wx.ALIGN_CENTER, 0)

        self.current_ctrl = []
        for i in range(20):
            tmp ={}
            tmp['name'] = wx.TextCtrl(current_panel, -1, '', style=wx.TE_READONLY|wx.TE_CENTER)
            tmp['id'] = wx.TextCtrl(current_panel, -1, '', style=wx.TE_READONLY|wx.TE_CENTER)
            tmp['skill'] = wx.TextCtrl(current_panel, -1, '', style=wx.TE_READONLY|wx.TE_CENTER)
            tmp['lat'] = wx.TextCtrl(current_panel, -1, '', style=wx.TE_READONLY|wx.TE_CENTER)
            tmp['lon'] = wx.TextCtrl(current_panel, -1, '', style=wx.TE_READONLY|wx.TE_CENTER)

            current_box.Add(tmp['name'], 0, wx.EXPAND, 0)
            current_box.Add(tmp['id'], 0, wx.EXPAND, 0)
            current_box.Add(tmp['skill'], 0, wx.EXPAND, 0)
            current_box.Add(tmp['lat'], 0, wx.EXPAND, 0)
            current_box.Add(tmp['lon'], 0, wx.EXPAND, 0)
            
            self.current_ctrl.append(tmp)
        
        current_space = 139
        current_box.Add(wx.Size(current_space,0), 0)
        current_box.Add(wx.Size(current_space,0), 0)
        current_box.Add(wx.Size(current_space,0), 0)
        current_box.Add(wx.Size(current_space,0), 0)
        current_box.Add(wx.Size(current_space,0), 0)
    
        current_panel.SetSizer(current_box)

        current_panel.Show(False)

        self.panels[current_action.GetId()] = current_panel

        #Main Sizer
        ##########################################################################
        self.main_box = wx.BoxSizer()

        self.main_box.Add(main_panel, 0, wx.EXPAND, 0)
        self.main_box.Add(spectrum_panel, 0, wx.EXPAND, 0)
        self.main_box.Add(manage_panel, 0, wx.EXPAND, 0)
        self.main_box.Add(graphic_panel, 0, wx.EXPAND, 0)
        self.main_box.Add(new_panel, 0, wx.EXPAND, 0)
        self.main_box.Add(current_panel, 0, wx.EXPAND, 0)

        self.SetSizer(self.main_box)

        self.Bind(wx.EVT_TIMER, self.timer_handler, id=self.timer.GetId())

        #Connection to Controller
        ##########################################################################
        self.__set_new_users = set_new_users
        self.__make_freq_request = make_freq_requests
        self.__release_freq = release_freq
        self.__set_emphasis = set_emphasis
        self.__get_freq_data = get_freq_data
        self.__get_user_data = get_user_data
        self.__get_geoloc_data = get_geoloc_data
 

    def quit(self, event):
        self.Close()

    def panel_show(self, event):
        event_id = event.GetId()
        
        panel_keys = self.panels.keys()
        for key in panel_keys:
            if key == event_id:
                self.panels[key].Show(True)
            else:
                self.panels[key].Show(False)

        self.main_box.Layout()

    def demo(self, event):
        demo_dialog(self, self.demo_handler)

    def demo_handler(self, position):
        panel_keys = self.panels.keys()

        index = -1
        if position < 1:
            index = 5
        elif position < 2:
            index = 0
        elif position < 3:
            index = 2
        elif position < 4:
            index = 1
        elif position < 5:
            index = 3
        elif position < 6:
            index = 4

        show_key = panel_keys[index]
        for key in panel_keys:
            if key == show_key:
                self.panels[key].Show(True)
            else:
                self.panels[key].Show(False)

        self.main_box.Layout()

    def about_handler(self, event):
        description="""<Name> is a fancy schmancy system to do stuff that is good. As a matter of fact everyone in the universe loves <Name> and I know cause I was there."""

        licence="""The major language used by <Name> is python and thus <Name> is technically open source.  As far as the  concepts held within are ours, you can have them. We work for a long long time on this stuffs and you can't just come allong and steal our work like that, jerk."""

        info = wx.AboutDialogInfo()

        info.SetName('<Name>')
        info.SetVersion('0.728')
        info.SetDescription(description)
        info.SetCopyright('(C) 2010 CW--Awesome--T')
        info.SetWebSite('www.cwt.awesome')
        info.SetLicence(licence)
        info.AddDeveloper('Alex \'The Vision Keeper\' Young')
        info.AddDeveloper('Hedieh \'The Mathemagician\' Alavi')
        info.AddDeveloper('Nick \'The Also There Guy\' Kaminski')
        info.AddDocWriter('All the same peoples that developed stuffs')
        info.AddArtist('Once again all of us--our system is so beautiful it\'s art')
        
        wx.AboutBox(info)

    def al_handler(self, event):
        al_dialog(self)

    def request_frequency(self, event):
        team_id = self.manage_request_ctrl.GetValue().strip()
        
        if len(team_id) == 0:
            self.manage_request_ctrl.SetValue("Value Needed")
        elif not(self.is_digit(team_id)):
            self.manage_request_ctrl.SetValue("No Characters")
        else:
            team_id = int(team_id)
            skill = None
            loc = None
            self.lock.acquire()
            if self.users:
                for user in self.users:
                    if user['id'] == team_id:
                        skill = user['skill']
                        loc = user['location']
            self.lock.release()
            request = (team_id, skill, loc)
            self.__make_freq_request(team_id)
            self.manage_request_ctrl.SetValue("Request made for Team %d"%team_id)

    def release_frequency(self, event):
        freq = self.manage_release_ctrl.GetValue().strip()

        if len(freq) == 0:
            self.manage_release_ctrl.SetValue("Value Needed")
        elif not(self.is_digit(freq)):
            self.manage_release_ctrl.SetValue("No Characters")
        else:
            freq = float(freq)
            self.__release_freq(freq)
            self.manage_release_ctrl.SetValue("Frequency %.1f Released"%freq)

    def set_emphasis(self, event):
        text = self.manage_emphasis_ctrl.GetValue().strip()

        if len(text) == 0:
            self.manage_emphasis_ctrl.SetValue("Value Needed")
        elif self.is_digit(text):
            self.manage_emphasis_ctrl.SetValue("Only Characters")
        else:
            self.__set_emphasis(str(text))
            self.manage_emphasis_ctrl.SetValue("Emphasis set to %s"%text)

    def timer_handler(self, event):
        self.update_spectrum_panel(event)
        self.update_graphic_panel(event)
        self.update_current_panel(event)

    def update_spectrum_panel(self, event):
        freq_data = self.__get_freq_data()
        
        index = 0
        for item in freq_data:
            self.spectrum_ctrl[index]['freq'].SetValue(str(item[0]))

            if item[1] < 0:
                user_id = item[1] * -1
                self.spectrum_ctrl[index]['user'].SetValue(str(user_id))
            else:
                self.spectrum_ctrl[index]['user'].SetValue('None')


            self.spectrum_ctrl[index]['time'].SetValue(str(item[2]))

            index += 1

        self.freq_data = [k for k in freq_data]
    
    def update_graphic_panel(self, event):
        for i in range(len(self.freq_data)):
            self.graphic_ctrl[i].set_text(self.freq_data[i][0])
            if self.freq_data[i][1] < 0:
                self.graphic_ctrl[i].set_used()
            else:
                self.graphic_ctrl[i].set_free()


    def update_current_panel(self, event):
        users = self.__get_user_data()
        
        self.lock.acquire()
        index = 0
        for user in users:
            self.current_ctrl[index]['name'].SetValue(user['name'])
            self.current_ctrl[index]['id'].SetValue(str(user['id']))
            self.current_ctrl[index]['skill'].SetValue(user['skill'])
            if user['location']:
                self.current_ctrl[index]['lat'].SetValue(str(user['location'][1]))
                self.current_ctrl[index]['lon'].SetValue(str(user['location'][0]))
            else:
                self.current_ctrl[index]['lat'].SetValue('None')
                self.current_ctrl[index]['lon'].SetValue('None')

            index += 1

        self.users = [k for k in users]
        self.lock.release()

    def add_user(self, event):
        name = self.new_name_ctrl.GetValue().strip()
        skill = self.new_skill_ctrl.GetValue().strip()
        team_id = self.new_id_ctrl.GetValue().strip()

        if len(name) == 0:
            self.new_name_ctrl.SetValue("Value Needed")
        elif len(skill) == 0:
            self.new_skill_ctrl.SetValue("Value Needed")
        elif self.is_digit(skill):
            self.new_skill_ctrl.SetValue("Only Character")
        else:
            team_id = int(team_id)
                
            user = {'name':name, 'skill':skill, 'id':team_id, 'location':None, 'freq':None}
            self.lock.acquire()
            self.users.append(user)
            self.lock.release()

            self.__set_new_users(user)
            
            self.new_notification_label.SetLabel("New User Accepted")
            self.new_name_ctrl.SetValue('')
            self.new_skill_ctrl.SetValue('')
            self.new_id_ctrl.SetValue(str(team_id+1))

    def clear_new_notification(self, event):
        name = self.new_name_ctrl.GetValue()
        skill = self.new_skill_ctrl.GetValue()
        
        if not(len(name) and len(skill)):
            if len(name) or len(skill):
                self.new_notification_label.SetLabel('')

    def is_digit(self, str):
        '''
        function to check if a str is a number
        considers 1.0 a number where isdigit() does not
        '''
        list = str.split('.')
        
        if len(list) < 2:
            list.append('0')

        if list[0][0]=='-':
            list[0] = list[0][1:]

        result = list[0].isdigit() and list[1].isdigit()

        if len(list) > 2:
            result = False

        return result    



        

