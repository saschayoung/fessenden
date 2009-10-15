#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Thu Oct  8 16:28:36 2009

import wx, os

# begin wxGlade: extracode
# end wxGlade



class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, None, -1, 'Beacon', size=(1000,700))
        self.bitmap_button_1 = wx.StaticBitmap(self, -1, wx.Bitmap("./ACR-2848-EPIRB.jpg", wx.BITMAP_TYPE_ANY), size=(600,600))
        self.button_1 = wx.Button(self, -1, "Start",size = (300,75))

        self.tag = wx.StaticText(self, -1, "Beacon ID: ")
        self.id_ctrl = wx.TextCtrl(self, -1, "42")

        self.button_1.SetFont(wx.Font(22,wx.DECORATIVE, wx.NORMAL,wx.BOLD))

        self.Bind(wx.EVT_BUTTON, self.change_words, id=self.button_1.GetId())
        self.light = wx.StaticBitmap(self, -1, wx.Bitmap("./led-off_grey.jpg",wx.BITMAP_TYPE_ANY))
        self.light_flag = 'off'

        self.timer = wx.Timer(self, -1)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

        self.timer.Start(100)

        self.button_locked = False
        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def OnTimer(self, event):
        if self.button_locked:
            if self.light_flag == 'off':
                self.light.SetBitmap(wx.Bitmap("./led-on_grey.jpg", wx.BITMAP_TYPE_ANY))
                self.light_flag = 'on'
            elif self.light_flag == 'on':
                self.light.SetBitmap(wx.Bitmap("./led-off_grey.jpg", wx.BITMAP_TYPE_ANY))
                self.light_flag = 'off'


    def change_words(self, event):
        if (self.button_1.GetLabel() == 'Start') and (not(self.button_locked)):
            self.button_1.SetLabel('Don\'t Panic')
            beacon_id = self.id_ctrl.GetValue()
            
            f = open('beacon_id', 'w')
            f.write(beacon_id)
            f.close()

            self.button_locked = True

            os.system('sudo ./beacon_IAB_demo.py -f 450M -r 125k -M 3M --tx-amplitude=0.125 &')

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Beacon")
        self.id_ctrl.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.tag.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
#        self.bitmap_button_1.SetSize(self.bitmap_button_1.GetBestSize())
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        awesome_sizer = wx.BoxSizer(wx.VERTICAL)
        id_sizer = wx.BoxSizer(wx.HORIZONTAL)

        
        sizer_2.Add(self.bitmap_button_1, 2, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        awesome_sizer.Add(self.light, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_TOP, 5)

        id_sizer.Add(self.tag, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        id_sizer.Add(self.id_ctrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        awesome_sizer.Add(id_sizer, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_TOP, 5)

        awesome_sizer.Add(self.button_1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_TOP, 10)
        sizer_2.Add(awesome_sizer, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_2)
        sizer_2.Fit(self)
        self.Layout()
        # end wxGlade

# end of class MyFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
