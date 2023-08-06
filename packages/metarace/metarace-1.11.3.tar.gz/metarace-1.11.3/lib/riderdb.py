
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

"""Rider 'database' utilities

Manage a rider db with the columns described below. Input columns
may be arranged in any order if the column header is present. Riders
are uniquely identified by their series and number, which may be specified
explicitly as a tuple: (no,series) or as a combined string 'no.series'. 

Numbers and series keys are matched case-insensitively, and must only 
contain alphanumeric characters 0-9, A-Z, a-z. All other values associated
with a rider are unicode strings.

	no	"No"
		Rider number
	seri	"Series"
		Rider's number series (optional)
	firs	"First Name"
		Rider full first name
	last	"Last Name"
		Rider full last name
	club	"Club"
		Club/team/state/nation field
	cate	"Category"
		A space separated list of rider category keys for this rider
	uci	"UCI ID"
		Rider's UCI ID
	lice	"License No."
		Rider's License no or namebank key
	rfid	"RFID No"
		Rider's RFID, or Transponder no (if relevant)
	nati	"Nation DoB"
		Rider's Nation and DoB (old UCI Code)

Reserved number series:

	team	Extended team information (for road tours)
	cat	Extended category information


"""

import gtk
import gobject
import glib
import logging
import os

from metarace import uiutil
from metarace import strops
from metarace import ucsv
from metarace import namebank

# Model column constants
COL_BIB = 0
COL_FIRST = 1
COL_LAST = 2
COL_CLUB = 3
COL_CAT = 4
COL_SERIES = 5
COL_REFID = 6
COL_UCICODE = 7
COL_NOTE = 8

# wheeltime refid prefix
TAGPREFIX = '058001'

# Reserved rider numbers.
RESERVED_NOS = [u'bib', u'no.', u'no', u'all', u'number', u'num']

# Default rider values if not empty string
RIDER_DEFAULTS = {
	u'no':None,
}

# rider db column heading and key mappings
RIDER_COLUMNS = {
	u'no':		u"No",
	u'seri':	u"Series",
	u'firs':	u"First Name",
	u'last':	u"Last Name",
	u'club':	u"Club/Team",
	u'cate':	u"Category",
	u'uci':		u"UCI ID",
	u'lice':	u"License No.",
	u'rfid':	u"RFID No",
	u'nati':	u"Nation DoB"
}

RIDER_COLUMN_CONVERTERS= {
	u'no':strops.confopt_riderno,
	u'seri':strops.confopt_riderno
}


def colkey(colstr=u''):
    return colstr[0:4].lower().strip()


class riderdb(object):
    """Rider database."""
    def addempty(self, bib=u'', series=u''):
        """Add a new empty row in the rider model."""
        i = self.model.append([bib.lower(), u'', u'', u'', u'',
                                series, u'', u'', u''])
        ref = gtk.TreeRowReference(self.model, self.model.get_path(i))
        if self.view is not None:
            self.postedit = None
            self.gotorow(ref)
        return ref

    def clear(self):
        """Clear rider model."""
        self.log.debug('Rider model cleared.')
        self.model.clear()

    def load_chipfile(self, csvfile=None):
        """Load refids from the named chipfile into to the riderdb."""
        count = 0
        if os.path.isfile(csvfile):
            self.log.debug(u'Loading refids from ' + repr(csvfile))
            with open(csvfile, 'rb') as f:
                cr = ucsv.UnicodeReader(f)
                for row in cr:
                    ir = [cell.translate(strops.PRINT_UTRANS) for cell in row]
                    if len(ir) > 1 and ir[0] != u'Refid':
                        nrefid = ir[0].strip().lower()
                        if len(nrefid) > 6 and nrefid[0:6] == TAGPREFIX:
                            nrefid = nrefid[6:]		# strip off prefix
                        bib = ir[1].strip().lower()
                        series = u''
                        if len(ir) > 2:
                            series = ir[2].strip()

                        if bib.isalnum() and bib not in RESERVED_NOS:
                            bibser = strops.bibser2bibstr(bib, series)
                            self.tagmap[nrefid] = bibser
                            self.maptag[bibser] = nrefid
                            dbr = self.getrider(bib, series) 
                            if dbr is not None:
                                self.editrider(ref=dbr,
                                               refid=nrefid)
                            count += 1
                        else:
                            self.log.warn(u'Invalid No.: %s', bib)
            self.log.debug(u'Loaded ' + unicode(count) + u' refids from ' 
                            + repr(csvfile))

    def load(self, csvfile=None, namedb=None, overwrite=False):
        """Load riders from supplied CSV file."""
        count = 0
        if os.path.isfile(csvfile):
            self.log.debug(u'Loading riders from ' + repr(csvfile))
            with open(csvfile, 'rb') as f:
                cr = ucsv.UnicodeReader(f)
                for row in cr:
                    ir = [cell.translate(strops.PRINT_UTRANS) for cell in row]
                    if len(ir) > 0 and ir[0] != u'Bib' and ir[0] != u'No.':
                        bib = ir[COL_BIB].strip().lower()
                        if bib.isalnum() and bib not in RESERVED_NOS:
                            nr = [bib, u'', u'', u'', u'', u'', u'', u'', u'']
                            for i in range(1,9):
                                if len(ir) > i:
                                    nr[i] = ir[i].strip()

                            # overwrite name fields if license no provided
                            if namedb and len(ir) > 1 and ir[1].isdigit():
                                nkey = ir[1].encode('ascii','ignore')
                                if nkey in namedb:
                                    # overwrite name fields with stored vals
                                    sr = namedb[nkey]
                                    for i in [1, 2]:	# first, last
                                        nr[i] = sr[i]
                                    if nr[COL_CLUB] == u'':	# club
                                        nr[COL_CLUB] = sr[namebank.COL_CLUB]
                                    if nr[COL_CAT] == u'':	# NRS/Origin
                                        nr[COL_CAT] = sr[namebank.COL_STATE]
                                    if nr[COL_REFID] == u'':	# refid
                                        nr[COL_REFID] = sr[namebank.COL_REFID]
                                    self.log.info(
       u'Loaded rider detail from namebank: ' + repr(bib)+ u':' + repr(nkey))

                            # overwrite refid in load data if chipfile loaded
                            bibser = strops.bibser2bibstr(bib, nr[COL_SERIES])
                            if bibser in self.maptag:
                                if nr[COL_REFID] == u'':
                                    nr[COL_REFID] = self.maptag[bibser]
                            oldr = self.getrider(bib, nr[COL_SERIES])
                            if oldr is not None:
                                # entry already exists, ignore or remove
                                if overwrite:
                                    self.log.info(u'Replaced: '+repr(bibser))
                                    self.model.remove(self.model.get_iter(
                                          oldr.get_path()))
                                else:
                                    self.log.warn(u'Duplicate ignored: '
                                              + repr(bibser))
                                    continue 
                            # strip wheeltime prefix 
                            if len(nr[COL_REFID]) > 8:
                                if nr[COL_REFID][0:6] == TAGPREFIX:
                                    nr[COL_REFID] = nr[COL_REFID][6:]
                            self.model.append(nr)
                            count += 1
                        else:
                            self.log.warn(u'Invalid No.: ' + repr(bib))
            self.log.debug('Loaded ' + unicode(count) + ' riders from ' 
                            + repr(csvfile))

    def save_chipfile(self, csvfile=None):
        """Save refids from current model to supplied CSV file."""
        chipmap = {}
        chiplist = []
        count = 0
        if os.path.exists(csvfile):
            # load in old chipfile 
            with open(csvfile, 'rb') as f:
                cr = ucsv.UnicodeReader(f)
                for row in cr:
                    ir = [cell.translate(strops.PRINT_UTRANS) for cell in row]
                    if len(ir) > 1 and ir[0] != u'Refid':
                        nrefid = ir[0].strip().lower()
                        bib = ir[1].strip().lower()
                        series = u''
                        if len(ir) > 2:
                            series = ir[2].strip()

                        if bib.isalnum() and bib not in RESERVED_NOS:
                            bibstr = strops.bibser2bibstr(bib, series)
                            if bibstr not in chipmap:
                                chipmap[bibstr] = nrefid
                                chiplist.append(bibstr)
                                count += 1
                        else:
                            self.log.warn(u'Invalid No.: ' + repr(bib))
                self.log.debug(u'Loaded ' + unicode(count) + u' refids from ' 
                            + repr(csvfile))

        # overwrite any existing refids
        ocount = 0
        ncount = 0
        for r in self.model:
            urefid = r[COL_REFID].decode('utf-8')
            if urefid:
                ubib = r[COL_BIB].decode('utf-8')
                useries = r[COL_SERIES].decode('utf-8')
                bibstr = strops.bibser2bibstr(ubib, useries)
                if bibstr not in chipmap:
                    chiplist.append(bibstr)
                    ncount += 1
                else:
                    if urefid != chipmap[bibstr]:
                        ocount += 1
                chipmap[bibstr] = urefid
        self.log.debug(u'Replacing ' + unicode(ocount) + ' refids from model.')
        self.log.debug(u'Adding ' + unicode(ncount) + ' refids from model.')

        chiplist.sort(key=strops.bibstr_key)
        count = 0
        with open(csvfile, 'wb') as f:
            cr = ucsv.UnicodeWriter(f)
            cr.writerow([u'Refid',u'No.',u'Series'])
            for bs in chiplist:
                (bib, ser) = strops.bibstr2bibser(bs)
                refid = chipmap[bs]
                if refid:
                    count += 1
                    cr.writerow([refid, bib, ser])
        self.log.debug(u'Wrote ' + unicode(count) + u' refids to: '
                           + repr(csvfile))

    def save(self, csvfile=None):
        """Save current model to supplied CSV file."""
        self.log.debug(u'Saving riders to '+ repr(csvfile))
        with open(csvfile, 'wb') as f:
            cr = ucsv.UnicodeWriter(f)
            cr.writerow([u'No.',u'First Name',u'Last Name',u'Club/Team',
                         u'Category',u'Series(optional)',u'Refid',
                          u'UCI ID',u'Nation DoB'])
            cr.writerows(self)	# check the unicode out-in-out-in

    def gotorow(self, ref=None):
        """Move view selection to the specified row reference."""
        if ref is None and len(self.model) > 0:
            ref = gtk.TreeRowReference(self.model, 0)
        if ref is not None and ref.valid():
            path = ref.get_path()
            self.view.scroll_to_cell(path)
            self.view.set_cursor_on_cell(path)

    def delselected(self):
        """Delete the currently selected row."""
        if self.view is not None:
            model, iter = self.view.get_selection().get_selected()
            if iter is not None:
                ref = None
                if self.model.remove(iter):
                    ref = gtk.TreeRowReference(self.model,
                                         self.model.get_path(iter))
                self.gotorow(ref)

    def getselected(self):
        """Return a reference to the currently selected row, or None."""
        ref = None
        if self.view is not None:
            model, iter = self.view.get_selection().get_selected()
            if iter is not None:
                ref = gtk.TreeRowReference(self.model,
                                           self.model.get_path(iter))
        return ref

    def mkridermap(self, series=u''):
        """Return a formatted rider map for mkresult scripts."""
        # Note: Hack until riderdb modified to be same as eventdb
        ret = {}
        for r in self.model:
            if r[COL_SERIES] == series:
                key = r[COL_BIB].decode('utf-8')
                first = r[COL_FIRST].decode('utf-8')
                last = r[COL_LAST].decode('utf-8')
                club = r[COL_CLUB].decode('utf-8')
                cat = r[COL_CAT].decode('utf-8')
                refid = r[COL_REFID].decode('utf-8')
                ucicode = r[COL_UCICODE].decode('utf-8')
                note = r[COL_NOTE].decode('utf-8')
                rmap = {}
                rmap[u'bib']=key
                rmap[u'first']=first
                rmap[u'last']=last
                rmap[u'club']=club
                rmap[u'cat']=cat
                rmap[u'refid']=refid
                rmap[u'ucicode']=ucicode
                rmap[u'note']=note
                rmap[u'namestr']=strops.resname(first, last, club)
                rmap[u'name']=strops.resname(first, last)
                ret[key]=rmap
        return ret
        
    def mkview(self, bib=True, first=True, last=True, club=True,
                     cat=False, series=True, refid=False, ucicode=False, note=False):
        """Create and return view object for the model."""
        if self.view is not None:
            return self.view
        v = gtk.TreeView(self.model)
        v.set_reorderable(True)
        v.set_enable_search(False)
        v.set_rules_hint(True)
        v.connect('key-press-event', self.__view_key)
        v.show()
        self.colmap = {}
        colcnt = 0
        if bib:
            uiutil.mkviewcoltxt(v, 'No.', COL_BIB, self.__editcol_cb,
                      halign=0.5, calign=0.5, editcb=self.__editstart_cb)
            self.colmap[COL_BIB] = colcnt
            colcnt += 1
        if first:
            uiutil.mkviewcoltxt(v, 'First Name', COL_FIRST, self.__editcol_cb,
                            expand=True, editcb=self.__editstart_cb)
            self.colmap[COL_FIRST] = colcnt
            colcnt += 1
        if last:
            uiutil.mkviewcoltxt(v, 'Last Name', COL_LAST, self.__editcol_cb,
                            expand=True, editcb=self.__editstart_cb)
            self.colmap[COL_LAST] = colcnt
            colcnt += 1
        if club:
            uiutil.mkviewcoltxt(v, 'Club', COL_CLUB, self.__editcol_cb,
                            editcb=self.__editstart_cb)
            self.colmap[COL_CLUB] = colcnt
            colcnt += 1
        if cat:
            uiutil.mkviewcoltxt(v, 'Cat', COL_CAT, self.__editcol_cb,
                            editcb=self.__editstart_cb)
            self.colmap[COL_CAT] = colcnt
            colcnt += 1
        if series:
            uiutil.mkviewcoltxt(v, 'Ser', COL_SERIES, self.__editcol_cb, 
                            editcb=self.__editstart_cb)
            self.colmap[COL_SERIES] = colcnt
            colcnt += 1
        if refid:
            uiutil.mkviewcoltxt(v, 'Refid', COL_REFID, self.__editcol_cb, 
                            editcb=self.__editstart_cb)
            self.colmap[COL_REFID] = colcnt
            colcnt += 1
        if ucicode:
            uiutil.mkviewcoltxt(v, 'UCI Code', COL_UCICODE, self.__editcol_cb, 
                            editcb=self.__editstart_cb)
            self.colmap[COL_UCICODE] = colcnt
            colcnt += 1
        if note:
            uiutil.mkviewcoltxt(v, 'Note', COL_NOTE, self.__editcol_cb, 
                            editcb=self.__editstart_cb)
            self.colmap[COL_NOTE] = colcnt
            colcnt += 1
        self.view = v
        return self.view

    def getrider(self, bib, series=u''):
        """Return a reference to the row with the given bib and series."""
        ret = None
        bib = bib.lower()
        i = self.model.get_iter_first()
        while i is not None:
            if (self.get_value(i, COL_BIB) == bib
                and self.get_value(i, COL_SERIES) == series):
                ret = gtk.TreeRowReference(self.model,
                                           self.model.get_path(i))
                break
            i = self.model.iter_next(i)
        return ret

    def get_partner(self, bib, series=u''):
        """Return a reference to the 'partner' for the specified rider."""
        ret = None
        bib = bib.lower()
        i = self.model.get_iter_first()
        while i is not None:
            if (self.get_value(i, COL_BIB) == bib
                and self.get_value(i, COL_SERIES) == series):
                ret = gtk.TreeRowReference(self.model,
                                           self.model.get_path(i))
                break
            i = self.model.iter_next(i)

        if i is not None:
            # look up cat and note for partner link
            cat = self.get_value(i, COL_CAT)
            if cat and u'tandem' in cat.lower():
                pno = self.get_value(i, COL_NOTE)
                if pno:
                    ret = self.getrider(pno, series)
        return ret

    def nextriderin(self, bib, series=u''):
        """Return the rider following the specified bib in the series."""
        ret = None
        cur = self.getrider(bib, series)
        if cur is not None:
            i = self.model.iter_next(self.model.get_iter(cur.get_path()))
            while i is not None:
                if self.get_value(i, COL_SERIES) == series:
                    ret = self.get_value(i, COL_BIB)
                    break
                i = self.model.iter_next(i)
        return ret

    def nextriderno(self):
        """Try and return a new unique rider number string."""
        lmax = 1
        for r in self.model:
            ubib = r[COL_BIB].decode('utf-8')
            if ubib.isdigit() and int(ubib) >= lmax:
                lmax = int(ubib) + 1
        return unicode(lmax)

    def getrefid(self, refid):
        """Return a reference to the row with the given refid."""
        ## altered to allow multiple references
        ret = None
        ck = refid.lower()
        rno = None
        rser = None
        if u'riderno:' in ck: 
            rno,rser = strops.bibstr2bibser(ck.split(u':')[-1])
        i = self.model.get_iter_first()
        while i is not None:
            if rno and (self.get_value(i, COL_BIB) == rno
                and self.get_value(i, COL_SERIES) == rser):
                ret = gtk.TreeRowReference(self.model,
                                           self.model.get_path(i))
                break
            else:
                for dbref in self.get_value(i,COL_REFID).lower().split():
                    if dbref == ck:
                        ret = gtk.TreeRowReference(self.model,
                                           self.model.get_path(i))
                        break
            i = self.model.iter_next(i)
        return ret
        
    def biblistfromcat(self, cat, series=u''):
        """Return a list of rider numbers in the given cat."""
        ret = u''
        cat = cat.upper()
        i = self.model.get_iter_first()
        while i is not None:
            if (cat in self.get_value(i, COL_CAT).upper().split()
               and self.get_value(i, COL_SERIES) == series):
                ret += u' ' + self.get_value(i, COL_BIB)
            i = self.model.iter_next(i)
        return ret

    def getbibs(self, cat, series=u''):
        """Return a list of refs to riders in the given cat and series."""
        ret = []
        cat = cat.upper()
        i = self.model.get_iter_first()
        while i is not None:
            if (cat in self.get_value(i, COL_CAT).upper().split()
               and self.get_value(i, COL_SERIES) == series):
                ret.append(gtk.TreeRowReference(self.model,
                                           self.model.get_path(i)))
            i = self.model.iter_next(i)
        return ret

    def listseries(self):
        """Return a list of all the series in the rider db."""
        ret = []
        for row in self.model:
            useries = row[COL_SERIES].decode('utf-8')
            if useries not in ret:
                ret.append(useries)
        return ret

    def listcats(self, series=None):
        """Return a list of all the categories in the specified series."""
        ret = []
        for row in self.model:
            ucat = row[COL_CAT].decode('utf-8').upper().split()
            useries = row[COL_SERIES].decode('utf-8')
            for rrcat in ucat:
                if rrcat and rrcat not in ret and (series is None
                                             or useries == series):
                    ret.append(rrcat)
        return ret

    def get_value(self, iter, column):
        return self.model.get_value(iter, column).decode('utf-8')

    def get_rowvalue(self, row, column):
        return row[column].decode('utf-8')

    def getvalue(self, ref, col):
        """Return the specified column from the supplied row."""
        ret = None
        if ref.valid():
            ret = self.model[ref.get_path()][col].decode('utf-8')
        return ret

    def editrider(self, ref=None, first=None, last=None,
                  club=None, cat=None, refid=None, ucicode=None, 
                  note=None, bib=None):
        """Create or update the rider with supplied parameters."""
        i = None
        if ref is None:
            if bib is None:
                bib = self.nextriderno()
            ## ERROR: num not ever defined?
            i = self.model.append([bib, u'', u'', u'', u'', u'', u'', u'', u''])
            ref = gtk.TreeRowReference(self.model,
                                           self.model.get_path(i))
        if ref.valid():
            i = self.model.get_iter(ref.get_path())
            if first is not None:
                self.model.set_value(i, COL_FIRST, first)
            if last is not None:
                self.model.set_value(i, COL_LAST, last)
            if club is not None:
                self.model.set_value(i, COL_CLUB, club)
            if cat is not None:
                self.model.set_value(i, COL_CAT, cat)
            if refid is not None:
                self.model.set_value(i, COL_REFID, refid)
            if ucicode is not None:
                self.model.set_value(i, COL_UCICODE, ucicode)
            if note is not None:
                self.model.set_value(i, COL_NOTE, note)
        return ref

    def filter_nonempty(self, col=None):
        """Return a filter model with col non empty."""
        ret = self.model.filter_new()
        ret.set_visible_func(self.__filtercol, col)
        return ret
        
    def __editcol_cb(self, cell, path, new_text, col):
        """Update model if possible and request post-edit movement."""
        ret = False
        if new_text is not None:
            new_text = new_text.strip()
            if new_text != self.model[path][col].decode('utf-8'):
                if col == COL_BIB:
                    if new_text.isalnum() and new_text.lower != 'all':
                        if not self.getrider(new_text,
                                 self.model[path][COL_SERIES].decode('utf-8')):
                            self.model[path][COL_BIB] = new_text.lower()
                            ret = True
                        else:
                            self.log.warn(
                              'Refusing to update no. to duplicate rider.')
                            self.postedit='same'
                            ret = True	# re-focus on the entry
                    else:
                        self.log.warn('Invalid no. number ignored.')
                elif col == COL_SERIES:
                    if not self.getrider(
                          self.model[path][COL_BIB].decode('utf-8'), new_text):
                        self.model[path][COL_SERIES] = new_text
                        ret = True
                    else:  # This path is almost never a real problem
                        self.log.debug(
                          'Refusing to update series to duplicate rider.')
                        ret = True
                else:
                    self.model[path][col] = new_text
                    ret = True
            else:	# No Change, but entry 'accepted'
                ret = True
        if ret and self.postedit is not None:
            glib.idle_add(self.__postedit_move, path, self.colmap[col])
        return ret

    def __postedit_move(self, path, col):
        """Perform a post-edit movement of the selection.

           NOTE: This 'col' refers to VIEW column index and not the
                 model's column index.

        """
        if self.postedit is None:	# race possible here
            return False

        # step 1: process left/right
        if self.postedit == 'left':
            col -= 1
            self.postedit = None
        elif self.postedit == 'right':
            col += 1
            self.postedit = None

        if col < 0:
            col = len(self.colmap) - 1
            self.postedit = 'up'    # followup with a upward movement
        elif col >= len(self.colmap):
            col = 0
            self.postedit = 'down'  # followup with a downward movement

        # step 2: check for additional up/down
        i = self.model.get_iter(path)
        if self.postedit == 'up':
            p = int(self.model.get_string_from_iter(i)) - 1
            if p >= 0:
                path = self.model.get_path(
                            self.model.get_iter_from_string(str(p)))
            else:
                return False    # can't move any further 'up'
        elif self.postedit == 'down':
            i = self.model.iter_next(i)
            if i is not None:
                path = self.model.get_path(i)
            else:
                return False    # no more rows to scroll to -> perhaps add?
        self.postedit = None    # suppress any further change
        return self.__moveto_col(path, col)

    def __moveto_col(self, path, col):
        """Move selection to supplied path and column.

           NOTE: This 'col' refers to VIEW column index and not the
                 model's column index.

        """
        self.view.scroll_to_cell(path,
                                 self.view.get_column(col),
                                 False)
        self.view.set_cursor(path,
                             self.view.get_column(col), True)
        return False

    def __view_key(self, widget, event):
        """Handle key events on tree view."""
        if event.type == gtk.gdk.KEY_PRESS:
            if event.state & gtk.gdk.CONTROL_MASK:
                key = gtk.gdk.keyval_name(event.keyval) or 'None'
                if key.lower() == 'a':
                    self.addempty()
                    return True
                elif key == 'Delete':
                    self.delselected()
                    return True
        return False

    def __edit_entry_key_cb(self, widget, event, editable=None):
        """Check key press in cell edit for postedit move."""
        if event.type == gtk.gdk.KEY_PRESS:
            key = gtk.gdk.keyval_name(event.keyval) or 'None'
            if key == 'Tab':
                self.postedit = 'right'
            elif key in ['Return', 'Escape']:   # allow cancel to handle
                self.postedit = None
            elif key == 'Up':
                if editable is None:
                    self.postedit = 'up'
            elif key == 'Down':
                if editable is None:
                    self.postedit = 'down'
            elif key == 'Right':
                if self.editwasempty:
                    self.postedit = 'right'
                    if editable is not None:
                        editable.editing_done()
                    else:
                        widget.editing_done()
            elif key == 'Left':
                if self.editwasempty:
                    self.postedit = 'left'
                    if editable is not None:
                        editable.editing_done()
                    else:
                        widget.editing_done()
        return False

    def __editstart_cb(self, cr, editable, path, data=None):
        """Prepare cell entry for post-edit movement."""
        self.postedit = None
        if type(editable) is gtk.Entry:
            self.editwasempty = len(editable.get_text()) == 0
            editable.connect('key-press-event', self.__edit_entry_key_cb)
        else:   # this is crap - but don't know the type
            self.editwasempty = False

    def __filtercol(self, model, iter, data=None):
        return bool(self.model.get_value(iter, data))

    def __iter__(self):
        """Map out unicode strings."""
        for r in self.model:
            yield [a.decode('utf-8') for a in r]

    def __init__(self):
        """Constructor for the rider db.

        Constructs a new rider database object. This function does
        not create the view object, use the mkview() function to
        create and return a valid treeview.

        """

        self.log = logging.getLogger('riderdb')
        self.log.setLevel(logging.DEBUG)
        self.model = gtk.ListStore(gobject.TYPE_STRING,	# 0 bib
                                   gobject.TYPE_STRING, # 1 first name
                                   gobject.TYPE_STRING, # 2 last name
                                   gobject.TYPE_STRING, # 3 club
                                   gobject.TYPE_STRING, # 4 category
                                   gobject.TYPE_STRING, # 5 series
                                   gobject.TYPE_STRING, # 6 refid
                                   gobject.TYPE_STRING, # 7 ucicode
                                   gobject.TYPE_STRING) # 8 note
        self.tagmap = {}
        self.maptag = {}
        self.view = None
        self.colvec = []
        self.postedit = None
        self.editwasempty = False

class listofentry(object):
    """Load and manage a MR style list of entries."""
    def __init__(self):
        __model = {}
        __event_name = None
       
    

