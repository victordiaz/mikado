#############################################################################
## 
## Victor Diaz Barrales 
## 
## 
##
#############################################################################

import sys

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import * 


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



class MBrowser(QWebPage): 
  def __init__(self):
    super(MBrowser, self).__init__()

  def userAgentForUrl(self, url): 
    UA = "Potato/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"
    UA = "Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3" 

    return UA
    
  def javaScriptAlert(self, frame, message):
     """Override default JavaScript alert popup and print results
     """
     common.logger.debug('Alert:' + message)

  def javaScriptConfirm(self, frame, message):
     """Override default JavaScript confirm popup and print results
     """
     common.logger.debug('Confirm:' + message)
     return self.confirm

  def javaScriptPrompt(self, frame, message, default):
        """Override default JavaScript prompt popup and print results
        """
        common.logger.debug('Prompt:%s%s' % (message, default))

  def javaScriptConsoleMessage(self, message, line_number, source_id):
        """Print JavaScript console messages
        """
        common.logger.debug('Console:%s%s%s' % (message, line_number, source_id))

  def shouldInterruptJavaScript(self):
        """Disable javascript interruption dialog box
        """
        return True

class MyWebView(QWebView): 

    def __init__(self):
        super(MyWebView, self).__init__() 
        #self.setContentsMargins(12, 12, 12, 12)

class Miniwini(QWidget):

    def __init__(self, url):
        super(Miniwini, self).__init__() 
        
        self.activated = False 
        self.createActions()
        self.createTrayIcon()
        self.trayIcon.activated.connect(self.iconActivated) 

        self.setIcon()
        
        self.trayIcon.show() 
        tray_x = self.trayIcon.geometry().x()
        tray_y = self.trayIcon.geometry().y()
        tray_w = self.trayIcon.geometry().width()

        w = QApplication.desktop().width()
        h = QApplication.desktop().height()        

        self.setGeometry(tray_x, abs(h + tray_y), 370, 480)


        self.webView = MyWebView()
        #self.webView.setStyleSheet("background-color: black; padding: 12px; margin:12px");
        
        page = MBrowser()
        self.webView.setPage(page)
        #self.webView.setStyleSheet("background-color: #222; padding: 12px; margin:12px");


        #self.webView.settings().setAttribute(QWebSettings.WebAttribute.DeveloperExtrasEnabled, True)
        
        self.webView.settings().setUserStyleSheetUrl('./qq.css')
        
        self.webView.load(QUrl(url))
        #self.webView.load(QUrl("http://learnwebtutorials.com/example/html5/slider-control.html"))
        
        page.currentFrame().documentElement().setInnerXml("<html><body style =background-color: #bbb; > hola <input type = button value = 'lalala'> </input> </body> </html>")
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5) 
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        

        image = QImage()
        image.load("arrow.png")
        label = QLabel() 
        label.setPixmap(QPixmap.fromImage(image))
        label.setContentsMargins(0, 0, 0, 0) 
        label.setStyleSheet("padding: 0px; margin:0px");
        #self.layout.addWidget(self.webView)

                
        self.olayout = MyLayout(self) 
        self.olayout.setContentsMargins(0, 0, 12, 12) 
        self.olayout.addWidget(self.webView)

        self.layout.addWidget(label)
        self.layout.addLayout(self.olayout)
        #print self.webView.spacing()

        #palette = self.webView.palette()
        # palette.setBrush(QPalette.Base, Qt.transparent)
        # self.webView.page().setPalette(palette)
        #self.webView.setAttribute(Qt.WA_OpaquePaintEvent, False)
        #self.connect(self.webView, SIGNAL("titleChanged(const QString&)"), 
        #             self.setWindowTitle)

        #cambiar esto de sitio 
        inspect = QWebInspector()
        inspect.setPage(self.webView.page())
        inspect.show()


        #self.resize(350, 480)

    def createActions(self):
        self.minimizeAction = QAction("Mi&nimize", self,
                triggered=self.hide)

        self.maximizeAction = QAction("Ma&ximize", self,
                triggered=self.showMaximized)

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


    def setIcon(self):
        icon = QIcon('stone.png') 
        #icon = QWebSettings.iconForUrl("http://www.meneame.net")
        #icon = self.webView.icon()

        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)

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
 
  
    	

if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('stone.png'))
    app.setApplicationName("hola") 

	# init webview 
    w = Miniwini("http://www.gmail.com")
    w.setAttribute(Qt.WA_TranslucentBackground, True)
    w.setWindowFlags(Qt.FramelessWindowHint)
	
	# init webview 
    w2 = Miniwini("http://www.twitter.com")
    w2.setAttribute(Qt.WA_TranslucentBackground, True)
    w2.setWindowFlags(Qt.FramelessWindowHint)


	# init webview 
    w3 = Miniwini("http://127.0.0.1:4000/qq.html")
    w3.setAttribute(Qt.WA_TranslucentBackground, True)
    w3.setWindowFlags(Qt.FramelessWindowHint)

    menubar = QMenuBar() 
    menubar.setWindowTitle("Miniwini")


	#systray 
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "Systray",
                "I couldn't detect any system tray on this system.")
        sys.exit(1)

    QApplication.setQuitOnLastWindowClosed(False)
    

    sys.exit(app.exec_())
