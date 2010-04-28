#!/usr/bin/env python
# PyWebShot - create webpage thumbnails. Originally based on 
# http://burtonini.com/computing/screenshot-tng.py
# Ben Dowling - http://www.coderholic.com

import os
import sys
import gtk
import gtk.gdk as gdk
import gtkmozembed
import urlparse
from optparse import OptionParser

class PyWebShot:
	def __init__(self, urls, screen, thumbnail, delay, outfile):
		self.parent = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.parent.set_border_width(10)
		self.urls = urls
		self.delay = delay

		# Get resoltion information
		(x,y) = screen.split('x')
		x = int(x)
		y = int(y)
		(t_x, t_y) = thumbnail.split('x')
		t_x = int(t_x)
		t_y = int(t_y)
		
		# Calculate the x scale factor
		scale_x = float(t_x) / x
		scale_y = float(t_y) / y
		
		self.t_x = t_x
		self.t_y = t_y
		self.scale = scale_x
		
		self.widget = gtkmozembed.MozEmbed()
		self.widget.set_size_request(x + 18, y)
		
		# Connect signal
		self.widget.connect("net_stop", self.on_net_stop)
		if outfile:
			(self.outfile_base, ignore) = outfile.split('.png')
		else:
			self.outfile_base = None
		self.parent.add(self.widget)
		self.url_num = 0
		self.load_next_url()
		self.parent.show_all()

	def load_next_url(self):
		if self.url_num > len(self.urls) - 1:
			gtk.main_quit()
			return
		self.current_url = self.urls[self.url_num]
		self.countdown = self.delay
		print "Loading " + self.current_url + "...", 
		self.url_num += 1
		self.widget.load_url(self.current_url)
		
	def on_net_stop(self, data = None):
		if self.delay > 0: gtk.timeout_add(1000,self.do_countdown,self)
		else: self.do_countdown()

	def do_countdown(self, data = None):
		self.countdown -= 1
		if(self.countdown > 0):
			return True
		else:
			self.screenshot()
			self.load_next_url()
			return False

	def screenshot(self, data = None):
		window = self.widget.window
		(x,y,width,height,depth) = window.get_geometry()

		width -= 16

		pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,width,height)
		pixbuf.get_from_drawable(window,self.widget.get_colormap(),0,0,0,0,width,height)
		thumbnail = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,self.t_x,self.t_y)
		pixbuf.scale(thumbnail, 0, 0, self.t_x, self.t_y, 0, 0, self.scale, self.scale, gdk.INTERP_HYPER)
		if self.outfile_base:
			if len(self.urls) == 1:
				filename = "%s.png" % (self.outfile_base)
			else:
				filename = "%s-%d.png" % (self.outfile_base, self.url_num)
		else:
			parts = urlparse.urlsplit(self.current_url)
			filename = parts.netloc + parts.path.replace('/', '.') + ".png"
		thumbnail.save(filename,"png")
		print "saved as " + filename
		return True
		
def __windowExit(widget, data=None):
	gtk.main_quit()
	
if __name__ == "__main__":
	usage = "usage: %prog [options] url1 [url2 ... urlN]"
	parser = OptionParser(usage=usage)
	parser = OptionParser()
	parser.add_option('-s', '--screen', action='store', type='string', help='Screen resolution at which to capture the webpage (default %default)', default="1024x769")
	parser.add_option('-t', '--thumbnail', action='store', type='string', help='Thumbnail resolution (default %default)', default="350x200")
	parser.add_option('-d', '--delay', action='store', type='int', help='Delay in seconds to wait after page load before taking the screenshot (default %default)', default=0)
	parser.add_option('-f', '--filename', action='store', type='string', help='PNG output filename with .png extension, otherwise default is based on url name and given a .png extension')
	(options, args) = parser.parse_args()
	if len(args) == 0:
		parser.error('No URL specified')
	
	window = PyWebShot(urls=args, screen=options.screen, thumbnail=options.thumbnail, delay=options.delay, outfile=options.filename)
	window.parent.connect("destroy", __windowExit)
	gtk.main()
