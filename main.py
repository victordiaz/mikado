import mikado

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
