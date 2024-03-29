#!/usr/bin/python
# Filename: mikado.py


#############################################################################
## 
## Victor Diaz Barrales 
## 
## 
##
#############################################################################


import os, sys

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import * 
import logging

logging.basicConfig(level=logging.DEBUG)



class MyLayout(QVBoxLayout): 
   def __init__(self, url):
        super(MyLayout, self).__init__() 
        
   	   
   def paintEvent(self, event):

       QWidget.paintEvent(self, event)
       print "hola"

       p = QPainter(self)
       #p.fillRect(event.rect(), Qt.transparent)
       p.setPen(Qt.NoPen)
       #p.setPen(QPen(Qt.black, 2, Qt.DashDotLine, Qt.RoundCap));

       p.setBrush(QColor(249, 247, 96))  
       p.setOpacity(0.8)
       p.drawRoundedRect(self.rect(), 8, 8)
    
       p.end()


class ConsolePrinter(QObject):
    def __init__(self, parent=None):
        super(ConsolePrinter, self).__init__(parent)

    @Slot(str)
    def text(self, message):
        print message


class MBrowser(QWebPage): 
  def __init__(self):
    super(MBrowser, self).__init__()
    QWebSettings.globalSettings().setAttribute(QWebSettings.PluginsEnabled, True) 
    QWebSettings.globalSettings().setAttribute(QWebSettings.OfflineStorageDatabaseEnabled, True)
    QWebSettings.globalSettings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True) 
    QWebSettings.globalSettings().setAttribute(QWebSettings.JavascriptCanAccessClipboard, True)
    
    #"""Captures url as an image to the file specified"""
    #self.mainFrame().setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)
    #self.mainFrame().setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)

  #def userAgentForUrl(self, url): 
  #  UA = "Potato/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"
  #  UA = "Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3" 
 #
 #   return UA 
    

  def javaScriptAlert(self, frame, message):
     """Override default JavaScript alert popup and print results
     """
     logging.debug('Alert:' + message)

  def javaScriptConfirm(self, frame, message):
     """Override default JavaScript confirm popup and print results
     """
     logging.debug('Confirm:' + message)
     return self.confirm

  def javaScriptPrompt(self, frame, message, default):
        """Override default JavaScript prompt popup and print results
        """
        logging.debug('Prompt:%s%s' % (message, default))

  def javaScriptConsoleMessage(self, message, line_number, source_id):
        """Print JavaScript console messages
        """
        logging.debug('Console:%s%s%s' % (message, line_number, source_id))

  def shouldInterruptJavaScript(self):
        """Disable javascript interruption dialog box
        """
        return True

class MyWebView(QWebView): 

    def __init__(self):
        super(MyWebView, self).__init__() 
        self.setContentsMargins(12, 12, 12, 12)

        self.saw_initial_layout = False
        self.saw_document_complete = False


class Miniwini(QWidget):

    def __init__(self, conf):
        super(Miniwini, self).__init__() 
        self.setWindowFlags(Qt.Tool)
        self.activated = False 
        self.createActions()
        shortcut = QShortcut(QKeySequence(self.tr("Alt+M", "File|Open")),self) 
        QObject.connect(shortcut, SIGNAL('activated()'), self.printqq)
            
        shortcut2 = QShortcut(QKeySequence(self.tr("Alt+B", "File|Open")),self) 
        QObject.connect(shortcut2, SIGNAL('activated()'), self.doCapture)
                       
        if (conf['docked'] == "yes"): 
          self.createTrayIcon()
          self.trayIcon.activated.connect(self.iconActivated) 
        
          self.setIcon(conf['icon'])
        
          self.trayIcon.show() 
          tray_x = self.trayIcon.geometry().x()
          tray_y = self.trayIcon.geometry().y()
          tray_w = self.trayIcon.geometry().width()

          desktop_w = QApplication.desktop().width()
          desktop_h = QApplication.desktop().height()   
          
          self.x = tray_x
          self.y = abs(desktop_h + tray_y)
          self.w = 370
          self.h = 480
   
        if (conf['absoluteposition'] == "yes"): 
          self.x = int(conf['x'])
          self.y = int(conf['y'])
          self.w = int(conf['w'])
          self.h = int(conf['h'])
       
        print self.x, self.y, self.w, self.h 
        self.setGeometry(self.x, self.y, self.w, self.h)
     
        self.webView = MyWebView() 

        #self.webView.settings().setAttribute(QWebSettings.WebAttribute.DeveloperExtrasEnabled, True)
        #self.webView.setAttribute(Qt.WA_TransparentForMouseEvents, True); 

        #self.webView.setStyleSheet("background-color: black; padding: 12px; margin:12px");
        
        self.page = MBrowser()
        self.webView.setPage(self.page) 
        
        path = os.getcwd() + os.sep + 'qq.css'
        print path
        self.webView.settings().setUserStyleSheetUrl(QUrl.fromLocalFile(path))
       
             
        self.webView.load(QUrl(conf['url']))
        
        self.page.currentFrame().documentElement().setInnerXml("<html><body style =background-color: #bbb; > hola <input type = button onclick = 'window.alert()' value = 'lalala'> </input> </body> </html>")
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0) 
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        
        if (conf['docked'] == "yes" and conf['fullscreen'] == "no"): 
          image = QImage()
          image.load("arrow.png")
          label = QLabel() 
          label.setPixmap(QPixmap.fromImage(image))
          label.setContentsMargins(0, 0, 0, 0) 
          label.setStyleSheet("padding: 0px; margin:0px");
          #self.layout.addWidget(self.webView)
          
          #self.olayout = MyLayout(self) 
          #self.olayout.setContentsMargins(0, 0, 12, 12) 
          #self.olayout.addWidget(self.webView)

          self.layout.addWidget(label)
        
        
        self.layout.addWidget(self.webView)
        #print self.webView.spacing()
        
        if (conf['border'] == "no"): 
        	print "hola"
       		self.setAttribute(Qt.WA_TranslucentBackground, True)
        	self.setWindowFlags(Qt.FramelessWindowHint)

        if (conf['transparency'] == "yes"):
          print "hola2" 
          palette = self.webView.palette()
          palette.setBrush(QPalette.Base, Qt.transparent)
          self.webView.page().setPalette(palette)
          self.webView.setAttribute(Qt.WA_OpaquePaintEvent, False)
          #self.connect(self.webView, SIGNAL("titleChanged(const QString&)"), 
          #             self.setWindowTitle)
          
   
        #cambiar esto de sitio 
        inspect = QWebInspector()
        inspect.setPage(self.webView.page())
        inspect.show()
        
        if (conf['docked'] == "no"): 
          self.show()

        #self.resize(350, 480) 
        if (conf['fullscreen'] == "yes"): 
          self.showFullScreen()
   
        
        self.frame = self.webView.page().mainFrame()
        printer = ConsolePrinter()
    
        self.frame.addToJavaScriptWindowObject('printer', printer)
        self.frame.evaluateJavaScript("alert('Hello');")
        self.frame.evaluateJavaScript("printer.text('Goooooooooo!');") 
        
  
        printer = QPrinter()
        printer.setPageSize(QPrinter.A4)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName("qq.pdf") 
        self.webView.print_(printer)
       
        self.webView.loadFinished.connect(self.loadFinishedSlot)
        self.page.mainFrame().initialLayoutCompleted.connect(self.initialLayoutSlot)
        
    def loadFinishedSlot(self):
      logging.debug("loadFinished") 
      self.loadUserScript()
      #self.saw_document_complete = True 
      #print "qqqqqqqqqqqqq"
      #if self.saw_initial_layout and self.saw_document_complete:
      #  self.doCapture()

    def initialLayoutSlot(self):
      logging.debug("initialLayout") 
      #self.saw_initial_layout = True
      #if self.saw_initial_layout and self.saw_document_complete:
      #  self.doCapture()
     
    def loadUserScript(self): 
        try: 
      	  dir = os.getcwd() + "/" + "qq.js" 
     	  f = open (dir,"r")
     	  #Read whole file into data 
     	  data = f.read() 
     	  print data
     	  #Close the file
     	  f.close()
     	  self.frame.evaluateJavaScript(data) 
     	except:
     	  print "User script cannot be loaded"
   
    
    def doCapture(self):
        self.page.setViewportSize(self.page.mainFrame().contentsSize())
        img = QImage(self.page.viewportSize(), QImage.Format_ARGB32)
        painter = QPainter(img)
        self.page.mainFrame().render(painter)
        painter.end()
        img.save("qq2.png")
        #QCoreApplication.instance().quit()


    def printqq(self): 
      print "qq"
      self.webView.reload()

    def createActions(self):
        self.minimizeAction = QAction("Mi&nimize", self,  shortcut="Alt+B", 
                triggered=self.printqq)

        self.maximizeAction = QAction("Ma&ximize", self, shortcut="Alt+M", 
                triggered=self.doCapture)

        self.restoreAction = QAction("&Restore", self,
                triggered=self.showNormal)

        self.quitAction = QAction("&Quit", self,
                triggered=qApp.quit)

    def createTrayIcon(self):
         #self.trayIconMenu = QMenu(self)
         #self.trayIconMenu.addAction(self.minimizeAction)
         #self.trayIconMenu.addAction(self.maximizeAction)
         #self.trayIconMenu.addAction(self.restoreAction)
         #self.trayIconMenu.addSeparator()
         #self.trayIconMenu.addAction(self.quitAction)

         self.trayIcon = QSystemTrayIcon(self)
         #self.trayIcon.setContextMenu(self.trayIconMenu)


    def setIcon(self, icon):
        t_icon = QIcon(icon) 
        #icon = QWebSettings.iconForUrl("http://www.meneame.net")
        #icon = self.webView.icon()

        self.trayIcon.setIcon(t_icon)
        self.setWindowIcon(t_icon)

        self.trayIcon.setToolTip("qq")
        
   
    def iconActivated(self, reason): 
    
    	if (self.activated == False): 
    		self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
    		self.show() 
    		
    	else: 
    		self.hide(); 
        
        self.activated = not self.activated
        
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            print reason
            #self.iconComboBox.setCurrentIndex(
            #        (self.iconComboBox.currentIndex() + 1)
            #        % self.iconComboBox.count())
        elif reason == QSystemTrayIcon.MiddleClick:
            self.showMessage()
 
version = '0.1'
# End of mikado.py
  
    	

if __name__ == "__main__":
    import ConfigParser
    import io
    
   
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('stone.png'))
    app.setApplicationName("hola") 

	
	#read config  
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read('settings.conf')
    
    q = []
    
    for section in config.sections(): 
        conf = {}
        for m in config.items(section):
            conf[m[0]] = m[1]
        print conf
        w = Miniwini(conf)
        q.append(w)

  	# init webview 
    #conf = {'url': 'http://www.gmail.com', 'icon': 'stone.png', 'border': True, 'transparency': False}
    #w = Miniwini(conf)
 
	# init webview 
    #conf = {'url': 'http://www.twitter.com', 'icon': 'arrow.png', 'border': True, 'transparency': False}
    #w2 = Miniwini(conf)
  
	# init webview 
    #conf = {'url': "http://127.0.0.1:4000/qq.html", 'icon': 'stone.png', 'border': False, 'transparency': True}
    #w3 = Miniwini(conf)

	# init webview 
    #conf = {'url': "http://127.0.0.1:8081/static/livecoding/index.html#fullscreen", 'icon': 'stone.png', 'border': False, 'transparency': False}
    #w5 = Miniwini(conf)

    menubar = QMenuBar() 
    menubar.setWindowTitle("Miniwini")




	#systray 
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "Systray",
                "I couldn't detect any system tray on this system.")
        sys.exit(1)

    QApplication.setQuitOnLastWindowClosed(False)
    

    sys.exit(app.exec_())  
