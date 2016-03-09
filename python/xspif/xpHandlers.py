#-----------------------------------------------------------------------
# Vincent Goudard and R�my Muller                                07/2003
# xspif.xpHandlers.py
# 
# Implement xmlproc's ErrorHandler Interface
#-----------------------------------------------------------------------


from xml.parsers.xmlproc.xmlapp import ErrorHandler


class BadXspifPluginErrorHandler(ErrorHandler):
    def warning(self, msg):
        print "XSPIF Warning: ", msg

    def error(self, msg):
        print "XSPIF Error: ", msg

    def fatal(self, msg):
        print "XSPIF Fatal error: ", msg
