import os
PLUGIN_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW'
###########################################################################
if os.path.exists('/var/lib/dpkg/status'):
    enigmaos = 'oe2.2'
else:
    enigmaos = 'oe2.0'
#################################################################################
def Copy_Donnees(what):
    Milef = '/usr/lib/enigma2/python/Plugins/Extensions/SupTVoDNeW/Cfg/foldImag'
    if os.path.isfile(Milef):
        file_write = open(Milef, 'w')
        file_write.write(str(what))
        file_write.close()
################################################################################################Spinner
from Components.GUIComponent import GUIComponent
from enigma import ePixmap, eTimer
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS
def startspinner():
    cursel = PLUGIN_PATH + '/img/spinner'
    Bilder = []
    if cursel:
        for i in range(30):
            if os.path.isfile('%s/wait%d.png' % (cursel, i + 1)):
                Bilder.append('%s/wait%d.png' % (cursel, i + 1))
    else:
        Bilder = []
    Copy_Donnees(Bilder)
    return Spinner(Bilder)
def buildBilder():
    cursel = PLUGIN_PATH + '/img/spinner'
    Bilder = []
    if cursel:
        for i in range(30):
            if os.path.isfile('%s/wait%d.png' % (cursel, i + 1)):
                Bilder.append('%s/wait%d.png' % (cursel, i + 1))
    else:
        Bilder = []
    return Bilder
class Spinner(GUIComponent):
    def __init__(self, Bilder):
        GUIComponent.__init__(self)
    def SetBilder(self, Bilder):
        self.Bilder = Bilder
    GUI_WIDGET = ePixmap
    def start(self, Bilder):
        self.len = 0
        self.SetBilder(Bilder)
        self.timer = eTimer()
        try:
            if enigmaos == 'oe2.0':
                self.timer.callback.append(self.Invalidate)
            else:
                return
                self.timer_conn = self.timer.timeout.connect(self.Invalidate)
        except:
            pass
        self.timer.start(100)
    def stop(self):
        self.timer.stop()
        if enigmaos == 'oe2.0':
            self.timer.callback.remove(self.Invalidate)
        else:
            self.timer_conn = None
        return
    def destroy(self):
        try:
            self.timer.stop()
            if enigmaos == 'oe2.0':
                self.timer.callback.remove(self.Invalidate)
            else:
                self.timer_conn = None
        except:
            pass
        return
    def Invalidate(self):
        try:
            if self.instance:
                if self.len >= len(self.Bilder):
                    self.len = 0
                self.instance.setPixmapFromFile(self.Bilder[self.len])
                self.len += 1
        except:
            pass