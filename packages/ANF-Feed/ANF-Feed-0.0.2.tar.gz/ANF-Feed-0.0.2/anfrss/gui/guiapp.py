'''
GUI Module for ANF Feed Reader
##############################

The run() - Function is the main function.
It is also imported by the __init__ so
it can be used by the __main__ of the
package.

This package is licensed under:
 -- GNU General Public License v3.0 --

For more informations, reading the License,
contributing and else you may visit
the Github Repository:

 --> https://github.com/m1ghtfr3e/ANF-Feed-Reader

 Containing classes:
    - :class: ANFApp
    - :class: ArticleWidget
    - :class: TitleWidget
'''

import sys
from pathlib import Path
from PyQt5.QtWidgets import (QApplication,
                             QMainWindow,
                             QPushButton,
                             QWidget,
                             QListWidget,
                             QVBoxLayout,
                             QLabel,
                             QTextEdit,
                             QSplitter,
                             QMenuBar,
                             QScrollArea,
                             )
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, pyqtSignal

# Import qdarkstyle
# If not available
#  -> just pass
try:
    import qdarkstyle
except ImportError:
    print('qdarkstyle not installed! "pip install qdarkstyle"')
    pass

try:
    from ..parser.anffeed import ANFFeed
except ImportError:
    from ..parser.anffeed import ANFFeed

# Get the current directory to set the Icon later.
DIR = Path(__file__).parents[1]


class ArticleWidget(QWidget):
    '''
    Article Widget
    ==============

    This widget is holding a
    :class: QTextEdit
    as read-only, so there is
    no edit enabled for the User.
    '''
    def __init__(self, *args):
        super().__init__(*args)

        self.setGeometry(0, 0, 400, 600)

        self.initUi()

    def initUi(self):
        '''
        Defines UI of the
        :class: ArticleWidget

        The Layout is a
        :class: QVBoxLayout

        There is a
        :class: QLabel over
        the Text Box

        Central Widget of this
        class is the
        :class: QTextEdit
            - Read-onldy so user
              can not change or
              delete text by acci-
              dent
             - Font is set to:
               Times, and size 12
        Text to the QTextEdit is
        added in the
        :class: ANFApp:
            It catches the signal
            if a title is clicked
            and appends the:
                - Summary of the
                    content
                - Link of the article
                - The article (just
                    text, no pictures etc.)
        '''
        self.hbox = QVBoxLayout(self)
        self.setLayout(self.hbox)

        self.label = QLabel('Your chosen Feed (Summary, Link and Article):')
        self.hbox.addWidget(self.label)

        self.text = QTextEdit()
        self.text.setReadOnly(True)
        font = QFont('Times', 12)
        self.text.setFont(font)
        self.text.setPlaceholderText('Click on a title to read the article')
        self.hbox.addWidget(self.text)


class TitleWidget(QWidget):
    '''
    Title Widget
    ============

    This widget is presenting
    the Feed titles of the
    :class: ANFFeed ;
    It is also containing a
    :class: pyqtSignal
    on double click which will
    be responsible to present
    the linked feed in the
    :class: ArticleWidget
    '''
    TitleClicked = pyqtSignal([list])

    def __init__(self, *args):
        super().__init__(*args)

        self.setGeometry(0, 0, 350, 600)

        self.initUi()

    def initUi(self):
        '''
        Defines UI of the
        :class: TitleWidget

        The structure of this
        Widget:

        The Layout is a
        :class: QVBoxLayout

        :class: QLabel

        :class: QListWidget
        '''
        self.hbox = QVBoxLayout()
        self.setLayout(self.hbox)

        self.label = QLabel('Titles of available Feeds:')
        self.hbox.addWidget(self.label)

        self.titleList = QListWidget()
        self.titleList.itemPressed.connect(self.onClicked)

        self.newsFeed()

    def newsFeed(self, language=None):
        '''
        Set ANF Feeds
        =============

        This method is interacting
        with the :class: ANFFeed
        It is getting the RSS Feeds
        and is representing the Titles
        of each Feed.
        Furthermore, it is changing
        the language if the User is
        interacting with the "Language"
        option of the Menu.
            -> See more in the
            :class: ANFApp

        :param language:
            The language to be set
            (The ANFFeed is setting
            to English by default)
            Default here is None, so
            it is able to track if
            a language was chosen by
            the User or not
        :type language: str, optional
        '''
        self.news = ANFFeed()

        if language:
            self.news.set_language(language)
        for item in self.news.all_feeds:
            self.titleList.addItem(item[0])
            self.titleList.addItem('')
            font = QFont('Times')
            font.setBold(True)
            self.titleList.setFont(font)
        self.hbox.addWidget(self.titleList)

    def onClicked(self, item):
        '''
        Emit Content
        ============
        This method will be called
        on double click on one of
        the titles.
        Depending on the Title
        clicked on, it gets the
        Summary, Link and the
        article's text. After
        the pyqtSignal TitleClicked
        is emitting the content.

        :param item: Item contained
            by the article clicked on
        :type item: PyQt Obj
        '''
        feeds = self.news.all_feeds
        id = 0
        for elem in range(len(feeds)):
            if feeds[elem][0] == item.text():
                id = elem

        summary = feeds[id][1] + '\n\n'
        link = feeds[id][2]
        detailed = feeds[id][3]

        self.TitleClicked.emit([summary, link, detailed])


class ANFApp(QMainWindow):
    '''
    Main Window
    ===========

    All other Widgets and
    Elements are organized.

    Referring objets:
        - :class: TitleWidget
        - :class: ArticleWidget

    General Layout:
        - QStatusBar
        - QSplitter()
            - TitleWidget
            - ArticleWidget
        - QMenuBar
        - QPushButton (Exit)
    '''
    def __init__(self, *args):
        super().__init__(*args)

        self.setWindowState(Qt.WindowMaximized)
        self.setWindowIcon(QIcon(f'{DIR}/assets/anf.png'))
        self.setAutoFillBackground(True)
        self.setWindowTitle('ANF RSS Reader')
        self.statusBar()

        self.anfInit()

        self.show()

    def anfInit(self):
        '''
        Defines UI of the
        :class: ANFApp
            (Main Window)

        Both, the Article
        and the Title Widget
        are organized inside
        :class: QSplitter
        Moreover there is:
        :class: QMenuBar
        :class: QPushButton
            (Exit Button)
        '''
        self.central_widget = QSplitter()

        self.title_widget = TitleWidget()
        self.article_widget = ArticleWidget()

        self.setCentralWidget(self.central_widget)

        self.menu_bar = QMenuBar()
        self.actionEdit = self.menu_bar.addMenu('Edit')
        self.actionEdit.addAction('Size +')
        self.actionEdit.addAction('Size -')
        self.actionEdit.addSeparator()
        self.actionEdit.addAction('Settings')
        self.actionDownload = self.menu_bar.addMenu('Download')
        self.actionHelp = self.menu_bar.addMenu('Help')
        self.actionLang = self.menu_bar.addMenu('Language')
        self.actionLang.addAction('german')
        self.actionLang.addAction('english')
        self.actionLang.addAction('kurmanjî')
        self.actionLang.addAction('spanish')
        self.actionLang.addAction('arab')
        self.actionLang.hovered.connect(self.languageAction)
        self.central_widget.addWidget(self.menu_bar)

        self.central_widget.addWidget(self.title_widget)
        self.central_widget.addWidget(self.article_widget)

        self.exitBtn = QPushButton(self)
        self.exitBtn.setGeometry(50, 600, 100, 55)
        self.exitBtn.setText('Exit')
        self.exitBtn.setStyleSheet("background-color: red")
        self.exitBtn.setStatusTip('Exit the Application')
        self.exitBtn.clicked.connect(self.exit)

        # Catch Slot Signal from the TitleWidget
        self.title_widget.TitleClicked.connect(self.title_click)

        self.show()

    def languageAction(self, lang):
        '''
        Change Language
        ===============

        Changing the Language
        of the Feeds if Menu
        Option is hovered.

        :param lang: The Language
            Text given by Menu Option
        :type lang: PyQt obj
        '''
        self.title_widget.titleList.clear()
        self.title_widget.newsFeed(lang.text())
        self.title_widget.update()

    def title_click(self, feed):
        '''
        Signal Catcher
        ==============

        Catches the Slot Signal
        of the
        :class: TitleWidget
        and sets the Text for the
        :class: ArticleWidget;

        :param feed: The Signal
            in the TitleWidget
            emits a list with
            the contents;
        :type feed: list
        '''
        # Title = feed[0]
        # Link = feed[1]
        # Detailed = feed[2]

        # Set Title with Italic Font.
        self.article_widget.text.setFontItalic(True)
        self.article_widget.text.setText(feed[0])
        self.article_widget.text.setFontItalic(False)
        # Underline & Append Link.
        self.article_widget.text.setFontUnderline(True)
        self.article_widget.text.append(feed[1])
        self.article_widget.text.setFontUnderline(False)
        # Append Detailed
        self.article_widget.text.append('\n\n')
        self.article_widget.text.append(feed[2])

    def exit(self):
        '''
        Exit the Application
        ====================

        Called when Exit Button
        is clicked.
        '''
        self.close()


def run(*args):
    '''
    Run the App
    ===========

    Default Style is set
    to "Breeze"
    '''
    app = QApplication(sys.argv)

    for arg in args:
        if 'dark' in arg:
            app.setStyleSheet(qdarkstyle.load_stylesheet())
        else:
            app.setStyle('breeze')
    window = ANFApp()
    sys.exit(app.exec_())


if __name__ == '__main__':
    pass
