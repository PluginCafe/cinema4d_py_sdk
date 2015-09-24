"""
CVRss
Copyright: Rick Barrett
Written for Cinema 4D R12.016

Modified Date: 08/30/2010
"""


import c4d
import os
import urllib
import webbrowser

from c4d import bitmaps, gui, plugins

from xml.dom import minidom

# be sure to use a unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1025244

# container ids
FEED = 1000
ITEMS = 1001
SCROLL = 1002
INTERVAL = 1003
CUSTOM_URLS = 1004

#feed
MNU_PLAYLIST = {"id": 1006, "name": "Cineversity Playlists","url": "http://www.cineversity.com/search/playlists_rss/"}
MNU_TUTORIAL = {"id": 1006, "name": "Cineversity Tutorials","url": "http://www.cineversity.com/search/tutorials_rss/"}
MNU_TW_CIN = {"id": 1007, "name": "Twitter @cineversity", "url": "http://twitter.com/statuses/user_timeline/18199026.rss"}
MNU_MAXONNEWS = {"id": 1008, "name": "MAXON News","url": "http://www.maxon.net/index.php?id=1164&type=100&L=0"}
MNU_TW_MAXON3D = {"id": 1009, "name": "Twitter @maxon3d","url": "http://twitter.com/statuses/user_timeline/18089167.rss"}
MNU_CUSTOM = {"id": 1010, "name": "Custom", "url": ""}

#items
ITEMS_5 = {"id": 1011, "name": "5", "private": 5}
ITEMS_10 = {"id": 1012, "name": "10", "private": 10}
ITEMS_25 = {"id": 1013, "name": "25", "private": 25}
ITEMS_50 = {"id": 1014, "name": "50", "private": 50}
ITEMS_100 = {"id": 1015, "name": "100", "private": 100}

#scroll
SCROLL_5 = {"id": 1016, "name": "1 sec", "private": 1}
SCROLL_10 = {"id": 1017, "name": "5 sec", "private": 5}
SCROLL_15 = {"id": 1018, "name": "10 sec", "private": 10}
SCROLL_30 = {"id": 1019, "name": "30 sec", "private": 30}
SCROLL_60 = {"id": 1020, "name": "60 sec", "private": 60}

#interval
INTERVAL_1 = {"id": 1021, "name": "1 min", "private": 1}
INTERVAL_5 = {"id": 1022, "name": "5 min", "private": 5}
INTERVAL_10 = {"id": 1023, "name": "10 min", "private": 10}
INTERVAL_30 = {"id": 1024, "name": "30 min", "private": 30}
INTERVAL_60 = {"id": 1025, "name": "60 min", "private": 60}

#about
ABOUT = {"id": 1026, "name": "About"}

#gui elements
TXT_LABEL = {"id": 1027, "name": "Cinversity Tutorials: "}
BTN_NEXT = {"id": 1028, "name": ">", "width": 8, "height": 8}

# MyDialog class
class MyDialog(gui.GeDialog):

    rss_items = []
    rss_url = "http://www.cineversity.com/search/playlists_rss/"
    current_item = 0
    scroll_items = 5
    scroll_time = 1000*10
    update_time = 1000*60*10
    last_update = 0
    CVRssData = None

    def CreateLayout(self):
        #set the title
        self.SetTitle("Cineversity RSS")
        
        #create the menu
        self.MenuFlushAll()
        #feed menu
        self.MenuSubBegin("Feed")
        self.MenuAddString(MNU_PLAYLIST["id"], MNU_PLAYLIST["name"])
        self.MenuAddString(MNU_TUTORIAL["id"], MNU_TUTORIAL["name"])
        self.MenuAddString(MNU_TW_CIN["id"], MNU_TW_CIN["name"])
        self.MenuAddString(MNU_MAXONNEWS["id"], MNU_MAXONNEWS["name"])
        self.MenuAddString(MNU_TW_MAXON3D["id"], MNU_TW_MAXON3D["name"])
        self.MenuAddSeparator()
        self.MenuAddString(MNU_CUSTOM["id"], MNU_CUSTOM["name"])
        self.MenuSubEnd()
        #scroll menu
        self.MenuSubBegin("Scroll")
        self.MenuAddString(SCROLL_5["id"],  SCROLL_5["name"]+"&c&")
        self.MenuAddString(SCROLL_10["id"], SCROLL_10["name"])
        self.MenuAddString(SCROLL_15["id"], SCROLL_15["name"])
        self.MenuAddString(SCROLL_30["id"], SCROLL_30["name"])
        self.MenuAddString(SCROLL_60["id"], SCROLL_60["name"])
        self.MenuSubEnd()
        #items menu
        self.MenuSubBegin("Items")
        self.MenuAddString(ITEMS_5["id"], ITEMS_5["name"])
        self.MenuAddString(ITEMS_10["id"], ITEMS_10["name"])
        self.MenuAddString(ITEMS_25["id"], ITEMS_25["name"])
        self.MenuAddString(ITEMS_50["id"], ITEMS_50["name"])
        self.MenuAddString(ITEMS_100["id"], ITEMS_100["name"])
        self.MenuSubEnd()
        #update menu
        self.MenuSubBegin("Update")
        self.MenuAddString(INTERVAL_1["id"], INTERVAL_1["name"])
        self.MenuAddString(INTERVAL_5["id"], INTERVAL_5["name"])
        self.MenuAddString(INTERVAL_10["id"], INTERVAL_10["name"])
        self.MenuAddString(INTERVAL_30["id"], INTERVAL_30["name"])
        self.MenuAddString(INTERVAL_60["id"], INTERVAL_60["name"])
        self.MenuSubEnd()
        #about/branding menu
        self.MenuSubBegin("Cineversity RSS")
        self.MenuAddString(ABOUT["id"], ABOUT["name"])
        self.MenuSubEnd()
        self.MenuFinished()
        
        #the dialog itself - just a static text label and button
        self.GroupBegin(id=0, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT, cols=30, rows=1, title="", groupflags=0)
        self.element = self.AddStaticText(id=TXT_LABEL["id"],
                                          flags=c4d.BFH_SCALEFIT,
                                          initw=0,
                                          inith=0,
                                          name=TXT_LABEL["name"],
                                          borderstyle=c4d.BORDER_THIN_IN)
        
        self.button = self.AddButton(id=BTN_NEXT["id"], flags=c4d.BFH_RIGHT,
                            initw=BTN_NEXT["width"],
                            inith=BTN_NEXT["height"],
                            name=BTN_NEXT["name"])
        self.GroupEnd()
        return True
    
    def InitValues(self):
        # Get saved values from container
        self.CVRssData = plugins.GetWorldPluginData(PLUGIN_ID)
        if self.CVRssData:
            self.rss_url = self.CVRssData[FEED]
            self.scroll_items = self.CVRssData[ITEMS]
            self.scroll_time = self.CVRssData[SCROLL]
            self.update_time = self.CVRssData[INTERVAL]
        else:
            self.CVRssData = c4d.BaseContainer()
        # When the dialog opens, get the RSS feed
        self.UpdateRss()
        # Set the dialog timer to trigger based on the scroll time
        self.SetTimer(self.scroll_time)
        return True

    def Timer(self, msg):
        # When the timer fires, call the Scroll RSS function
        self.ScrollRss()

    def ScrollRss(self):
        # Called by the dialog timer at the scroll_time interval
        
        # Test to see if update time has been reached
        if c4d.GeGetTimer() > self.last_update + self.update_time:
            self.UpdateRss()                # update the feed
        
        # Scroll functionality - get the item and update the dialog
        # the XML parser delivers unicode - has to be encoded first
        if len(self.rss_items)==0:
            title = "No RSS feeds"
        else:
            title = unicode(self.rss_items[self.current_item]['title'])
        
        # update the "element" dialog item
        self.SetString(self.element, title)
        
        # update the current_item variable
        self.current_item = self.current_item + 1
        # loop condition if we've reached the last item or scroll_items
        if self.current_item >= len(self.rss_items) or self.current_item >= self.scroll_items:
            self.current_item = 0

    def UpdateRss(self):
        # Get the RSS Url and parse its XML
        print "Updating... " + self.rss_url
        dom = minidom.parse(urllib.urlopen(self.rss_url))
        # Reset the rss_items list - otherwise the new ones get tacked on the old
        self.rss_items = []
        # Loop thru the XML "item" nodes
        for node in dom.getElementsByTagName("item"):
	    if node.getElementsByTagName('pubDate'):
		pubdata = node.getElementsByTagName('pubDate')[0].firstChild.data
	    elif node.getElementsByTagName('dc:date'):
		pubdata = node.getElementsByTagName('dc:date')[0].firstChild.data
	    
            # Append the title, link and pubdate to the rss_items list
            self.rss_items.append({
                'title':node.getElementsByTagName('title')[0].firstChild.data,
                'link':node.getElementsByTagName('link')[0].firstChild.data,
                'pubdata':pubdata
                })
        
        # Reset the last_update variable so we know when the update happened
        self.last_update = c4d.GeGetTimer()
        
        # Update the dialog with the ScrollRss function
        self.ScrollRss()
        
    def GoToUrl(self):
        # BUTTON TRIGGER
        # Go to the link associated with the currently displayed item
        url = self.rss_items[self.current_item-1]['link'].encode('utf-8')
        webbrowser.open(url, 2, True)
        return True
    
    def Command(self, id, msg):
        #interval check
        if id==SCROLL_5["id"]:
            self.SetScrollTime(SCROLL_5["private"])
            self.MenuInitString(SCROLL_5["id"], True, True)
        elif id==SCROLL_10["id"]:
            self.SetScrollTime(SCROLL_10["private"])
            self.MenuInitString(SCROLL_10["id"], True, True)
        elif id==SCROLL_15["id"]:
            self.SetScrollTime(SCROLL_15["private"])
            self.MenuInitString(SCROLL_15["id"], True, True)
        elif id==SCROLL_30["id"]:
            self.SetScrollTime(SCROLL_30["private"])
            self.MenuInitString(SCROLL_30["id"], True, True)
        elif id==SCROLL_60["id"]:
            self.SetScrollTime(SCROLL_60["private"])
            self.MenuInitString(SCROLL_60["id"], True, True)
        #rss feeds
        elif id==MNU_TUTORIAL["id"]:
            self.SetFeedUrl(MNU_TUTORIAL["url"])
        elif id==MNU_TW_CIN["id"]:
            self.SetFeedUrl(MNU_TW_CIN["url"])
        elif id==MNU_MAXONNEWS["id"]:
            self.SetFeedUrl(MNU_MAXONNEWS["url"])
        elif id==MNU_TW_MAXON3D["id"]:
            self.SetFeedUrl(MNU_TW_MAXON3D["url"])
        elif id==MNU_CUSTOM["id"]:
            self.SetFeedUrl(MNU_CUSTOM["url"])
        #items
        elif id==ITEMS_5["id"]:
            self.SetScrollItems(ITEMS_5["private"])
        elif id==ITEMS_10["id"]:
            self.SetScrollItems(ITEMS_10["private"])
        elif id==ITEMS_25["id"]:
            self.SetScrollItems(ITEMS_25["private"])
        elif id==ITEMS_50["id"]:
            self.SetScrollItems(ITEMS_50["private"])
        elif id==ITEMS_100["id"]:
            self.SetScrollItems(ITEMS_100["private"])
        #interval
        elif id==INTERVAL_1["id"]:
            self.SetUpdateTime(INTERVAL_1["private"])
        elif id==INTERVAL_5["id"]:
            self.SetUpdateTime(INTERVAL_5["private"])
        elif id==INTERVAL_10["id"]:
            self.SetUpdateTime(INTERVAL_10["private"])
        elif id==INTERVAL_30["id"]:
            self.SetUpdateTime(INTERVAL_30["private"])
        elif id==INTERVAL_60["id"]:
            self.SetUpdateTime(INTERVAL_60["private"])
        #interval
        elif id==ABOUT["id"]:
            self.About()
        elif id==BTN_NEXT["id"]:
            self.GoToUrl()
        
        return True
    
    def SetFeedUrl(self, private):
        # MENU ITEM - Feed
        # private contains feed url or "" for custom
        if private == "":
            # pop up a dialog to get the custom url
            self.rss_url = gui.InputDialog("Custom URL", self.rss_url)
        else:
            # set the chosen url
            self.rss_url = private
        # if the url isn't blank, update the RSS
        if self.rss_url != "":
            self.UpdateRss()
            self.UpdatePrefs()
        return True  

    def SetScrollItems(self, private):
        # MENU ITEM - Items
        # Sets scroll_items variable - how many items to scroll through
        self.scroll_items = private
        self.UpdatePrefs()
        return True

    def SetScrollTime(self, private):
        # MENU ITEM - Scroll
        # Sets the amount of time to show each item
        # private = time in seconds
        self.scroll_time = private*1000     #in milliseconds!
        self.SetTimer(self.scroll_time)    #reset the dialog timer
        self.UpdatePrefs()
        return True

    def SetUpdateTime(self, private):
        # MENU ITEM - Update
        # Sets the amount of time between updating RSS
        # private = time in minutes
        self.update_time = private*1000*60  #in milliseconds!
        self.UpdatePrefs()
        return True

    def About(self):
        # MENU ITEM - About
        # Open a messagebox with about info
        gui.MessageDialog("Cineversity RSS v0.7\nby Rick Barrett (SDG)", c4d.GEMB_OK)
        return True
        
    def UpdatePrefs(self):
        self.CVRssData.SetString(FEED, self.rss_url)
        self.CVRssData.SetLLong(ITEMS, self.scroll_items)
        self.CVRssData.SetLLong(SCROLL, self.scroll_time)
        self.CVRssData.SetLLong(INTERVAL, self.update_time)
        plugins.SetWorldPluginData(PLUGIN_ID, self.CVRssData)
    
 # Cineversity class
class CVRss(plugins.CommandData):

    dialog = None
    
    def Execute(self, doc):
        # create the dialog
        if self.dialog is None:
            self.dialog = MyDialog()
        
        return self.dialog.Open(dlgtype=c4d.DLG_TYPE_ASYNC, pluginid=PLUGIN_ID, defaultw=400, defaulth=32)

    def RestoreLayout(self, sec_ref):
        # manage nonmodal dialog
        if self.dialog is None:
            self.dialog = MyDialog()
            
        return self.dialog.Restore(pluginid=PLUGIN_ID, secret=sec_ref)


# main
if __name__ == "__main__":
    # load icon.tif from res into bmp
    bmp = bitmaps.BaseBitmap()
    dir, file = os.path.split(__file__)
    fn = os.path.join(dir, "res", "icon.tif")
    bmp.InitWith(fn)
    # register the plugin
    plugins.RegisterCommandPlugin(id=PLUGIN_ID, 
                                  str="Py-Cineversity RSS",
                                  info=0,
                                  help="Displays a chosen RSS feed", 
                                  dat=CVRss(),
                                  icon=bmp)
