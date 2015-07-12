import os, cookielib

class Cookies:
    """
    Class to simplify cookie jar management.
    """

    inst = None

    @staticmethod
    def cookies():
        if not Cookies.inst:
            Cookies.inst = Cookies()
        return Cookies.inst

    @staticmethod
    def getCookieJar():
        cookies = Cookies.cookies()
        cookie_file = cookies.getCookieFile()
        if os.path.isfile(cookie_file): 
            return cookies.loadCookieJar()
        return cookies.createCookieJar()

    @staticmethod
    def saveCookieJar(jar):
        cookies = Cookies.cookies()
        cookie_file = cookies.getCookieFile()
        #if not os.path.isfile(cookie_file):
        #    cookielib.LWPCookieJar(cookie_file)

        jar.save(filename=cookie_file, ignore_discard=True)
        return None


    def getCookieFile(self):
        try:
            import xbmc, xbmcaddon
            base = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile'))
        except:
            base = os.getcwd()
        return os.path.join(base, 'cookies.lwp')


    def createCookieJar(self):
        """
        Create the cookie jar file. Do not use this; instead, call getCookieJar,
        which will create the cookie jar if it doesn't already exist
        """
        cookie_file = self.getCookieFile()
        return cookielib.LWPCookieJar(cookie_file)


    def loadCookieJar(self):
        """
        Load teh cookie jar file. Do not use this; instead, call getCookieJar,
        which will load the cookie jar if it already exists.
        """
        jar = cookielib.LWPCookieJar()
        cookie_file = self.getCookieFile()
        jar.load(cookie_file,ignore_discard=True)
        return jar
