PyWebShot
=========

Automatically generate thumbnails for 1 or more websites from the command line. Requires the python-gtkmozembed package.

Ben Dowling - http://www.coderholic.com

Usage
-----
pywebshot.py [options] url1 [url2 ... urlN]

Options:
  -h, --help            show this help message and exit
  -s SCREEN, --screen=SCREEN
                        Screen resolution at which to capture the webpage
                        (default 1024x769)
  -t THUMBNAIL, --thumbnail=THUMBNAIL
                        Thumbnail resolution (default 350x200)
  -d DELAY, --delay=DELAY
                        Delay in seconds to wait after page load before taking
                        the screenshot (default 0)
  -f FILENAME, --filename=FILENAME
                        PNG output filename with .png extension, otherwise
                        default is based on url name and given a .png
                        extension

Examples
--------
pywebshot.py google.com
pywebshot.py google.com yahoo.com
cat urls.txt | xargs ./pywebshot.py
pywebshot.py page_with_delayed_content.com -d10

# single url will output to /tmp/shot.png
pywebshot.py -f /tmp/shot.png google.com
# multiple url will output to /tmp/shot-1.png and /tmp/shot-2.png
pywebshot.py -f /tmp/shot.png google.com yahoo.com
