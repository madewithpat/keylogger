import keylogger

cs = keylogger.ConsoleSink()
klog = keylogger.KeyLogger(sink=cs)
klog.start()

