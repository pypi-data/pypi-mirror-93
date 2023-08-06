
import pygtk
pygtk.require("2.0")

import gtk
import glib
#import pango
import gobject

import os
import sys
import logging
import metarace
from metarace import uiutil
from metarace import tod
from metarace import ucsv

COL_RNO = 0
COL_NAME = 1
COL_START = 2
COL_HIT = 3
COL_FINISH = 4
COL_ELAPSED = 5
COL_INFO = 6
CONFIG = u'sittt.csv'

class sittt:
    def loadconfig(self):
        lfile = os.path.join(self.configpath, CONFIG)
        if os.path.exists(lfile):
            with open(lfile, 'rb') as f:
                cr = ucsv.UnicodeReader(f)
                for r in cr:
                    nr = [u'',u'',u'',u'',u'',u'',u'']
                    if len(r) > 6 and r[0] != 'No.':
                        for c in [0,1,3,6]:
                            nr[c] = r[c]
                        for c in [2,4,5]:
                            nv = tod.str2tod(r[c])
                            if nv is not None:
                                nr[c] = nv.rawtime(2)
                        self.model.append(nr)
        glib.idle_add(self.recalc)

    def saveconfig(self):
        sfile = os.path.join(self.configpath, CONFIG)
        hdr = [u'No.',u'Rider',u'Start',u'Hit',u'Finish',u'Elapsed',u'Info']
        with metarace.savefile(sfile) as f:
            cw = ucsv.UnicodeWriter(f)
            cw.writerow(hdr)
            for r in self.model:
                cw.writerow(r)
        self.dosave = False
        return False

    def start(self):
        pass

    def meet_destroy_cb(self, window, msg=u''):
        """Handle destroy signal and exit application."""
        self.window.hide()
        self.saveconfig()
        gtk.main_quit()

    def shutdown(self, msg=None, data=None):
        pass

    def editcol_cb(self, cell, path, new_text, col):
        """Edit column callback."""
        recalc = False
        new_text = new_text.strip()
        if col in [2,4,5]:
            nv = tod.str2tod(new_text)
            if nv is not None:
                new_text = nv.rawtime(2)
            else:
                new_text = u''
            recalc = True
            self.dosave = True
        self.model[path][col] = new_text
        if recalc:
            glib.idle_add(self.recalc)

    def set_time(self, rider=None, finish=None, hitno=None):
        """Find and update the rider."""
        if rider is None:
            return
        nr = None
        for r in self.model:
            if r[0] == rider:
                nr = r
        if nr is None:
            # make a new rider record
            ni = self.model.append([rider, u'', u'', u'', u'',u'',u''])
            if ni is not None:
                nr = self.model[self.model.get_path(ni)]

        if finish is not None:
            nr[COL_FINISH] = finish.rawtime(2)
        nr[COL_HIT] = hitno
        self.dosave = True
        glib.idle_add(self.recalc)

    def entry_cb(self, entry, data=None):
        """Manual entry."""
        tvec = entry.get_text().split()
        tt = None
        rno = None
        hit = u''
        if len(tvec) > 0:
            tt = tod.str2tod(tvec[0])
        if len(tvec) > 1:
            rno = tvec[1]
        if len(tvec) > 2:
            hit = tvec[2]
        if tt is not None and rno is not None:
            self.set_time(rider=rno, finish=tt, hitno=hit)
            entry.set_text(u'')
        elif tt is not None:
            entry.set_text(tt.rawtime(2) + u' ')
        return True

    def recalc(self, data=None):
        """Re-calculate elapsed fields."""
        res = tod.todlist()
        for r in self.model:
            rno = r[COL_RNO]
            st = tod.str2tod(r[COL_START])
            ft = tod.str2tod(r[COL_FINISH])
            if rno and st is not None and ft is not None:
                elap = ft - st
                res.insert(elap, rno)
                r[COL_ELAPSED] = elap.rawtime(2)
        for r in self.model:
            rno = r[COL_RNO]
            info = u''
            rk = res.rank(rno)
            if rk is not None and rk < 10:
                info = u'({0}.)'.format(rk+1)
                if rk == 0:
                    self.label.set_text(u'Leader: ' + rno + u' ' + r[COL_NAME])
            r[COL_INFO] = info
        if self.dosave:
            glib.idle_add(self.saveconfig)
        return False

    def __init__(self, configpath=None, etype=None):
        """SITTT constructor."""
        # logger and log handler
        self.log = logging.getLogger()
        self.log.setLevel(logging.DEBUG)
        self.loghandler = None  # set in loadconfig to meet dir

        # meet configuration path and options
        if configpath is None:
            configpath = u'.'   # None assumes 'current dir'
        self.configpath = configpath

        b = gtk.Builder()
        b.add_from_file(os.path.join(metarace.UI_PATH, u'sittt.ui'))
        self.window = b.get_object('window')
        self.label = b.get_object('info')
        self.viewbox = b.get_object('viewbox')
        self.model = gtk.ListStore(gobject.TYPE_STRING, # rno
                                   gobject.TYPE_STRING, # name
                                   gobject.TYPE_STRING, # start
                                   gobject.TYPE_STRING, # hit
                                   gobject.TYPE_STRING, # median
                                   gobject.TYPE_STRING, # elap
                                   gobject.TYPE_STRING) # info
        self.view = gtk.TreeView(self.model)
        self.view.set_rules_hint(True)
        t = self.view
        uiutil.mkviewcoltxt(t, 'No.', COL_RNO, cb=self.editcol_cb,calign=1.0)
        uiutil.mkviewcoltxt(t, 'Rider', COL_NAME, cb=self.editcol_cb,expand=True,maxwidth=500)
        uiutil.mkviewcoltxt(t, 'Start', COL_START, cb=self.editcol_cb,calign=1.0)
        uiutil.mkviewcoltxt(t, 'Hit', COL_HIT, cb=self.editcol_cb,calign=1.0)
        uiutil.mkviewcoltxt(t, 'Finish', COL_FINISH, cb=self.editcol_cb,calign=1.0)
        uiutil.mkviewcoltxt(t, 'Elapsed', COL_ELAPSED, cb=self.editcol_cb,calign=1.0)
        uiutil.mkviewcoltxt(t, 'Info', COL_INFO, cb=self.editcol_cb,calign=1.0)

        self.view.show()
        self.viewbox.add(self.view)
        self.dosave = False
        b.connect_signals(self)
        
#COL_SPARE = 0
#COL_RNO = 1
#COL_START = 2
#COL_HIT = 3
#COL_FINISH = 4
#COL_ELAP = 5
#COL_INFO = 6

def main(etype=None):
    """Run the application."""
    configpath = None

    # expand configpath on cmd line to realpath _before_ doing chdir
    if len(sys.argv) > 2:
        print(u'usage: sittt [configdir]\n')
        sys.exit(1)
    elif len(sys.argv) == 2:
        rdir = sys.argv[1]
        if not os.path.isdir(rdir):
            rdir = os.path.dirname(rdir)
        configpath = os.path.realpath(rdir)
    metarace.init()
    if configpath is not None:
        os.chdir(configpath)
    app = sittt(configpath, etype)
    app.loadconfig()    # exception here ok
    app.window.show()
    app.start()
    try:
        metarace.mainloop()
    except:
        app.shutdown(u'Exception from main loop.')
        raise

if __name__ == '__main__':
    main()

