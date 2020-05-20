def open_social_media(option):
    """Opens a new tab in user's browser with our research group social medias"""
    import webbrowser
    if option == 'facebook':
        webbrowser.open_new_tab('https://www.facebook.com/GrupoCNPqDocsDigitais/')
    elif option == 'blogger':
        webbrowser.open_new_tab('http://documentosarquivisticosdigitais.blogspot.com/')

class ItemHasChildren(BaseException):
    """ Custom Exception """

class NotAbleToDeleteDB(BaseException):
    """ Custom Exception """

class NotAbleToWriteFile(BaseException):
    """ Custom Exception """