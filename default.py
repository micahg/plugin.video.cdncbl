import providerfactory
import xbmc, xbmcplugin, xbmcgui, xbmcaddon, os, urllib, urlparse

__settings__ = xbmcaddon.Addon(id='plugin.video.cdncbl')
__language__ = __settings__.getLocalizedString


def getAuthCredentials():
    username = __settings__.getSetting("username")
    if len(username) == 0:
        dialog = xbmcgui.Dialog()
        dialog.ok(__language__(30000), __language__(30001))
        xbmcplugin.endOfDirectory(handle = int(sys.argv[1]),
                                  succeeded=False)
        return None

    # get the password
    password = __settings__.getSetting("password")
    if len(password) == 0:
        dialog = xbmcgui.Dialog()
        dialog.ok(__language__(30002), __language__(30003))
        xbmcplugin.endOfDirectory(handle = int(sys.argv[1]),
                                  succeeded=False)
        return None

    mso = __settings__.getSetting("mso")

    return { 'u' : username, 'p' : password, 'm' : mso }

def createMainMenu():
    """
    Create the main menu
    """
    pf = providerfactory.ProviderFactory()
    providers = pf.getProviderNames()

    for provider in providers.keys():
        values = { 'menu' : 'provider',
                   'provider' : provider,
                   'name' : providers[provider] }

        chan = xbmcgui.ListItem(values['name'])
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
                                    url=sys.argv[0] + "?" + urllib.urlencode(values),
                                    listitem=chan,
                                    isFolder=True)


    # signal the end of the directory
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def createProviderMenu(values):
    """
    Create a menu for a provider. Show what they have on offer. For now its just
    live streams
    """

    creds = getAuthCredentials()

    pid = values['provider'][0]
    pf = providerfactory.ProviderFactory()
    provider = pf.getProviders()[pid]
    categories = provider.getCategories()
    provider.checkMSOs()

    provider.authorize(creds['u'], creds['p'], creds['m'])

    if 'live' in categories:
        values = { 'menu' : 'live', 'provider' : pid }
        live = xbmcgui.ListItem(__language__(30010))
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
                                    url=sys.argv[0] + "?" + urllib.urlencode(values),
                                    listitem=live,
                                    isFolder=True)


    # signal the end of the directory
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def createLiveMenu(values):
    pid = values['provider'][0]
    pf = providerfactory.ProviderFactory()
    provider = pf.getProviders()[pid]


    channels = provider.getChannels()
    print channels
    for channel in channels:
        values = { 'menu' : 'channel', 'provider' : pid,
                   'name' : channel['name'], 'id' : channel['id'],
                   'abbr' : channel['abbr'] }
        live = xbmcgui.ListItem(values['name'])
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
                                    url=sys.argv[0] + "?" + urllib.urlencode(values),
                                    listitem=live,
                                    isFolder=False)

    # signal the end of the directory
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def playChannel(values):
    print values
    pid = values['provider'][0]
    pf = providerfactory.ProviderFactory()
    provider = pf.getProviders()[pid]

    stream = provider.getChannel(values['id'][0], values['abbr'][0])
    if not stream:
        dialog = xbmcgui.Dialog()
        dialog.ok(__language__(30004), __language__(30005))
    else:
        name = values['name'][0]
        li = xbmcgui.ListItem(name)
        li.setInfo( type="Video", infoLabels={"Title" : name})
        p = xbmc.Player()
        p.play(stream, li)

    # signal the end of the directory
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


if len(sys.argv[2]) == 0:

    # create the data folder if it doesn't exist
    data_path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile'))
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    # show the main menu
    createMainMenu()
else:
    values = urlparse.parse_qs(sys.argv[2][1:])
    if values['menu'][0] == 'provider':
        createProviderMenu(values)
    elif values['menu'][0] == 'live':
        createLiveMenu(values)
    elif values['menu'][0] == 'channel':
        playChannel(values)

