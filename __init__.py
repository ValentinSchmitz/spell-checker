import os.path

from PyQt6.QtWebEngineCore import QWebEngineProfile
from aqt import gui_hooks
from aqt.qt import *
from aqt import editor, QMenu
from .const import *
from functools import partial

from .dict import DictionaryManager

dictMan = DictionaryManager()


def replaceMisspelledWord(page, recommendation):
    page.replaceMisspelledWord(recommendation)


def addToDictionary(word):
    try:
        # workaround for bdic compiler, only takes files with >4 lines
        if not os.path.isfile(PERSONAL_PATH):
            with open(PERSONAL_PATH, "a") as f:
                f.write("abc \nabcde\nabcdef\nabcdefg\n")

        with open(PERSONAL_PATH, "a") as f:
            f.write(f"{word}\n")
        dictMan.refreshUserDictionary()
    except IOError as error:
        showWarning(f"Could not write user files, check permissions. Error: {error}")


def onContextMenuEvent(editor_webview: editor.EditorWebView, menu: QMenu):
    page = editor_webview._page

    base_action = menu.actions()[0]

    data = editor_webview.lastContextMenuRequest()

    if data.spellCheckerSuggestions():
        title = menu.addAction("Spell suggestions:")
        title.setEnabled(False)
        menu.insertAction(base_action, title)

        for word in data.spellCheckerSuggestions():
            recommendation = menu.addAction(word)
            menu.insertAction(base_action, recommendation)
            recommendation.triggered.connect(partial(replaceMisspelledWord, page, word))

        menu.insertSeparator(base_action)

        add = menu.addAction("Add to dictionary")
        menu.insertAction(base_action, add)
        add.triggered.connect(partial(addToDictionary, data.misspelledWord()))

        menu.insertSeparator(base_action)


def setupBDIC(editor_webview: editor.EditorWebView):
    page = editor_webview._page
    profile: QWebEngineProfile = page.profile()
    profile.setSpellCheckEnabled(True)
    profile.setSpellCheckLanguages(dictMan.getDictionaries())


gui_hooks.editor_will_show_context_menu.append(onContextMenuEvent)
gui_hooks.editor_web_view_did_init.append(setupBDIC)
