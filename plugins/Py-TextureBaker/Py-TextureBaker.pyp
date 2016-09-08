"""
Texture Baker
Copyright: MAXON Computer GmbH
Written for Cinema 4D R18.020

Last Modified Date: 23/08/2016
"""

import c4d
from c4d import bitmaps, documents, gui, plugins, threading, utils

# Be sure to use a unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1037872

# Thread for the TextureBaker Command Plugin
class TextureBakerThread(threading.C4DThread):

    # Initializes the Texture Baker thread
    def __init__(self, doc, textags, texuvws, destuvws):
        self.doc = doc
        self.textags = textags
        self.texuvws = texuvws
        self.destuvws = destuvws

        self.bakeDoc = None
        self.bakeData = None
        self.bakeBmp = bitmaps.MultipassBitmap(256, 256, c4d.COLORMODE_RGB)
        self.bakeError = c4d.BAKE_TEX_ERR_NONE

    # Setups and starts the texture baking thread
    def Begin(self):
        bakeData = c4d.BaseContainer()
        bakeData[c4d.BAKE_TEX_WIDTH] = 256
        bakeData[c4d.BAKE_TEX_HEIGHT] = 256
        bakeData[c4d.BAKE_TEX_PIXELBORDER] = 1
        bakeData[c4d.BAKE_TEX_CONTINUE_UV] = False
        bakeData[c4d.BAKE_TEX_SUPERSAMPLING] = 0
        bakeData[c4d.BAKE_TEX_FILL_COLOR] = c4d.Vector(1)
        bakeData[c4d.BAKE_TEX_USE_BUMP] = False
        bakeData[c4d.BAKE_TEX_USE_CAMERA_VECTOR] = False
        bakeData[c4d.BAKE_TEX_AUTO_SIZE] = False
        bakeData[c4d.BAKE_TEX_NO_GI] = False
        bakeData[c4d.BAKE_TEX_GENERATE_UNDO] = False
        bakeData[c4d.BAKE_TEX_PREVIEW] = False
        bakeData[c4d.BAKE_TEX_COLOR] = True
        bakeData[c4d.BAKE_TEX_UV_LEFT] = 0.0
        bakeData[c4d.BAKE_TEX_UV_RIGHT] = 1.0
        bakeData[c4d.BAKE_TEX_UV_TOP] = 0.0
        bakeData[c4d.BAKE_TEX_UV_BOTTOM] = 1.0

        self.bakeData = bakeData

        # Initializes bake process
        bakeInfo = utils.InitBakeTexture(self.doc, self.textags, self.texuvws, self.destuvws, self.bakeData, self.Get())
        self.bakeDoc = bakeInfo[0]
        self.bakeError = bakeInfo[1]

        if self.bakeError != c4d.BAKE_TEX_ERR_NONE or self.bakeDoc is None:
            return False

        # Starts bake thread
        self.Start(c4d.THREADMODE_ASYNC, c4d.THREADPRIORITY_BELOW)

        return True

    # Texture Baker hook
    # Prints the baker progress information
    def BakeTextureHook(self, info):
        print info

    # Bake Texture Thread Main routine
    def Main(self):
        self.bakeError = utils.BakeTexture(self.bakeDoc, self.bakeData, self.bakeBmp, self.Get(), self.BakeTextureHook)
        c4d.SpecialEventAdd(PLUGIN_ID) # Send core message once baking has finished

    # Checks for user break
    def TestDBreak(self):
        return False


# Main dialog for the Texture Baker
class TextureBakerDlg(gui.GeDialog):

    BUTTON_BAKE = 1000
    BUTTON_ABORT = 1001

    aborted = False
    textureBakerThread = None
    infoText = None

    def CreateLayout(self):

        self.SetTitle("Texture Baker")

        self.GroupBegin(id=0, flags=c4d.BFH_SCALEFIT, rows=1, title="", cols=2, groupflags=0)
        self.AddButton(id=self.BUTTON_BAKE, flags=c4d.BFH_LEFT, initw=100, inith=25, name="Bake")
        self.AddButton(id=self.BUTTON_ABORT, flags=c4d.BFH_LEFT, initw=100, inith=25, name="Abort")
        self.GroupEnd()

        self.GroupBegin(id=0, flags=c4d.BFH_SCALEFIT, rows=1, title="", cols=1, groupflags=0)
        self.infoText = self.AddStaticText(id=0, initw=0, inith=0, name="", borderstyle=0, flags=c4d.BFH_SCALEFIT)
        self.GroupEnd()

        self.EnableButtons(False)

        return True

    def EnableButtons(self, baking):
        self.Enable(self.BUTTON_BAKE, not baking)
        self.Enable(self.BUTTON_ABORT, baking)

    def Command(self, id, msg):

        if id==self.BUTTON_BAKE:
            self.Bake()
        elif id==self.BUTTON_ABORT:
            self.Abort()

        return True

    def Bake(self):
        doc = documents.GetActiveDocument()
        if doc is None:
            return

        textags = []
        texuvws = []

        objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)
        if len(objects) == 0:
            return

        # Gather texture and UVW tags from the objects to bake
        for obj in objects:
            tag = obj.GetTag(c4d.Ttexture)
            if tag is None:
                return
            textags.append(tag)

            tag = obj.GetTag(c4d.Tuvw)
            if tag is None:
                return
            texuvws.append(tag)

        # Initialize and start texture baker thread
        self.aborted = False
        self.textureBakerThread = TextureBakerThread(doc, textags, texuvws, None)
        if not self.textureBakerThread.Begin():
            print "Bake Init Failed: Error " + str(self.textureBakerThread.bakeError)
            self.SetString(self.infoText, str("Bake Init Failed: Error " + str(self.textureBakerThread.bakeError)))
        else:
            self.EnableButtons(True)
            self.SetString(self.infoText, "Baking")

    def Abort(self):
        if self.textureBakerThread and self.textureBakerThread.IsRunning():
            self.aborted = True
            self.textureBakerThread.End()
            self.textureBakerThread = None

    def CoreMessage(self, id, msg):
        # Checks if texture baking has finished
        if id==PLUGIN_ID:

            self.EnableButtons(False)

            # Aborted?
            if not self.aborted:
                # Not aborted
                print "Baking Finished"
                self.SetString(self.infoText, str("Baking Finished"))
                bmp = self.textureBakerThread.bakeBmp
                if bmp:
                    bitmaps.ShowBitmap(bmp)
                self.textureBakerThread = None
                return True
            else:
                # Aborted
                print "Baking Aborted"
                self.SetString(self.infoText, str("Baking Aborted"))

            return True

        return gui.GeDialog.CoreMessage(self, id, msg)

    def AskClose(self):
        self.Abort()            # Abort on close
        return False


# Texture Baker Command Plugin
class TextureBakerData(c4d.plugins.CommandData):
    dialog = None

    def Execute(self, doc):
        if self.dialog is None:
            self.dialog = TextureBakerDlg()

        return self.dialog.Open(dlgtype=c4d.DLG_TYPE_ASYNC, pluginid=PLUGIN_ID, defaultw=250, defaulth=50)

    def RestoreLayout(self, sec_ref):
        if self.dialog is None:
            self.dialog = TextureBakerDlg()

        return self.dialog.Restore(pluginid=PLUGIN_ID, secret=sec_ref)


if __name__ == "__main__":
    plugins.RegisterCommandPlugin(id=PLUGIN_ID, str="Py-TextureBaker",
                                  help="Py - Texture Baker", info=0,
                                  dat=TextureBakerData(), icon=None)
