# -*- coding: utf-8 -*-
from aqt.qt import *
from .const import *
from .manage import *
import os.path

QCOLOR_ORANGE = QColor(255, 165, 0, 50)
QCOLOR_GREEN = QColor(0, 255, 0, 50)


class DictionaryManager:
    def __init__(self):
        self.setupMenu()

    def setupMenu(self):
        a = QAction("Dictionary Configuration", mw)
        a.triggered.connect(self.showConfig)
        mw.form.menuTools.addAction(a)

    def showConfig(self):
        DictionaryDialog()
        refreshLanguages()


class DictionaryDialog(QDialog):

    list = None

    def __init__(self):
        QDialog.__init__(self)

        self._enabled = getUserData("enabled", default={key: False for key in LANGUAGE_LIST})
        self._downloaded = {key: False for key in LANGUAGE_LIST}
        self._setupDialog()
        self._update()
        self.exec()

    def _setupDialog(self):
        self.setWindowTitle("Spell checker configuration")
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.resize(350, 300)

        layout = QHBoxLayout()
        self.list = QListWidget()
        self.list.setAlternatingRowColors(True)
        self.list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.list.itemDoubleClicked.connect(self._toggle)

        en_btn = QPushButton('Enable')
        en_btn.clicked.connect(self._enable)
        dis_btn = QPushButton('Disable')
        dis_btn.clicked.connect(self._disable)

        l1 = QLabel("Enabled")
        l1.setStyleSheet(f"background-color:rgba{QCOLOR_GREEN.getRgb()}")
        l2 = QLabel("Missing/downloading")
        l2.setStyleSheet(f"background-color:rgba{QCOLOR_ORANGE.getRgb()}")
        l3 = QLabel("Disabled")

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)

        comp_btn = QPushButton("Compile your\ndictionaries")
        comp_btn.clicked.connect(compileUserDictionaries)

        open_pdics_btn = QPushButton("Open personal\ndictionary folder")
        open_pdics_btn.clicked.connect((partial(openPath, USER_DICT_PATH)))

        open_dics_btn = QPushButton("Open .bdic folder")
        open_dics_btn.clicked.connect((partial(openPath, DICT_DIR)))

        control_box = QVBoxLayout()
        control_box.alignment()
        control_box.addWidget(en_btn)
        control_box.addWidget(dis_btn)
        control_box.addWidget(l1)
        control_box.addWidget(l2)
        control_box.addWidget(l3)
        control_box.addWidget(line)
        control_box.addWidget(comp_btn)
        control_box.addWidget(open_pdics_btn)
        control_box.addWidget(open_dics_btn)

        layout.addWidget(self.list)
        layout.addLayout(control_box)
        self.setLayout(layout)

    def _update(self, *args):
        self.list.clear()

        download = []
        dic_files = getDictionaries()
        for key, value in self._enabled.items():
            if key not in dic_files and value:
                download.append(key)
            if key in dic_files and value:
                dic_files.remove(key)
                self._downloaded[key] = True
            if not value:
                self._downloaded[key] = False
        if download:
            self._manageDownloads(download)

        for dic in dic_files:
            if dic == "personal":
                continue
            item = QListWidgetItem(f"Custom: {dic}.bdic")
            item.setBackground(QCOLOR_GREEN)
            item.setData(Qt.ItemDataRole.WhatsThisRole, "custom")
            item.setData(Qt.ItemDataRole.UserRole, dic)
            self.list.addItem(item)

        for key, language in LANGUAGE_LIST.items():
            name = language[0]
            item = QListWidgetItem(name)
            if self._enabled[key]:
                item.setBackground(QCOLOR_ORANGE)
            if self._downloaded[key]:
                item.setBackground(QCOLOR_GREEN)
            item.setData(Qt.ItemDataRole.UserRole, key)
            self.list.addItem(item)

    def _downloadItemUpdate(self):
        li = self.list
        dl = getDictionaries()
        for i in range(li.count()):
            key = li.item(i).data(Qt.ItemDataRole.UserRole)
            if key in dl:
                li.item(i).setBackground(QCOLOR_GREEN)

    @background_op()
    def _manageDownloads(self, keys, *args):
        for key in keys:
            file_path = os.path.join(DICT_DIR, key + ".bdic.disabled")
            if os.path.isfile(file_path):
                os.rename(file_path, file_path.removesuffix(".disabled"))
            else:
                self._download(key)
        self._downloadItemUpdate()
        return keys

    def _download(self, key):
        list_raw = download(URL_DICTIONARIES(LANGUAGE_LIST[key][1])).json()
        targets = ["index.aff", "index.dic"]
        downloads = [item["download_url"] for item in list_raw if any([x in item["name"] for x in targets])]

        temp_files = []
        temp_dict = os.path.join(DICT_DIR, "tmp")
        for down in downloads:
            save_path = downloadToFile(down, temp_dict, ".".join([key, down.split(".")[-1]]))
            temp_files.append(save_path)

        compileBDIC(temp_dict, key, remove=True)

    def _enable(self):
        sel = [i for i in range(self.list.count()) if self.list.item(i).isSelected()]
        if sel:
            for i in sel:
                fn = self.list.item(i).data(Qt.ItemDataRole.UserRole)
                cu = self.list.item(i).data(Qt.ItemDataRole.WhatsThisRole)
                if cu:
                    continue
                if fn is not None:
                    self._enabled[fn] = True
        setUserData("enabled", self._enabled)
        self._update()

    def _disable(self):
        sel = [i for i in range(self.list.count())
               if self.list.item(i).isSelected()]
        if sel:
            for i in sel:
                fn = self.list.item(i).data(Qt.ItemDataRole.UserRole)
                cu = self.list.item(i).data(Qt.ItemDataRole.WhatsThisRole)
                file_path = os.path.join(DICT_DIR, fn + ".bdic")
                if cu:
                    os.remove(file_path)
                if fn is not None:
                    self._enabled[fn] = False
                    if os.path.isfile(file_path):
                        os.rename(file_path, file_path + ".disabled")
        setUserData("enabled", self._enabled)
        self._update()

    def _toggle(self):
        fn = self.list.currentItem().data(Qt.ItemDataRole.UserRole)
        if fn is not None:
            self._enabled[fn] = not self._enabled[fn]
        setUserData("enabled", self._enabled)
        self._update()
