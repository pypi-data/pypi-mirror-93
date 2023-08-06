
# Metarace : Cycle Race Abstractions
# Copyright (C) 2012  Nathan Fraser
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# HACK: track lap times, toward the "hotlap" event - more work required.

import os
import logging
import csv
import ConfigParser
import gtk
import glib
import gobject

import metarace
from metarace import scbwin
from metarace import tod
from metarace import uiutil
from metarace import eventdb
from metarace import riderdb
from metarace import strops
from metarace import printing

# config version string
EVENT_ID = 'hotlap-1.6'

# Model columns
COL_BIB = 0
COL_NAME = 1
COL_CUR = 2
COL_LAST = 3
COL_BEST = 4

# sort on time
def sort_timefield(x,y):
    return cmp(x[2],y[2])

# scb function key mappings
key_reannounce = 'F4'	# (+CTRL)
key_abort = 'F5'	# (+CTRL)
key_startlist = 'F3'
key_results = 'F4'

class hotlap(object):
    def loadconfig(self):
        """Load race config from disk."""
        self.riders.clear()
        cr = ConfigParser.ConfigParser({'startlist':'',
                                        'id':EVENT_ID,
                                        'showinfo':'Yes'
                                        })
        cr.add_section('event')

        if os.path.isfile(self.configpath):
            self.log.debug('Attempting to read config from '
                               + repr(self.configpath))
            cr.read(self.configpath)
        for r in cr.get('event', 'startlist').split():
            lasttod = None
            besttod = None
            if cr.has_option('laps', r):
                ril = csv.reader([cr.get('laps', r)]).next() 
                if len(ril) > 0:
                    lasttod = tod.str2tod(ril[0])
                if len(ril) > 1: 
                    besttod = tod.str2tod(ril[1])
            self.addrider(r, last=lasttod, best=besttod)
            ## TODO : load/save comment for rider

        self.info_expand.set_expanded(strops.confopt_bool(
                                       cr.get('event', 'showinfo')))

        self.recalculate()

        # After load complete - check config and report. This ensures
        # an error message is left on top of status stack. This is not
        # always a hard fail and the user should be left to determine
        # an appropriate outcome.
        eid = cr.get('event', 'id')
        if eid and eid != EVENT_ID:
            self.log.error('Event configuration mismatch: '
                           + repr(eid) + ' != ' + repr(EVENT_ID))
            #self.readonly = True

    def startlist_report(self, program=False):
        """Return a startlist report."""
        ret = []
        sec = printing.section()
        headvec = [u'Event', self.evno, u':', self.event[u'pref'],
                         self.event[u'info']]
        if not program:
            headvec.append(u'- Start List')
        sec.heading = u' '.join(headvec)
        sec.lines = []
        for r in self.riders:
            rno = r[COL_BIB]
            rname = r[COL_NAME]
            sec.lines.append([None, rno, rname, None, None, None])
        ret.append(sec)
        return ret

    def get_startlist(self):
        """Return a list of bibs in the rider model."""
        ret = []
        for r in self.riders:
            ret.append(r[COL_BIB])
        return ' '.join(ret)

    def saveconfig(self):
        """Save race to disk."""
        if self.readonly:
            self.log.error('Attempt to save readonly ob.')
            return
        cw = ConfigParser.ConfigParser()
        cw.add_section('event')
        cw.set('event', 'startlist', self.get_startlist())
        cw.set('event', 'events', self.events)
        cw.set('event', 'evnicks', ' '.join(self.nicknames))
        cw.set('event', 'showinfo', self.info_expand.get_expanded())
        cw.set('event', 'id', EVENT_ID)
        self.log.debug('Saving race config to: ' + self.configpath)
        cw.add_section('laps')
        for r in self.riders:
            last = u''
            if r[COL_CUR]:
                last = r[COL_CUR].rawtime()
            best = u''
            if r[COL_BEST]:
                best = r[COL_BEST].rawtime()
            cw.set('laps', r[COL_BIB], u','.join([last, best]))
        with open(self.configpath, 'wb') as f:
            cw.write(f)

    def result_gen(self):
        """Generator function to export a final result."""
        for r in self.riders:
            bib = r[COL_BIB]
            rank = None
            info = ''
            if r[COL_PLACE] != '':
                if r[COL_PLACE].isdigit():
                    rank = int(r[COL_PLACE])
                    info = r[COL_PLACE]
                else:
                    # TODO: allow for 'dnf'/'dns' here, propagates into event
                    rank = r[COL_PLACE]
                    info = None		# no seeding info available
            time = None

            yield [bib, rank, time, info]

    def result_report(self):
        """Return a list of printing sections containing the race result."""
        ret = []
        sec = printing.section()
        sec.heading = 'Event ' + self.evno + ': ' + ' '.join([
                         self.event[u'pref'], self.event[u'info']]).strip()
        sec.subheading = self.standingstr()
        sec.lines = []
        aggtm = None
        prevline = None

        for r in self.riders:
            rno = r[COL_BIB]
            rname = strops.resname(r[COL_FIRST], r[COL_LAST],
                                       r[COL_CLUB])
            rank = ''
            if r[COL_PLACE] != '':
                rank = r[COL_PLACE]
                if rank.isdigit():
                    rank += '.'
            ptsstr = ''
            if r[COL_TOTAL] > 0:
                ptsstr = str(r[COL_TOTAL])
            tmstr = ''
            if r[COL_TIME] != tod.ZERO:
                tmstr = r[COL_TIME].rawtime(2)
            nrow = [rank, rno, rname, None, ptsstr, None, tmstr]
            if prevline:
                if rank and prevline[4] == ptsstr:	# same pts
                    prevline[5] = prevline[6]	# patch tmstr
                    nrow[5] = tmstr
                    aggtm = 'Time'
                prevline[6] = None
                sec.lines.append(prevline)
            prevline = nrow

        if prevline is not None:
            sec.lines.append(prevline)
        sec.colheader = [None, None, None, None, 'Points', aggtm]
        ret.append(sec)
        return ret

    def addrider(self, bib='', info=None, last=None, best=None):
        """Add specified rider to race model."""
        nr=[bib, '', last, best, best]
        if bib == '' or self.getrider(bib) is None:
            dbr = self.meet.rdb.getrider(bib, self.series)
            if dbr is not None:
                rname = strops.listname(self.meet.rdb.getvalue(dbr, 1),
                                        self.meet.rdb.getvalue(dbr, 2),
                                        self.meet.rdb.getvalue(dbr, 3))
                nr[1] = rname
            return self.riders.append(nr)
        else:
            return None

    def getrider(self, bib):
        """Return temporary reference to model row."""
        ret = None
        for r in self.riders:
            if r[COL_BIB] == bib:
                ret = r         ## DANGER- Leaky ref
                break
        return ret

    def delrider(self, bib):
        """Remove the specified rider from the model."""
        i = self.getiter(bib)
        if i is not None:
            self.riders.remove(i)

    def getiter(self, bib):
        """Return temporary iterator to model row."""
        i = self.riders.get_iter_first()
        while i is not None:
            if self.riders.get_value(i, COL_BIB) == bib:
                break
            i = self.riders.iter_next(i)
        return i

    def clearplaces(self):
        """Zero internal model for recalculate."""
        for r in self.riders:
            r[COL_PLACE] = ''
            r[COL_TOTAL] = 0
            r[COL_TIME] = tod.tod(0)
            r[COL_POINTS] = []

    def standingstr(self):
        """Return an event status string for reports and scb."""
        ret = u''
        if self.curevent is not None and self.lastevent is not None:
            if self.curevent != self.lastevent:
                ev = self.meet.edb[self.curevent]
                if ev is not None:
                    if self.curevent in self.eventstatusmap:
                        if self.eventstatusmap[self.curevent] in ['running']:
                            # force virtual for race in progress
                            self.resultvirtual = True
                    if self.resultvirtual:
                        ret = u'Virtual Standings'
                    else:
                        ret = u'Standings after ' + ev[u'info']
                else:
                    ret = u'Standings'               
            else:
                # TODO check for completion
                if self.resultvirtual:
                    ret = u'Virtual Standings'
                else:
                    ret = u'Final Result'
        return ret

    def sortomnium(self, x, y):
        """Sort results according to omnium rules."""

        # Comparison vecs: [idx, bib, rcnt, dnf, r[COL_TOTAL], r[COL_TIME]
        if x[2] == y[2]:	# Same number of results so far
            if x[3] == y[3]:	# Both dnf or not
                if x[3] == 'dnf':
                    return cmp(x[1], y[1])		# revert to bib
                else:
                    if x[4] == y[4]:			# same pts
                        if x[5] == y[5]:		# same aggregate time
                            return cmp(strops.riderno_key(x[1]),
                                       strops.riderno_key(y[1]))# revert to bib
                        else:
                            return cmp(x[5], y[5])
                    else:
                        return cmp(x[4], y[4])
            else:
                return cmp(x[3], y[3])		# In then DNF
        else:
            return cmp(y[2], x[2]) # Sort descending on rcount

    def recalculate(self):
        """Update internal model."""
        pass

    def key_event(self, widget, event):
        """Race window key press handler."""
        if event.type == gtk.gdk.KEY_PRESS:
            key = gtk.gdk.keyval_name(event.keyval) or 'None'
            if event.state & gtk.gdk.CONTROL_MASK:
                if key == key_abort or key == key_reannounce:
                    # override ctrl+f5
                    self.recalculate()
                    glib.idle_add(self.delayed_announce)
                    return True
            elif key[0] == 'F':
                if key == key_startlist:
                    self.do_startlist()
                    return True
                elif key == key_results:
                    self.do_places()
                    return True
        return False

    def delayed_announce(self):
        """Initialise the announcer's screen after a delay."""
        if self.winopen:
            self.meet.announce.clrall()

            self.meet.ann_title(' '.join([
                  'Event', self.evno, ':',
                  self.event[u'pref'], self.event[u'info'],
                  self.standingstr()]))
            self.meet.announce.linefill(1, '_')
        return False

    def do_startlist(self):
        """Show startlist on scoreboard."""
        self.meet.scbwin = None
        self.timerwin = False
        startlist = []
        name_w = self.meet.scb.linelen - 4
        fmt = [(3, u'r'), u' ', (name_w,u'l')]
        for r in self.riders:
            startlist.append([r[COL_BIB],
                              r[COL_NAME].decode('utf-8', 'ignore')])
        evtstatus = u'Startlist'
        self.meet.scbwin = scbwin.scbtable(scb=self.meet.scb,
                                     head=self.meet.racenamecat(self.event),
                                     subhead=evtstatus,
                                     coldesc=fmt, rows=startlist)
        self.meet.scbwin.reset()

    def do_places(self):
        """Show race result on scoreboard."""
        name_w = self.meet.scb.linelen - 9
        coldesc = [(3, u'l'), u' ', (name_w,u'l'), u' ', (4,u'r')]
        resvec = []
        for r in self.riders:
            thetime = r[COL_BEST] 
            if thetime:
                resvec.append([None, r[COL_NAME].decode('utf-8', 'ignore'),thetime])
        resvec.sort(sort_timefield)
        lt = None
        ct = 0
        lp = None
        for r in resvec:
            ct += 1
            if r[2] != lt:
                lp = unicode(ct)+u'.'
            r[0] = lp
            r[2] = r[2].rawtime(1)
        ## TODO: detect standings after nn/provisonal/final
        evtstatus = self.standingstr()
        self.meet.scbwin = scbwin.scbtable(scb=self.meet.scb,
                                    head=self.meet.racenamecat(self.event),
                                    subhead=evtstatus,
                                    coldesc=coldesc,
                                    rows=resvec)
        self.meet.scbwin.reset()
        return False

    def shutdown(self, win=None, msg='Exiting'):
        """Terminate race object."""
        self.log.debug('Race shutdown: ' + msg)
        if not self.readonly:
            self.saveconfig()
        self.winopen = False

    def timercb(self, e):
        """Handle a timer event."""
        return False

    def rftimercb(self, e):
        """Handle rftimer event."""
        if e.refid == '':       # got a trigger
            #return self.starttrig(e)
            return False

        # else assume this is a passing
        r = self.meet.rdb.getrefid(e.refid)
        if r is None:
            self.log.info('Unknown tag: ' + e.refid + '@' + e.rawtime(2))
            return False

        bib = self.meet.rdb.getvalue(r, riderdb.COL_BIB)
        ser = self.meet.rdb.getvalue(r, riderdb.COL_SERIES)
        if ser != self.series:
            self.log.error('Ignored non-series rider: ' + bib + '.' + ser)
            return False

        # at this point should always have a valid source rider vector
        lr = self.getrider(bib)
        if lr is None:
            self.log.warn('Ignoring non starter: ' + bib
                          + ' @ ' + e.rawtime(2))
            return False

        if lr[COL_CUR] is not None:
            laptime = e-lr[COL_CUR].truncate(2)
            if laptime < self.maxlap and laptime > self.minlap:
                if lr[COL_BEST] is not None:
                    if laptime < lr[COL_BEST]:
                        self.log.info(u'New Best Lap: ' + repr(bib) + ' :: '
                                 + laptime.rawtime(2))
                        lr[COL_BEST] = laptime
                        glib.idle_add(self.do_places)
                else:
                    lr[COL_BEST] = laptime
                lr[COL_LAST] = laptime
                if self.hotlap is None or laptime < self.hotlap:
                    self.hotlap = laptime
                    self.log.info(u'New Hot Lap: ' + repr(bib) + ' :: '
                                     + laptime.rawtime(2))
        lr[COL_CUR] = e

        self.log.info(u'Saw: ' + repr(bib) + '@' + e.rawtime(2))
        return False

    def timeout(self):
        """Update scoreboard and respond to timing events."""
        if not self.winopen:
            return False
        return True

    def do_properties(self):
        """Run race properties dialog."""
        b = gtk.Builder()
        b.add_from_file(os.path.join(metarace.UI_PATH, 'omnium_properties.ui'))
        dlg = b.get_object('properties')
        dlg.set_transient_for(self.meet.window)
        se = b.get_object('race_series_entry')
        se.set_text(self.series)
        re = b.get_object('race_events_entry')
        re.set_text(self.events)
        ne = b.get_object('race_nicks_entry')
        ne.set_text(' '.join(self.nicknames))
        response = dlg.run()
        if response == 1:       # id 1 set in glade for "Apply"
            self.log.debug('Updating race properties.')
            # update event config
            self.events = re.get_text()
            self.nicknames = ne.get_text().split()

            # update series
            ns = se.get_text()
            if ns != self.series:
                self.series = ns
                self.event[u'seri'] = ns

            # xfer starters if not empty
            slist = strops.reformat_riderlist(
                          b.get_object('race_starters_entry').get_text(),
                                        self.meet.rdb, self.series).split()
            for s in slist:
                self.addrider(s)

            self.recalculate()
            glib.idle_add(self.delayed_announce)
        else:
            self.log.debug('Edit race properties cancelled.')

        # if prefix is empty, grab input focus
        if self.prefix_ent.get_text() == '':
            self.prefix_ent.grab_focus()
        dlg.destroy()

    def destroy(self):
        """Signal race shutdown."""
        if self.context_menu is not None:
            self.context_menu.destroy()
        self.frame.destroy()

    def show(self):
        """Show race window."""
        self.frame.show()

    def hide(self):
        """Hide race window."""
        self.frame.hide()

    def update_expander_lbl_cb(self):
        """Update race info expander label."""
        self.info_expand.set_label('Race Info : '
                    + self.meet.racenamecat(self.event, 64))

    def editent_cb(self, entry, col):
        """Shared event entry update callback."""
        if col == u'pref':
            self.event[u'pref'] = entry.get_text().decode('utf-8', 'replace')
        elif col == u'info':
            self.event[u'info'] = entry.get_text().decode('utf-8', 'replace')
        self.update_expander_lbl_cb()

    def todcur(self, col, cr, model, iter, data=None):
        """Format tod into text for listview."""
        lt = model.get_value(iter, COL_LAST)
        if lt is not None and lt != tod.ZERO:
            cr.set_property('text', lt.timestr(2))
        else:
            cr.set_property('text', '')

    def todbest(self, col, cr, model, iter, data=None):
        """Format tod into text for listview."""
        bt = model.get_value(iter, COL_BEST)
        if bt is not None and bt > tod.tod('8.0'):
            cr.set_property('text', bt.timestr(2))
        else:
            cr.set_property('text', '')

    def editcol_db(self, cell, path, new_text, col):
        """Cell update with writeback to meet."""
        new_text = new_text.strip()
        self.riders[path][col] = new_text.strip()
        glib.idle_add(self.meet.rider_edit, self.riders[path][COL_BIB],
                                           self.series, col, new_text)

    def treeview_button_press(self, treeview, event):
        """Set callback for mouse press on model view."""
        if event.button == 3:
            pathinfo = treeview.get_path_at_pos(int(event.x), int(event.y))
            if pathinfo is not None:
                path, col, cellx, celly = pathinfo
                treeview.grab_focus()
                treeview.set_cursor(path, col, 0)
                self.context_menu.popup(None, None, None,
                                        event.button, event.time)
                return True
        return False

    def tod_context_clear_activate_cb(self, menuitem, data=None):
        """Clear times for selected rider."""
        # clear has no real meaning in omnium
        glib.idle_add(self.delayed_announce)

    def tod_context_edit_activate_cb(self, menuitem, data=None):
        """Run edit time dialog."""
        # no edit time for now in omnium
        glib.idle_add(self.delayed_announce)

    def tod_context_del_activate_cb(self, menuitem, data=None):
        """Delete selected row from race model."""
        sel = self.view.get_selection().get_selected()
        if sel is not None:
            i = sel[1]  # grab off row iter
            if self.riders.remove(i):
                pass    # re-select?
            glib.idle_add(self.delayed_announce)

    def __init__(self, meet, event, ui=True):
        """Constructor."""
        self.meet = meet
        self.event = event      # Note: now a treerowref
        self.evno = event[u'evid']
        self.evtype = event[u'type']
        self.series = event[u'seri']
        self.configpath = meet.event_configfile(self.evno)
        self.log = logging.getLogger('omnium')
        self.log.setLevel(logging.DEBUG)
        self.log.debug('opening event: ' + str(self.evno))
        self.curevent = None
        self.lastevent = None
        self.resultvirtual = False
        self.eventstatusmap = {}
        self.hotlap = None
        self.minlap = tod.tod(15)
        self.maxlap = tod.tod(32)

        # race run time attributes
        self.onestart = False
        self.readonly = not ui
        self.winopen = True
        self.events = ''
        self.nicknames = []


        self.riders = gtk.ListStore(gobject.TYPE_STRING, # 0 bib
                                    gobject.TYPE_STRING, # 1 name
                                    gobject.TYPE_PYOBJECT, # 2 current start
                                    gobject.TYPE_PYOBJECT, # 3 last lap
                                    gobject.TYPE_PYOBJECT) # 4 best lap

        b = gtk.Builder()
        b.add_from_file(os.path.join(metarace.UI_PATH, 'omnium.ui'))

        self.frame = b.get_object('omnium_vbox')
        self.frame.connect('destroy', self.shutdown)

        # info pane
        self.info_expand = b.get_object('info_expand')
        b.get_object('omnium_info_evno').set_text(self.evno)
        self.showev = b.get_object('omnium_info_evno_show')
        self.prefix_ent = b.get_object('omnium_info_prefix')
        self.prefix_ent.connect('changed', self.editent_cb,u'pref')
        self.prefix_ent.set_text(self.event[u'pref'])
        self.info_ent = b.get_object('omnium_info_title')
        self.info_ent.connect('changed', self.editent_cb,u'info')
        self.info_ent.set_text(self.event[u'info'])

        self.update_expander_lbl_cb()

        # riders pane
        t = gtk.TreeView(self.riders)
        self.view = t
        t.set_reorderable(True)
        t.set_enable_search(False)
        t.set_rules_hint(True)
        t.connect('button_press_event', self.treeview_button_press)

        # riders columns
        uiutil.mkviewcoltxt(t, 'No.', COL_BIB, calign=1.0)
        uiutil.mkviewcoltxt(t, 'Name', COL_NAME, expand=True)
        uiutil.mkviewcoltod(t, 'Last', cb=self.todcur)
        uiutil.mkviewcoltod(t, 'Best', cb=self.todbest)
        t.show()
        b.get_object('omnium_result_win').add(t)

        self.context_menu = None
        if ui:
            # connect signal handlers
            b.connect_signals(self)
            b = gtk.Builder()
            b.add_from_file(os.path.join(metarace.UI_PATH, 'tod_context.ui'))
            self.context_menu = b.get_object('tod_context')
            b.connect_signals(self)
