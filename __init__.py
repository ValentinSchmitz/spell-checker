# -*- coding: utf-8 -*-
from PyQt6.QtWebEngineCore import QWebEngineProfile
from aqt import editor, QMenu
from functools import partial
from aqt import gui_hooks
from aqt.qt import *

from .dict import DictionaryManager, getDictionaries
from .manage import *
from .const import *

dictMan = DictionaryManager()


def addToDictionary(word):
    saveWrite(PERSONAL_PATH, f"{word}\n", "a+")
    compilePersonal()


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
            recommendation.triggered.connect(partial(page.replaceMisspelledWord, word))

        menu.insertSeparator(base_action)

    if data.misspelledWord():
        add = menu.addAction("Add to dictionary")
        menu.insertAction(base_action, add)
        add.triggered.connect(partial(addToDictionary, data.misspelledWord()))

        menu.insertSeparator(base_action)


def setupBDIC(editor_webview: editor.EditorWebView):
    page = editor_webview._page
    profile: QWebEngineProfile = page.profile()
    profile.setSpellCheckEnabled(getUserData("status", default=True))
    profile.setSpellCheckLanguages(getDictionaries())


def on_setup_editor_buttons(buttons, edi: editor.Editor):
    icon = os.path.join(ADDON_PATH, "icon.svg")

    def toggleSpellChecker(edit: editor.Editor):
        new = not getUserData("status", default=False)
        setUserData("status", new)
        mw.web._page.profile().setSpellCheckEnabled(new)

    b = edi.addButton(
        icon,
        "SC",
        toggleSpellChecker,
        tip="Toggle Spell Checker"
    )
    buttons.append(b)
    return buttons


gui_hooks.editor_did_init_buttons.append(on_setup_editor_buttons)
gui_hooks.editor_will_show_context_menu.append(onContextMenuEvent)
gui_hooks.editor_web_view_did_init.append(setupBDIC)
gui_hooks.main_window_did_init.append(checkConversionBinaries)
mw.addonManager.setConfigAction(__name__, dictMan.showConfig)
