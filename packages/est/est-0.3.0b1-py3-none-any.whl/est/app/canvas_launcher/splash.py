from silx.gui import qt
from est.gui import icons


def splash_screen():
    """

    :return: splash screen for orange-canvas
    :rtype: tuple(QPixmap, QRect),

    note: QRect is used by orange to define a mask to display the message.
          In our case we overwrite the QSplashScreen so we don't need this.
    """
    pixmap = icons.getQPixmap("est")
    return pixmap, qt.QRect(0, 0, 400, 400)


def getIcon():
    """

    :return: application icon
    :rtype: QIcon
    """
    pixmap = icons.getQPixmap("est")
    return qt.QIcon(pixmap)
