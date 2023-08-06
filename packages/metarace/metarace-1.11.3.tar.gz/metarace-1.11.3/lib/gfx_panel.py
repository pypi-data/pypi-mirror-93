
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

"""Graphic Overlay Hackup."""

import pygtk
pygtk.require("2.0")

import gtk
import glib
import pango
import pangocairo
import cairo
import random
import logging
import os
import csv
#import rsvg

import metarace
from metarace import riderdb
from metarace import jsonconfig
from metarace import strops
from metarace import telegraph
from metarace import printing
from metarace import unt4
from metarace import tod
from metarace import ucsv

# Globals
CONFIGFILE = u'gfx_panel.json'
LOGFILE = u'gfx_panel.log'
#MONOFONT = u'unifont'	# fixed-width font for text panels
MONOFONT = u'monospace'	# fixed-width font for text panels
STDFONT = u'Nimbus Sans L Bold Italic Condensed' # proportional font for gfx
NOHDR = [u'Start', u'start', u'time', u'Time', u'']
DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 360
# http://graphics.stanford.edu/courses/cs248-98-fall/Final/q1.html
ARC_TO_BEZIER = 0.55228475

# colours !@#
TITLE_R = 0.0
TITLE_G = 0.21569
TITLE_B = 0.40392
DARK_R = 0.15765
DARK_G = 0.14588
DARK_B = 0.15373
LIGHT_R = 0.85
LIGHT_G = 0.85
LIGHT_B = 0.85

# Userkeys (roadtt mode)
KEY_TITLE = 'f1'
KEY_START = 's'
KEY_STANDINGS = 'space'
KEY_FINISH = 'f'
KEY_CLEAR = 'backspace'

def scaleup(c, s):
    """Scale colour value roughly up toward 1."""
    return 1.0-(s - s*c)

def roundedrec(cr,x,y,w,h,radius_x=8,radius_y=8):
    """Draw a rounded rectangle."""

    #from mono moonlight aka mono silverlight
    #test limits (without using multiplications)
    # http://graphics.stanford.edu/courses/cs248-98-fall/Final/q1.html
    ARC_TO_BEZIER = 0.55228475
    if radius_x > w - radius_x:
        radius_x = w / 2
    if radius_y > h - radius_y:
        radius_y = h / 2

    #approximate (quite close) the arc using a bezier curve
    c1 = ARC_TO_BEZIER * radius_x
    c2 = ARC_TO_BEZIER * radius_y
    cr.new_path();
    cr.move_to ( x + radius_x, y)
    cr.rel_line_to ( w - 2 * radius_x, 0.0)
    cr.rel_curve_to ( c1, 0.0, radius_x, c2, radius_x, radius_y)
    cr.rel_line_to ( 0, h - 2 * radius_y)
    cr.rel_curve_to ( 0.0, c2, c1 - radius_x, radius_y, -radius_x, radius_y)
    cr.rel_line_to ( -w + 2 * radius_x, 0)
    cr.rel_curve_to ( -c1, 0, -radius_x, -c2, -radius_x, -radius_y)
    cr.rel_line_to (0, -h + 2 * radius_y)
    cr.rel_curve_to (0.0, -c2, radius_x - c1, -radius_y, radius_x, -radius_y)
    cr.close_path ()

def monotext(cr, pr, l, oh, x1, msg):
    """Redraw a defined layout with no scale."""
    if msg is not None:
        cr.save()
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.set_line_width(4.0)
        l.set_text(msg)
        cr.move_to(x1, oh)
        pr.update_layout(l)
        cr.set_source_rgb(1.0,1.0,1.0)
        pr.show_layout(l)
        cr.restore()

def draw_layout(cr, pr, l, oh, x1, x2, msg, align=0, invert=False, colour=False):
    if msg is not None:
        cr.save()
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.set_line_width(4.0)
        maxw = x2 - x1
        l.set_text(msg)
        (tw,th) = l.get_pixel_size()	# !! faulty
        oft = 0.0
        if align != 0 and tw < maxw:
            oft = align * (maxw - tw)	# else squish
        cr.move_to(x1+oft, oh)	# move before applying conditional scale
        if tw > maxw:
            ## This seems to be faulty
            #cr.scale(float(maxw)/float(tw),1.0)
            pass
        pr.update_layout(l)

        # fill 
        if invert:
            cr.set_source_rgb(1.0,1.0,1.0)
        elif colour:
            cr.set_source_rgb(0.1372,0.2235,0.5215)
        else:
            cr.set_source_rgb(0.0,0.0,0.0)

        pr.show_layout(l)
        
        cr.restore()

def draw_text(cr, pr, oh, x1, x2, msg, align=0, invert=False,
                                    font=None, colour=False):
    if msg is not None:
        cr.save()
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.set_line_width(4.0)
        maxw = x2 - x1
        l = pr.create_layout()
        l.set_font_description(font)
        l.set_text(msg)
        (tw,th) = l.get_pixel_size()
        oft = 0.0
        if align != 0 and tw < maxw:
            oft = align * (maxw - tw)	# else squish
        cr.move_to(x1+oft, oh)	# move before applying conditional scale
        if tw > maxw:
            cr.scale(float(maxw)/float(tw),1.0)
        pr.update_layout(l)

        # fill 
        if invert:
            cr.set_source_rgb(1.0,1.0,1.0)
        elif colour:
            cr.set_source_rgb(0.1372,0.2235,0.5215)
        else:
            cr.set_source_rgb(0.0,0.0,0.0)

        pr.show_layout(l)
        
        cr.restore()

def tod2key(tod=None):
    """Return a key from the supplied time of day."""
    ret = None
    if tod is not None:
        ret = int(tod.truncate(0).timeval)
    return ret

class gfx_panel(object):
    """Graphical Panel."""
 
    def show(self):
        self.window.show()

    def hide(self):
        self.window.show()

    def start(self):
        """Start threads."""
        if not self.started:
            self.scb.start()
            self.scb.set_pub_cb(self.msg_cb)
            self.started = True

    def shutdown(self):
        """Cleanly shutdown."""
        self.scb.exit()
        self.scb.join()
        self.started = False

    def window_destroy_cb(self, window):
        """Handle destroy signal."""
        if self.started:
            self.shutdown()
        self.running = False
        gtk.main_quit()
    
    def area_expose_event_cb(self, widget, event):
        """Update desired portion of drawing area."""
        x , y, width, height = event.area
        widget.window.draw_drawable(widget.get_style().fg_gc[gtk.STATE_NORMAL],
                                    self.area_src, x, y, x, y, width, height)
        return False

    def general_clearing(self):
        """Handle a GC request and update dbrows accordingly."""
        nr = u'X' * self.monocols
        for i in range(0, self.monorows):
            self.dbrows[i] = nr
        #self.gdata = {}
        self.rows = []

    def draw_monotext(self, cr, pr):
        """Draw the plain text scoreboard."""
        lh = self.ph/self.monorows
        nt = u' '*self.monocols
        for i in range(0,self.monorows):
            if i in self.dbrows:
                nt = self.dbrows[i]
            curof = lh * i + self.monofontoffset
            draw_text(cr, pr, curof, 0.0, self.pw, nt,
                          font=self.monofontdesc, invert=True)
        # watermark
        
    def draw_image(self, cr, pr):
        """Draw an all-image overlay."""
        ov = self.overlays[self.curov]
        cr.set_source_surface(ov[u'image'])
        cr.paint()
        
    def draw_align(self, cr, pr):
        """Draw the alignment screen."""
        # re-set BG to solid white
        cr.set_source_rgb(1.0,1.0,1.0)
        cr.paint()

        # place alignment marks
        cr.set_source_rgb(0.1,0.1,0.1)
        cr.rectangle(0.0,0.0,self.pw,self.ph)
        cr.fill()

        cr.set_source_rgb(1.0,1.0,1.0)
        cr.set_line_width(0.75)
        lx = 0.2*self.pw
        ly = 0.2*self.ph
        bx = 0.8*self.pw
        by = 0.8*self.ph
        llx = 0.02*self.pw
        lly = 0.02*self.ph
        bbx = 0.98*self.pw
        bby = 0.98*self.ph

        # TL 10% crop
        cr.move_to(llx,ly)
        cr.line_to(llx,lly)
        cr.line_to(lx,lly)
        # BL 10% crop
        cr.move_to(llx,by)
        cr.line_to(llx,bby)
        cr.line_to(lx,bby)
        # TR 10% crop
        cr.move_to(bbx,ly)
        cr.line_to(bbx,lly)
        cr.line_to(bx,lly)
        # BR 10% crop
        cr.move_to(bbx,by)
        cr.line_to(bbx,bby)
        cr.line_to(bx,bby)
        # TL diagonal
        cr.move_to(0.0,0.0)
        cr.line_to(lx, ly)
        # BL diagonal
        cr.move_to(0.0,self.ph)
        cr.line_to(lx,by)
        # BR diagonal
        cr.move_to(self.pw, self.ph)
        cr.line_to(bx,by)
        # TR diagonal
        cr.move_to(self.pw, 0.0)
        cr.line_to(bx,ly)
        cr.stroke()
         
        # Reference circle
        cr.set_source_rgb(0.5,0.5,1.0)
        xp = 0.3*self.pw
        yp = 0.25*self.ph
        rad = 0.15*self.ph
        cr.move_to(xp, yp)
        cr.arc(xp, yp, rad, 0, 6.3)
        cr.fill()
        cr.set_source_rgb(0.0,0.0,0.5)
        cr.move_to(xp-rad, yp)
        cr.line_to(xp+rad, yp)
        cr.move_to(xp, yp-rad)
        cr.line_to(xp, yp+rad)
        cr.stroke()
        
        # halfmarks
        cr.set_source_rgb(1.0,0.0,0.0)
        cr.set_dash([10.0,7.5])
        cr.move_to(0.0,0.5*self.ph)
        cr.line_to(self.pw,0.5*self.ph)
        cr.stroke()
        cr.set_source_rgb(0.0,1.0,0.0)
        cr.move_to(0.5*self.pw,0.0)
        cr.line_to(0.5*self.pw,self.ph)
        cr.stroke()

        # font desc
        cr.set_source_rgb(1.0,1.0,1.0)
        draw_text(cr, pr, 0.51*self.ph,
                          0.50*self.pw, 0.99*self.pw,
                          u'First LAST 1h23:45.67',
                          font=self.stdfontdesc, invert=True)

        cr.move_to(0.50*self.pw, 0.70*self.ph)
        cr.line_to(self.pw, 0.70*self.ph)
        nh = 0.70*self.ph + (self.ph/8.0)
        cr.move_to(0.50*self.pw, nh)
        cr.line_to(self.pw, nh)
        cr.stroke()
 
        draw_text(cr, pr, 0.70*self.ph+self.monofontoffset,
                          0.50*self.pw, 0.99*self.pw,
                          u'0123456789ABCDEF',
                          font=self.monofontdesc, invert=True)

        # draw pixel patch
        cr.save()
        cr.translate(0.5*self.pw-120,0.5*self.ph+20)
        cr.rectangle(0.0,0.0,100.0,100.0)
        cr.clip()
        cr.set_source_surface(self.overlays[u'align'][u'patch'])
        cr.paint()
        cr.restore()

    def draw_clock(self, cr, pr):
        """Draw the analog facility clock with start pips."""
        pass

    def draw_gfx(self):
        """Draw the whole graphical panel."""
        ov = self.overlays[u'gfx']
        cr = ov[u'cr']
        pr = ov[u'pr']

        # Return if no valid mode to work on
        if self.ovmode is None:
            self.log.debug(u'No valid gfx mode.')
            return

        # is cr valid?
        cr.save()

        # clear
        #cr.set_source_rgb(0.0,1.0,0.0) # KEY: Green
        cr.set_source_rgb(0.0,0.0,0.0)
        cr.paint()

        # draw the data rows?
        dorows = True

        # Titles	-> top
        if self.ovmode in [u'title', u'standings']:
            #and self.title or self.subtitle:
            titleof = 0.0
            if self.ovmode == u'title':
                dorows = False
                titleof = 11.0*self.growh
            self.title_pane(cr, pr, self.safetop + titleof)
            # logos
            if titleof > self.growh:
                ov[u'lml'].draw(cr, pr)
                ov[u'lsl'].draw(cr, pr)
            else:
                ov[u'ml'].draw(cr, pr)
                ov[u'sl'].draw(cr, pr)
            if self.title:
                draw_layout(cr, pr, ov[u'mtl'],
                          titleof + self.safetop + self.stdfontoffset,
                          self.safeleft + self.growlogow, self.saferight-self.growlogow,
                          self.title, align=0.5, invert=True)
            thesub = self.subtitle
            if self.ovmode == u'title':
                thesub = self.altsubtitle
            if thesub:
                draw_layout(cr, pr, ov[u'mtl'],
                 titleof + self.safetop + self.stdfontoffset + self.growh,
                          self.safeleft + self.growlogow, self.saferight-self.growlogow,
                          thesub, align=0.5, invert=True)
        else:
            pass # not a titleable overlay mode

        # start of result rows 2 slots down page
        if dorows:
            rowh = self.safetop + 2.0 * self.growof
            for r in ov[u'rows']:
                if r[u'index'] in self.gdata:
                  dr = self.gdata[r[u'index']]
                  if dr[1]:
                    if dr[0] is not None:	# left panel has own deal
                        self.left_panel(cr, pr, rowh)
                # [u'll', u'rnl', u'rtl', u'rxl', u'lil', u'ril']:
                        draw_layout(cr, pr, r[u'll'], rowh + self.stdfontoffset,
                                  self.growll+self.growrad,
                                  self.growll+self.growlbw,
                                  dr[0],
                                  align = 0.5, invert=True)
                        
                    if dr[1] is not None or dr[2] is not None or dr[3] is not None:
                        self.mid_panel(cr, pr, rowh)
                        if dr[2] is not None:
                            draw_layout(cr, pr, r[u'rnl'], rowh + self.stdfontoffset,
                                  self.growmlt+self.growrad+self.growrad,
                                  self.growmrb,	# bottom
                                  dr[2],
                                  align = 0.0, invert=True)
                            # use left version
                        elif dr[3] is not None:
                            # use right version
                            pass
                        else:
                            draw_layout(cr, pr, r[u'rtl'], rowh + self.stdfontoffset,
                                  self.growmlt+self.growrad+self.growrad,
                                  self.growmrb,
                                  dr[2],
                                  align = 0.0, invert=True)
                    if dr[4] is not None or dr[5] is not None:
                        self.right_panel(cr, pr, rowh)
                        if dr[4]:	# centred text in right panel
                            draw_layout(cr, pr, r[u'rcl'], rowh + self.stdfontoffset,
                                  self.growmrt+self.growrad,
                                  self.growrr-self.growrad-self.growrad,
                                  dr[4],
                                  align = 0.5, invert=True)
                        elif dr[5]:
                            cr.save()                          
                            if not dr[6]: # apply clip region
                                cr.move_to(self.growmrt,rowh)
                                cr.line_to(self.growmrt+self.decimalw,rowh)
                                cr.line_to(self.growmrb+self.decimalw,rowh+self.growh)
                                cr.line_to(self.growmrb,rowh+self.growh)
                                cr.close_path()
                                cr.clip()
                            draw_layout(cr, pr, r[u'ril'], rowh + self.stdfontoffset,
                                  self.growmrt+self.growrad,
                                  self.growrr-self.growrad-self.growrad,
                                  dr[5],
                                  align = 1.0, invert=True)
                            cr.restore()	# balance contexts
                # append row offset for empty rows
                rowh += self.growof
        cr.restore()

    def draw_stdrow(self, cr, pr, rowh, row):
        if row[0]:
            self.left_panel(cr, pr, rowh)
            draw_text(cr, pr, rowh + self.stdfontoffset,
                              self.growll+self.growrad,
                              self.growll+self.growlbw,
                              row[0],
                              align = 0.5,
                              font=self.stdfontdesc, invert=True)
        if row[1]:
            self.mid_panel(cr, pr, rowh)
            draw_text(cr, pr, rowh + self.stdfontoffset,
                              self.growmlt, self.growmrb,
                              row[1],
                              align = 0.0,
                              font=self.stdfontdesc)
        if row[2]:
            self.right_panel(cr, pr, rowh)
            draw_text(cr, pr, rowh + self.stdfontoffset,
                          self.growrr-self.growrtw,
                          self.growrr-2*self.growrad,
                          row[2],
                          align = 1.0,
                          font=self.stdfontdesc, invert=True)

    def reinit_overlay(self):
        """Create handles for the GFX overlay."""
        cr = self.area_src.cairo_create()
        pr = pangocairo.CairoContext(cr)

        cr.identity_matrix()

        # adjust geometry
        cr.translate(self.xoft, self.yoft)
        cr.scale(self.width/(self.xscale*self.pw),
                 self.height/(self.yscale*self.ph))
        ov = self.overlays[u'gfx']
        ov[u'cr'] = cr
        ov[u'pr'] = pr
        # title layouts
        for tr in [u'mtl', u'stl']:
            ov[tr] = pr.create_layout()
            ov[tr].set_font_description(self.stdfontdesc)
            ov[u'pr'].update_layout(ov[tr])
        ov[u'rows'] = []
        for i in [0,1,2,3,4,5,6,7,8,9] :
            rdef = { u'index': i,
                     u'lp': None,	# left most panel
                     u'rno': None, # left side of middle panel
                     u'rtxt': None, # middle panel
                     u'rxtra': None, # right of middle panel
                     u'linfo': None, # left side of info panel
                     u'rinfo': None, # right side of info panel
                    }
            # Row by row layouts
            for lk in [u'll', u'rnl', u'rtl', u'rxl', u'lil', u'ril',u'rcl']:
                rdef[lk] = pr.create_layout()
                rdef[lk].set_font_description(self.stdfontdesc)
                ov[u'pr'].update_layout(rdef[lk])
            ov[u'rows'].append(rdef)
        ov[u'ml'] = printing.image_elem(self.safeleft,self.safetop,
                                 self.safeleft+self.growlogow,self.safetop+self.titleh,
                                 0.0, 0.5,
                                 ov[u'mainlogo'])
        lowpos = 11.0*self.growh
        ov[u'lml'] = printing.image_elem(self.safeleft,lowpos+self.safetop,
                                 self.safeleft+self.growlogow,lowpos+self.safetop+self.titleh,
                                 0.0, 0.5,
                                 ov[u'mainlogo'])
        ov[u'sl'] = printing.image_elem(self.saferight-self.growlogow, 
                                        self.safetop,
                                        self.saferight,
                                        self.safetop+self.titleh-self.growrad,
                                 1.0, 0.5,
                                 ov[u'sublogo'])
        ov[u'lsl'] = printing.image_elem(self.saferight-self.growlogow, 
                                        lowpos+self.safetop,
                                        self.saferight,
                                        lowpos+self.safetop+self.titleh-self.growrad,
                                 1.0, 0.5,
                                 ov[u'sublogo'])

    def area_redraw(self):
        """Lazy full area redraw method."""

        if self.curov == u'gfx':
            # check curov for mode
            if self.ovmode == u'start':
                self.gdata = {}
                if self.onstart is not None:
                    if self.onstart in self.rmap:
                        rname = self.rmap[self.onstart][u'namestr']
                        rnat = self.rmap[self.onstart][u'cat']
                    self.gdata[8] = [self.onstart,1,rname,1,rnat,None,1]
                #nd copy runtime datainto the gdata field

            elif self.ovmode == u'finish':
                self.gdata = {}
                if len(self.finishdat) > 2 and self.finishdat[1]:
                    #self.finishdat = [rank, bib, namestr, elap, speedstr, roll]
                    estr = u''
                    if self.finishdat[3] is not None:
                        estr = self.finishdat[3].rawtime(2)
                    self.gdata[8] = [self.finishdat[1],1,self.finishdat[2],1,None,estr,not self.finishdat[5]]
                    if not self.finishdat[5]:
                        self.gdata[9] = [None, 1, u'({0}) {1}'.format(self.finishdat[0], self.finishdat[4]),0,None,u'',1]
             #8:[u'221',1,u'Christopher JUUL JENSEN (TCS)',1,None,u'2:13.00',0],
             #8:[u'221',1,u'Christopher JUUL JENSEN (TCS)',1,None,u'2:14.27',1],
             #8:[u'221',1,u'Christopher JUUL JENSEN (TCS)',1,u'DEN',None,1],
             #9:[None,1,u'(2.)  \t56.7 km/h',0,None,u'+0.51',1],
                #nd copy runtime datainto the gdata field
       
            # New style - caches contexts
            return self.draw_gfx()

        # Old style re-creates on each draw
        cr = self.area_src.cairo_create()
        pr = pangocairo.CairoContext(cr)
        cr.identity_matrix()

        # adjust geometry
        cr.translate(self.xoft, self.yoft)
        cr.scale(self.width/(self.xscale*self.pw),
                 self.height/(self.yscale*self.ph))

        # clear
        #cr.set_source_rgb(0.0,1.0,0.0) # KEY: Green
        cr.set_source_rgb(0.0,0.0,0.0)
        cr.paint()

        # draw overlay
        if self.curov in self.overlays:
            if self.curov == u'align':
                self.draw_align(cr, pr)
            elif self.curov == u'0':
                self.draw_clock(cr, pr)
            elif self.curov == u'1':
                self.draw_monotext(cr, pr)
            elif self.curov in [u'2', u'3']:
                self.draw_image(cr, pr)
            else:
                self.log.error(u'missing handler for overlay '
                                 + repr(self.curov))
        
    def number_box(self, cr, hof):
        cr.move_to(255.0,hof-5.0)
        cr.rectangle(255.0,hof-5.0,90.0,80.0)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.set_source_rgb(0.95,0.75,0.75)
        cr.fill()
        cr.rectangle(257.0,hof-3.0,90.0,80.0)
        cr.set_source_rgb(0.5,0.3,0.3)
        cr.fill()
        cr.rectangle(256.0,hof-4.0,90.0,80.0)
        cr.set_source_rgb(0.9,0.2,0.2)
        cr.fill()

    def area_configure_event_cb(self, widget, event):
        """Re-configure the drawing area and redraw the base image."""
        self.dirty = True
        x, y, width, height = widget.get_allocation()
        ow = 0
        oh = 0
        if self.area_src is not None:
            ow, oh = self.area_src.get_size()
        if width > ow or height > oh:
            self.area_src = gtk.gdk.Pixmap(widget.window, width, height)
        self.width = float(width)
        self.height = float(height)
        self.reinit_overlay()
        self.area_redraw()
        self.area.queue_draw()
        return True

    def clear(self):
        """Clear all elements."""
        self.title = u''
        self.subtitle = u''
        self.rows = []
        self.dirty = True
        self.draw_and_update()
        
    def set_title(self, tstr=''):
        """Draw title and update."""
        self.title = tstr
        self.draw_and_update()

    def set_subtitle(self, tstr=''):
        """Draw subtitle and update."""
        self.subtitle = tstr
        self.draw_and_update()

    def clear_rows(self):
        """Empty gfx rows and redraw."""
        self.rows = []
        self.doredraw = True
 
    def add_row(self, msg=''):
        """Split row and then append to self.rows"""
        sr = msg.split(chr(unt4.US))
        if len(sr) > 2:
            self.rows.append([sr[0], sr[1], sr[2]])
        self.doredraw = True

    def loadconfig(self):
        """Load config from disk."""
        cr = jsonconfig.config({u'gfx_panel':{
                                    u'fullscreen':False,
                                    u'remoteport':u'',
                                    u'remoteuser':u'',
                                    u'remotechan':u'#agora',
                                    u'monofontsize':40,
                                    u'monofont':MONOFONT,
                                    u'monofontoffset':-4.0,
                                    u'stdfontoffset':-4.0,
                                    u'monorows':7,
                                    u'monocols':32,
                                    u'stdfontsize':20,
                                    u'stdfont':STDFONT,
                                    u'curov':u'blank'
                                 }})
        cr.add_section(u'gfx_panel')
        cwfilename = metarace.default_file(CONFIGFILE)
        cr.merge(metarace.sysconf, u'gfx_panel')

        # check for config file
        try:
            with open(cwfilename, 'rb') as f:
                cr.read(f)
        except Exception as e:
            self.log.error(u'Reading app config: ' + repr(e))

        if strops.confopt_bool(cr.get(u'gfx_panel', u'fullscreen')):
            self.dofullscreen = True
            #self.window.fullscreen()

        self.remoteport = cr.get(u'gfx_panel', u'remoteport')
        self.remotechan = cr.get(u'gfx_panel', u'remotechan')
        self.remoteuser = cr.get(u'gfx_panel', u'remoteuser')
        self.scb.set_portstr(portstr=self.remoteport,
                             channel=self.remotechan)
        if self.remoteuser:
            self.log.info(u'Enabled remote control by: '
                          + repr(self.remoteuser))
        else:
            self.log.info(u'Promiscuous remote control enabled.')

        self.stdfont = cr.get(u'gfx_panel',u'stdfont')
        self.monofont = cr.get(u'gfx_panel',u'monofont')
        self.monofontoffset = strops.confopt_float(cr.get(u'gfx_panel',
                                                      u'monofontoffset'))
        self.monofontsize = strops.confopt_float(cr.get(u'gfx_panel',
                                                      u'monofontsize'))
        self.stdfontoffset = strops.confopt_float(cr.get(u'gfx_panel',
                                                      u'stdfontoffset'))
        self.stdfontsize = strops.confopt_float(cr.get(u'gfx_panel',
                                                      u'stdfontsize'))
        self.set_monofontsize(self.monofontsize)
        self.set_stdfontsize(self.stdfontsize)

        self.monorows = strops.confopt_posint(cr.get(u'gfx_panel',
                                  u'monorows'), 8)
        self.monocols = strops.confopt_posint(cr.get(u'gfx_panel',
                                  u'monocols'), 32)
        self.curov = cr.get(u'gfx_panel', u'curov')

        if cr.has_option(u'gfx_panel', u'geometry'):
            self.set_geometry(unichr(unt4.US).join(cr.get(u'gfx_panel', u'geometry')))

        self.general_clearing()

        # try to load a list of riders
        try:
            rdb = riderdb.riderdb()
            rdb.load(metarace.default_file(u'riders.csv'))
            self.rmap = rdb.mkridermap()
        except Exception as e:
            # always an error - there must be startlist to continue
            self.log.error(u'Error loading from riders: '
                             + unicode(e))
        # try to load start line infos
        try:
            rlist = []
            with open(metarace.default_file(u'startlist.csv'),'rb') as f:
                cr = ucsv.UnicodeReader(f)
                for r in cr:
                    key = None
                    st = None
                    bib = u''
                    series = u''
                    name = u''
                    next = None
                    # load rider info
                    # start, no, series, name, cat
                    if len(r) > 0 and r[0] not in NOHDR: # time & no provided
                        st = tod.str2tod(r[0])
                        if len(r) > 1:  # got bib
                            bib = r[1]
                        if len(r) > 2:  # got series
                            series = r[2]
                        if len(r) > 3:  # got name
                            name = r[3]
                        if st is not None:
                            # enough data to add a starter
                            key = tod2key(st)
                            nr = [st, bib, series, name, next]
                            self.ridermap[key] = nr
                            rlist.append(key)
            # sort startlist and build list linkages
            curoft = tod2key(tod.tod(u'now'))
            self.currider = None
            rlist.sort()
            prev = None
            for r in rlist:
                if prev is not None:
                    self.ridermap[prev][4] = r  # prev -> next
                prev = r
                if self.currider is None and r > curoft:
                    self.currider = r
                    rvec  = self.ridermap[r]
                    stxt = tod.tod(r).meridian()
                    sno = rvec[1]
                    sname = rvec[3]
                    self.log.info(u'Setting first rider to: '
                          + u','.join([sno, sname]) + u' @ ' + stxt)
            # last link will be None
        except Exception as e:
            # always an error - there must be startlist to continue
            self.log.error(u'Error loading from startlist: '
                             + unicode(e))

    def draw_and_update(self, data=None):
        """Redraw in main loop, not in timeout."""
        if self.dirty:
            self.area_redraw()
            self.area.queue_draw()
            self.dirty = False
        return False

    def timeout(self, data=None):
        """Handle timeout."""

        # 1: Terminate?
        if not self.running:
            return False

        # 2: Process?
        try:
            self.process_timeout()
        except Exception as e:
            self.log.error(u'Timeout: ' + repr(e))

        # 3: Re-Schedule
        #glib.timeout_add(50, self.timeout)

        # 4: I/O Connection
        if not self.scb.connected():
            self.failcount += 1
            if self.failcount > self.failthresh:
                self.scb.set_portstr(portstr=self.remoteport,
                                     channel=self.remotechan,
                                     force=True)
                self.failcount = 0
            self.log.debug(u'Telegraph connection failed, count = '
                           + repr(self.failcount))
        else:
            self.failcount = 0

        # 4: Return True!!!
        #return False    # must return False
        return True

    def setbulb(self, ov, newstate=u'off'):
        """Write bulb state consistently."""
        if newstate == u'red':
            ov['redbulb'] = True
            ov['greenbulb'] = False
        elif newstate == u'green':
            ov['redbulb'] = False
            ov['greenbulb'] = True
        else:
            ov['redbulb'] = False
            ov['greenbulb'] = False

    def left_panel(self, cr, pr, h):
        """Draw the left panel poly."""
        pat = cairo.LinearGradient(0.0, h, 0.0, h+self.growh)
        cor = DARK_R
        cog = DARK_G
        cob = DARK_B
        pat.add_color_stop_rgb(0.0,scaleup(cor, 0.4),
                                    scaleup(cog, 0.4),
                                    scaleup(cob, 0.4))
        pat.add_color_stop_rgb(0.25,cor,cog,cob)
        pat.add_color_stop_rgb(0.85,0.8*cor,0.8*cog,0.8*cob)
        pat.add_color_stop_rgb(1.0,0.5*cor,0.5*cog,0.5*cob)
        cx = ARC_TO_BEZIER * self.growrad
        cr.new_path();
        cr.move_to (self.growll + self.growrad, h)
        cr.rel_line_to (self.growltw - self.growrad, 0.0)
        cr.rel_line_to (self.growlbw - self.growltw, self.growh)
        cr.rel_line_to (-self.growlbw + self.growrad, 0.0)
        cr.rel_curve_to (-cx, 0, -self.growrad, -cx,
                         -self.growrad, -self.growrad)
        cr.rel_line_to (0, -self.growh + 2 * self.growrad)
        cr.rel_curve_to (0.0, -cx, self.growrad - cx,
                        -self.growrad, self.growrad, -self.growrad)
        cr.close_path ()

        #roundedrec(c, 32.0, h, 400.0, self.growh, self.growrad, self.growrad)
        cr.set_source(pat)
        cr.fill()

    def title_pane(self, cr, pr, h=None):
        """Draw a title pane at h"""
        if h is None:
            h = self.safetop

        pat = cairo.LinearGradient(0.0, h, 0.0, h+self.titleh)
        #cor = TITLE_R
        #cog = TITLE_G
        #cob = TITLE_B
        cor = 0.3
        cog = 0.3
        cob = 0.3
        pat.add_color_stop_rgb(0.0,scaleup(cor, 0.4),
                                    scaleup(cog, 0.4),
                                    scaleup(cob, 0.4))
        pat.add_color_stop_rgb(0.10,cor,cog,cob)
        pat.add_color_stop_rgb(0.95,0.8*cor,0.8*cog,0.8*cob)
        pat.add_color_stop_rgb(1.0,0.5*cor,0.5*cog,0.5*cob)
        cx = ARC_TO_BEZIER * self.growrad
        cr.new_path();
        cr.move_to (self.saferight, h)
        cr.rel_curve_to(cx,0, self.growrad, cx,
                        self.growrad, self.growrad)
        cr.rel_line_to (0, self.titleh - 2.0 * self.growrad)
        cr.rel_curve_to(0,cx, -self.growrad+cx,self.growrad,
                        -self.growrad,self.growrad)
        cr.rel_line_to (self.safeleft-self.saferight, 0)
        cr.rel_curve_to(-cx,0, -self.growrad, -self.growrad+cx, 
                         -self.growrad,-self.growrad)
        cr.rel_line_to(0,2.0 * self.growrad - self.titleh) 
        cr.rel_curve_to(0,-cx, self.growrad - cx, -self.growrad,
                        self.growrad, -self.growrad) 
        cr.close_path ()

        cr.set_source(pat)
        cr.fill()


        return

        pat = cairo.LinearGradient(0.0, h, 0.0, h+1.95*self.growh)
        cor = TITLE_R
        cog = TITLE_G
        cob = TITLE_B
        pat.add_color_stop_rgb(0.0,scaleup(cor, 0.4),
                                    scaleup(cog, 0.4),
                                    scaleup(cob, 0.4))
        pat.add_color_stop_rgb(0.10,cor,cog,cob)
        pat.add_color_stop_rgb(0.92,0.8*cor,0.8*cog,0.8*cob)
        pat.add_color_stop_rgb(1.0,0.5*cor,0.5*cog,0.5*cob)

        cx = ARC_TO_BEZIER * self.growrad
        cr.new_path();
        cr.move_to (0, h)
        cr.line_to (self.pw, h)
        cr.line_to (self.pw, h+1.95*self.growh)
        cr.line_to (0, h+1.95*self.growh)
        cr.close_path ()
        cr.set_source(pat)
        cr.fill()

    def mid_panel(self, cr, pr, h):
        """Draw the mid panel poly."""
        pat = cairo.LinearGradient(0.0, h, 0.0, h+self.growh)
        cor = DARK_R
        cog = DARK_G
        cob = DARK_B
        #cor = LIGHT_R
        #cog = LIGHT_G
        #cob = LIGHT_B
        pat.add_color_stop_rgb(0.0,scaleup(cor, 0.4),
                                    scaleup(cog, 0.4),
                                    scaleup(cob, 0.4))
        pat.add_color_stop_rgb(0.25,cor,cog,cob)
        pat.add_color_stop_rgb(0.85,0.8*cor,0.8*cog,0.8*cob)
        pat.add_color_stop_rgb(1.0,0.5*cor,0.5*cog,0.5*cob)
        cr.new_path();
        cr.move_to (self.growmlt+2, h)
        cr.line_to (self.growmrt-2, h)
        cr.line_to (self.growmrb-2, h+self.growh)
        cr.line_to (self.growmlb+2, h+self.growh)
        cr.close_path ()

        #roundedrec(c, 32.0, h, 400.0, self.growh, self.growrad, self.growrad)
        cr.set_source(pat)
        cr.fill()
        pass

    def right_panel(self, cr, pr, h):
        """Draw the right panel poly."""
        pat = cairo.LinearGradient(0.0, h, 0.0, h+self.growh)
        cor = DARK_R
        cog = DARK_G
        cob = DARK_B
        pat.add_color_stop_rgb(0.0,scaleup(cor, 0.4),
                                    scaleup(cog, 0.4),
                                    scaleup(cob, 0.4))
        pat.add_color_stop_rgb(0.25,cor,cog,cob)
        pat.add_color_stop_rgb(0.85,0.8*cor,0.8*cog,0.8*cob)
        pat.add_color_stop_rgb(1.0,0.5*cor,0.5*cog,0.5*cob)
        cx = ARC_TO_BEZIER * self.growrad
        cr.new_path();
        cr.move_to (self.growrr - self.growrad, h)
        cr.rel_curve_to (cx, 0.0, self.growrad, cx,
                             self.growrad, self.growrad)
        cr.rel_line_to (0, self.growh - 2 * self.growrad)
        cr.rel_curve_to (0.0, cx, cx - self.growrad,
                            self.growrad, -self.growrad, self.growrad)
        cr.rel_line_to (-self.growrbw + self.growrad, 0.0)
        cr.rel_line_to (self.growrbw - self.growrtw, -self.growh)
        #cr.rel_line_to (self.growrbw - self.growrad, 0.0)
        #cr.rel_curve_to (cx, 0, self.growrad, cx,
                         #self.growrad, self.growrad)
        #cr.rel_curve_to (0.0, cx, -self.growrad + cx,
                        #self.growrad, -self.growrad, self.growrad)
        cr.close_path ()

        #roundedrec(c, 32.0, h, 400.0, self.growh, self.growrad, self.growrad)
        cr.set_source(pat)
        cr.fill()
        pass

    def process_timeout(self):
        """Process countdown, redraw display if required."""
        self.tcount += 1
        if self.curov == u'gfx' or self.doredraw:
            self.doredraw = False
            self.xferplaces()
            self.draw_and_update()
        return False	# superfluous

    def delayed_cursor(self):
        """Remove the mouse cursor from the text area."""
        pixmap = gtk.gdk.Pixmap(None, 1, 1, 1)
        color = gtk.gdk.Color()
        cursor = gtk.gdk.Cursor(pixmap, pixmap, color, color, 0, 0)
        self.area.get_window().set_cursor(cursor)
        if self.dofullscreen:
            self.window.fullscreen()
        return False

    def addrider(self, msgtxt=''):
        """Append rider to standings."""
        fvec = msgtxt.split(unichr(unt4.US))
        if len(fvec) > 4:
            rank = u''
            if fvec[0]:
                if u'.' in fvec[0]:
                    rank = fvec[0]
                else:
                    rank = fvec[0] + u'.'
            rno = fvec[1]
            rname = fvec[2]
            #rtime = tod.str2tod(fvec[4])
            rtime = fvec[4]
            tstr = u''
            #if rtime is not None:
            if rtime:
                tstr = rtime
            if True:
                # have a time -> is this leader?
                #if len(self.rows) == 0:
                    #self.leadertime = rtime
                    #tstr = rtime.rawtime(2)
                #else:
                    #if self.leadertime is not None:
                        #tstr = u'+' + (rtime - self.leadertime).rawtime(2)
                    #else:
                        #tstr = rtime.rawtime(2)	# fallback
                self.rows.append([rank, rno, rname, None, tstr])

    def xferplaces(self):
        self.gdata = {}
        rmax = len(self.rows)
        if rmax > 10:
            rmax = 10
        count = 0
        for r in self.rows:
            self.gdata[count] = [r[0],
                                 1,
                                 r[2],
                                 1,
                                 None,
                                 r[4],
                                 1]
            count += 1
            if count > rmax:
                break

    def finish_command(self, msgtxt=''):
        """Update finish line data from standard finish message."""
        fvec = msgtxt.split(unichr(unt4.US))
        if len(fvec) > 4:
            roll = True
            rank = fvec[0]
            if rank and rank.isdigit():
                rank = rank + u'.'
                roll = False
            bib = fvec[1]
            namestr = fvec[2]
            #if bib in self.rmap:
                #namestr = self.rmap[bib][u'namestr']
            elap = tod.str2tod(fvec[4])
            speedstr = u''
            if not roll:
                speedstr = elap.speedstr(2100)	# HARD DIST
            self.finishdat = [rank, bib, namestr, elap, speedstr, roll]
            if self.ovmode == u'finish':
                self.draw_and_update()

    def set_monofontsize(self, msgtxt=''):
        self.monofontsize = strops.confopt_float(msgtxt, self.monofontsize)
        fnsz = u' ' + unicode(self.monofontsize) + u'px'
        self.monofontdesc = pango.FontDescription(self.monofont + fnsz)

    def set_stdfontsize(self, msgtxt=''):
        self.stdfontsize = strops.confopt_float(msgtxt, self.stdfontsize)
        fnsz = u' ' + unicode(self.stdfontsize) + u'px'
        self.stdfontdesc = pango.FontDescription(self.stdfont + fnsz)

    def set_geometry(self, msgtxt=''):
        """Update geometry."""
        fvec = msgtxt.split(unichr(unt4.US))
        if len(fvec) == 6:
            # frame width / height
            self.pw = strops.confopt_float(fvec[0], self.pw)
            self.ph = strops.confopt_float(fvec[1], self.ph)

            # X/Y offsets -> moves whole frame in physical units
            self.xoft = strops.confopt_float(fvec[2], self.xoft)
            self.yoft = strops.confopt_float(fvec[3], self.yoft)

            # physical scale of virtual to physical after translate
            self.xscale = strops.confopt_float(fvec[4], self.xscale)
            self.yscale = strops.confopt_float(fvec[5], self.xscale)

            # define 4:3 graphic 'safe' regions
            self.safeleft = 0.10 * self.pw	# 10% EBU R 95-2008
            self.saferight = 0.90 * self.pw	# 90%
            self.safetop = 0.05 * self.ph	# 5%
            self.safebot = 0.95 * self.ph	# 95%
            self.safew = self.saferight - self.safeleft
            self.safeh = self.safebot - self.safetop

            # whole physical frame is divided in to 12 logical slots
            self.growof = self.safeh/12.0	# divide into 12 slots
					# 2+8lines

            # drawable are within slot is 90% of available height
            self.growh = self.growof * 0.9
            self.growrad = self.growof * 0.10	# rad plus gap
            self.growll = self.safeleft
            self.growrr = self.saferight

            # panel divisions for left mid right
            self.growltw = 2.0 * self.growh	# aim for 2*h
            self.growlbw = 1.8 * self.growh	# aim for 2*h
            self.growrtw = 3.8 * self.growh	# aim for 4*h
            self.growrbw = 4.0 * self.growh	# aim for 4*h
            self.decimalw = 2.83 * self.growh	# fudged for JHST decimal

            self.growmlt = self.growll + self.growltw + 0.25 # allow 1/4 gap
            self.growmlb = self.growll + self.growlbw + 0.25 # allow 1/4 gap
            self.growmrt = self.growrr - self.growrtw - 0.25
            self.growmrb = self.growrr - self.growrbw - 0.25

            # top panel offsets?
            self.growlogow = self.growrtw	# logo widths
            self.titleh = 2.0 * self.growh	# title pane height

    def positioned_text(self, msg):
        nr = u''
        if msg.yy in self.dbrows:
            nr = self.dbrows[msg.yy]
        sp = u''
        md = msg.text
        ep = u''
        if msg.xx > 0:
            sp = nr[0:msg.xx]
        edx = msg.xx + len(md)
        if edx < self.monocols:
            ep = nr[edx:]
        if msg.erl:	# space pad to EOL
            ep = u' ' * (len(md) - edx)
        self.dbrows[msg.yy] = strops.truncpad(sp + md + ep,
                                       self.monocols, elipsis=False)
        self.doredraw = True

    def gfx_loader(self, gfxobj):
        """Receive a graphic frame object."""
        if u'overlay' in gfxobj:
            nov = gfxobj[u'overlay']
            

    def msg_cb(self, msg, nick=None, chan=None):
        """Handle a public message from the channel."""
        if msg.erp or msg.header == '0040100096':
            self.dirty = True
            self.general_clearing()
            self.draw_and_update()
        elif msg.yy is not None:
            self.positioned_text(msg)
            #if self.curov == 1:
                #self.draw_and_update()
        elif msg.header != '':
            command = msg.header.lower()
            if command == u'title':
                self.set_subtitle(msg.text)
            #elif command == u'subtitle':
                #self.set_subtitle(msg.text)
            #elif command == u'gfxaddrow':
                #self.add_row(msg.text)
            #elif command == u'gfxobj':
                #self.gfx_loader(self.scb.rcv_obj(msg.text))
            #elif command == u'gfxclear':
                #self.clear_rows()
            elif command == u'startline':
                if msg.text in self.rmap:
                    self.onstart = msg.text
                else:
                    self.onstart = None
                self.dirty = True
            elif command == u'finish':
                self.dirty = True
                self.finish_command(msg.text)
            elif command == u'overlay':	# for remote control
                self.dirty = True
                self.set_overlay(msg.text)
            elif command == u'geometry': # reset panel geometry
                self.dirty = True
                self.set_geometry(msg.text)
                self.reinit_overlay()	# fix text layouts in the gfx ov
                self.draw_and_update()
            elif command == u'monofontsize': # update font size
                self.set_monofontsize(msg.text)
                self.draw_and_update()
            elif command == u'rider': # add rider row (irtt)
                self.dirty = True
                self.addrider(msg.text)
            elif command == u'stdfontsize': # update font size
                self.dirty = True
                self.set_stdfontsize(msg.text)
                self.reinit_overlay()	# fix text layouts in the gfx ov
                self.draw_and_update()
            #else:
                #self.log.info(u'Ignoring unknown command: ' + repr(command))
        #else:
            #self.log.info(u'Ignoring unknown message type.')
        return False	# idle added
 
    def remote_msg(self, msg):
        """Log a message to the uscbsrv."""
        self.log.debug(msg)
        self.scb.add_rider([msg], 'message')

    def set_overlay(self, newov=None):
        if newov is not None and newov in self.overlays:
            self.curov = newov
        else:
            self.curov = u'blank'
        self.draw_and_update()	# pull out?

    def key_event(self, widget, event):
        """Collect key events on main window."""
        if event.type == gtk.gdk.KEY_PRESS:
            self.dirty = True
            key = gtk.gdk.keyval_name(event.keyval) or 'None'
            key = key.lower()
            if key == KEY_START:
                self.ovmode = u'start'
                self.set_overlay(u'gfx')
            elif key == KEY_TITLE:
                ## override title?
                self.altsubtitle = u'24 Hour Road Race'
                self.ovmode = u'title'
                self.set_overlay(u'gfx')
            elif key == KEY_STANDINGS:
                self.ovmode = u'standings'
                self.xferplaces()
                self.set_overlay(u'align')
                #self.set_overlay(u'gfx')
            elif key == KEY_FINISH:
                self.ovmode = u'finish'
                self.set_overlay(u'gfx')
            elif key == KEY_CLEAR:
                # set overlay to blank
                self.ovmode = None
                self.set_overlay(u'0')
            return True	# 'handle' all keys

    def __init__(self):
        # logger and handler
        self.log = logging.getLogger()
        self.log.setLevel(logging.DEBUG)
        self.loghandler = logging.FileHandler(LOGFILE)
        self.loghandler.setLevel(logging.DEBUG)
        self.loghandler.setFormatter(logging.Formatter(
                       '%(asctime)s %(levelname)s:%(name)s: %(message)s'))
        self.log.addHandler(self.loghandler)
        self.log.debug('Init')

        # require one uscbsrv
        self.dirty = True
        self.scb = telegraph.telegraph()
        self.remoteport = None
        self.remotechan = None
        self.remoteuser = None

        self.started = False
        self.running = True
        self.doredraw = False
        self.tcount = 0
        self.failcount = 0
        self.failthresh = 450    # connect timeout ~45sec
        self.tod = tod.tod(u'now').truncate(0)
        self.nc = self.tod + tod.tod(u'1.22') # set interval a little off mark

        # variables
        self.title = u'2017 Delirium 24'	# current title string
        self.subtitle = u''	# current title string
        self.altsubtitle = u''	# current title string
        self.countdown = None
        self.riderstr = None
        self.onstart = None
        self.bulb = None
        self.currider = None
        self.ridermap = {}
        self.rmap = {}
        self.monorows = 8	# size of monospace text panel
        self.monocols = 32	# size of monospace text panel
        self.dbrows = {}	# prefomat text rows
        #self.grows = []
        self.gdata = { 
             #   no, showrow?, name, ?, ctrrighttxt, rghtrighttxt, running?
             0:[u'1.',1,u'Mikhail IGNATYEV (KAT)',1,None,u'2:28.24',1],
             1:[u'2.',1,u'Ian STANNARD (SKY)',1,None,u'+0.02',1],
             2:[u'3.',1,u'Valerio AGNOLI (AST)',1,None,u'+0.06',1],
             3:[u'4.',1,u'Nathan EARLE (SKY)',1,None,u'+0.12',1],
             4:[u'5.',1,u'Boy VAN POPPEL (TFR)',1,None,u'+0.14',1],
             5:[u'6.',1,u'Calvin WATSON (TFR)',1,None,u'+0.49',1],
             6:[u'7.',1,u'Adam HANSEN (LTB)',1,None,u'+1.33',1],
             7:[u'8.',1,u'Steve MORABITO (BMC)',1,None,u'+2.71',1],
             8:[u'9.',1,u'Christopher JUUL JENSEN (TCS)',1,None,u'+10.22',1],
             9:[u'10.',1,u'Philip DEIGNAN (SKY)',1,None,u'+22.01',1],
             #8:[u'221',1,u'Christopher JUUL JENSEN (TCS)',1,None,u'2:13.00',0],
             #8:[u'221',1,u'Christopher JUUL JENSEN (TCS)',1,None,u'2:14.27',1],
             #8:[u'221',1,u'Christopher JUUL JENSEN (TCS)',1,u'DEN',None,1],
             #9:[None,1,u'(2.)  \t56.7 km/h',0,None,u'+0.51',1],
        }	# graphical animation result rows
        self.leadertime = None
        self.rows = []		# graphical rows
        self.curov = 'align'		# start on blank screen - the 'none' overlay
        self.ovmode = None	# graphical overlay mode
        self.finishdat = []
        self.overlays = { u'align': {		# alignment screen
                           u'patch':cairo.ImageSurface.create_from_png(
                                metarace.default_file('patch.png'))
                          },
                          u'0': {		# SCB Clock
                          },
                          u'1': {		# SCB Preformat Text
                          },
                          u'2': {		# SCB Image 1
                           u'image':cairo.ImageSurface.create_from_png(
                                metarace.default_file('overlay_image_2.png'))
                          },
                          u'3': {		# SCB Image 2
                           u'image':cairo.ImageSurface.create_from_png(
                                metarace.default_file('overlay_image_3.png'))
                          },
                          u'gfx': {
                           #u'mainlogo':rsvg.Handle(metarace.default_file(u'gfxmainlogo.svg')),
                           #u'sublogo':rsvg.Handle(metarace.default_file(u'gfxsublogo.svg')),
                           u'mainlogo':None,
                           u'sublogo':None,
                          }
                        }

        # Geometry
        self.width = float(DEFAULT_WIDTH)	# device w
        self.height = float(DEFAULT_HEIGHT)	# device h
        self.pw = self.width			# panel width
        self.ph = self.height			# panel height
        self.xscale = 1.0			# panel pre-scale x
        self.yscale = 1.0			# panel pre-scale y
        self.xoft = 0.0				# panel pre-translate x
        self.yoft = 0.0				# panel pre-translate y
        self.stdfontoffset = -4			# font vertical oft
        self.stdfontsize = 20			# font size in panel units
        self.monofontoffset = -4		# font vertical oft
        self.monofontsize = 34			# font size in panel units
        self.monofont = MONOFONT
        self.monofontdesc = None
        self.stdfont = STDFONT
        self.stdfontdesc = None
        self.dofullscreen = False
        ## TODO: rotation

        # Prepare UI
        self.window = gtk.Window()
        self.window.set_title('Metarace LoGFX')
        self.window.connect('destroy', self.window_destroy_cb)
        self.window.connect('key-press-event', self.key_event)
        self.area_src = None	# off-screen drawable
        self.area = gtk.DrawingArea()
        self.area.connect('configure_event', self.area_configure_event_cb)
        self.area.connect('expose_event', self.area_expose_event_cb)
        self.area.set_size_request(DEFAULT_WIDTH, DEFAULT_HEIGHT)
        self.area.show()
        self.window.add(self.area)
        self.log.debug(u'Starting clock intervals at: ' + self.nc.rawtime(3))
        glib.timeout_add(1000, self.timeout)
        glib.timeout_add_seconds(5, self.delayed_cursor)

def main():
    """Run the application."""
    metarace.init()
    app = gfx_panel()
    app.loadconfig()
    app.show()
    app.start()
    try:
        gtk.main()
    except:
        app.shutdown()
        raise

if __name__ == '__main__':
    main()

