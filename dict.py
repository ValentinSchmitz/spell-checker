import pickle
import subprocess
from aqt.operations import QueryOp
from requests import get
from aqt.qt import *
from aqt.utils import openFolder, showWarning, showInfo
from .const import *
from functools import partial


class DictionaryManager:
    def __init__(self):
        self.setupMenu()

    def setupMenu(self):
        a = QAction("Dictionary Configuration", mw)
        a.triggered.connect(self.showConfig)
        mw.form.menuTools.addAction(a)

    def showConfig(self):
        DictionaryDialog()
        self._refreshLanguages()

    def getDictionaries(self):
        dicts = []
        for file in os.listdir(DICT_DIR):
            if file.endswith(".bdic"):
                dicts.append(file.removesuffix(".bdic"))
        return dicts

    def refreshUserDictionary(self, *args):
        op = QueryOp(parent=mw, op=self._compileUserDictionary, success=self._refreshLanguages)
        op.run_in_background()

    def _compileUserDictionary(self, *args):
        command = " ".join([os.path.join(ADDON_PATH, "convert_dict", "convert_dict"), PERSONAL_PATH])
        ex = subprocess.call([command], shell=True)
        if os.path.isfile(os.path.join(USER_PATH, "personal" + ".bdic")):
            os.rename(os.path.join(USER_PATH, "personal" + ".bdic"), os.path.join(DICT_DIR, "personal" + ".bdic"))

    def _refreshLanguages(self, *args):
        p = mw.web._page.profile()
        p.setSpellCheckLanguages({})
        p.setSpellCheckLanguages(self.getDictionaries())
        p.setSpellCheckEnabled(True)


class DictionaryDialog(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        self._enabled = self._getEnabledList()
        self._downloaded = {key: False for key in LANGUAGE_LIST}
        self._setupDialog()
        self._isUpdating = False
        self._update()
        self.exec()

    def _setupDialog(self):
        self.setWindowTitle("Dictionaries")
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.resize(250, 250)

        layout = QVBoxLayout()
        self.list = QListWidget()
        self.list.setAlternatingRowColors(True)
        self.list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.list.itemDoubleClicked.connect(self._toggle)

        en_btn = QPushButton('Enable')
        en_btn.clicked.connect(self._enable)
        dis_btn = QPushButton('Disable')
        dis_btn.clicked.connect(self._disable)

        control_box = QHBoxLayout()
        control_box.addWidget(en_btn)
        control_box.addWidget(dis_btn)

        layout.addWidget(self.list)
        layout.addLayout(control_box)
        self.setLayout(layout)

    def _update(self):
        self._isUpdating = True
        self.list.clear()

        download = []
        for key, value in self._enabled.items():
            dic_file = os.path.join(DICT_DIR, key + ".bdic")
            dic_file_is = os.path.isfile(dic_file)
            if dic_file_is and value:
                self._downloaded[key] = True
            if not dic_file_is and value:
                download.append(key)
            if dic_file_is and not value:
                os.remove(dic_file)
                self._downloaded[key] = False
        if download:
            op = QueryOp(parent=mw, op=partial(self._manageDownloads, download), success=self._downloadItemUpdate)
            op.run_in_background()

        for key, language in LANGUAGE_LIST.items():
            name = language[0]
            item = QListWidgetItem(name)
            if self._enabled[key]:
                item.setBackground(QColor(255, 165, 0, 50))
            if self._downloaded[key]:
                item.setBackground(QColor(0, 255, 0, 50))
            item.setData(Qt.ItemDataRole.UserRole, key)
            self.list.addItem(item)
        self._isUpdating = False

    def _downloadItemUpdate(self, keys):
        for i in range(self.list.count()):
            if self.list.item(i).data(Qt.ItemDataRole.UserRole) in keys:
                self.list.item(i).setBackground(QColor(0, 255, 0, 50))

    def _enable(self):
        sel = [i for i in range(self.list.count()) if self.list.item(i).isSelected()]
        if sel:
            for i in sel:
                fn = self.list.item(i).data(Qt.ItemDataRole.UserRole)
                if fn is not None:
                    self._enabled[fn] = True
        self._setEnabledList()
        self._update()

    def _manageDownloads(self, keys, *args):
        for key in keys:
            self._download(key)
        return keys

    def _download(self, key):
        list_raw = get(URL_DICTIONARIES(LANGUAGE_LIST[key][1])).json()
        targets = ["index.aff", "index.dic"]
        downloads = [item["download_url"] for item in list_raw if any([x in item["name"] for x in targets])]

        temp_files = []
        temp_dict = os.path.join(DICT_DIR, "tmp")
        for down in downloads:
            try:
                res = get(down)
            except ConnectionError as error:
                showWarning(
                    "Internet connection failed. Dictionary files could not be downloaded. Please ensure you have an "
                    f"internet connection and reopen the 'Dictionary Configuration'. Error: {error}")
                break
            if res.status_code != 200:
                showWarning("Dictionary acces failed. Please contact the author of the PlugIn.")
            if not os.path.exists(temp_dict):
                try:
                    os.makedirs(temp_dict)
                except OSError as error:
                    showWarning(f"Dictionary downloads could not be saved to disk. Error: {error}")
            save_path = os.path.join(temp_dict, ".".join([key, down.split(".")[-1]]))
            temp_files.append(save_path)
            try:
                with open(save_path, "w+b") as f:
                    f.write(res.content)
            except IOError as error:
                showWarning(f"Dictionary downloads could not be saved to disk. Error: {error}")

        command = " ".join([os.path.join(ADDON_PATH, "convert_dict", "convert_dict"), os.path.join(temp_dict, key)])
        ex = subprocess.call([command], shell=True)
        if ex != 0:
            self._enabled[key] = False
            showInfo(f"Dictionary {LANGUAGE_LIST[key][0]} is broken, please report this error message.")

        for f in temp_files:
            os.remove(f)
        if os.path.isfile(os.path.join(temp_dict, key + ".bdic")):
            os.rename(os.path.join(temp_dict, key + ".bdic"), os.path.join(DICT_DIR, key + ".bdic"))

    def _disable(self):
        sel = [i for i in range(self.list.count())
               if self.list.item(i).isSelected()]
        if sel:
            for i in sel:
                fn = self.list.item(i).data(Qt.ItemDataRole.UserRole)
                if fn is not None:
                    self._enabled[fn] = False
        self._setEnabledList()
        self._update()

    def _toggle(self):
        fn = self.list.currentItem().data(Qt.ItemDataRole.UserRole)
        if fn is not None:
            self._enabled[fn] = not self._enabled[fn]
        self._setEnabledList()
        self._update()

    def _getEnabledList(self):
        default = {key: False for key in LANGUAGE_LIST}

        if not os.path.isfile(ENABLED_PATH):
            return default
        try:
            with open(ENABLED_PATH, "rb") as f:
                pck = f.read()
                return pickle.loads(pck)
        except IOError as err:
            showWarning(f"Could not read user files, check permissions. Error: {err}")
            return default

    def _setEnabledList(self):
        try:
            with open(ENABLED_PATH, "w+b") as f:
                pck = pickle.dumps(self._enabled)
                f.write(pck)
        except IOError as err:
            showWarning(f"List of enabled languages could not be saved to disk. Error: {err}")
