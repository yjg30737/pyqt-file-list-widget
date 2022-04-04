from collections import defaultdict

from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QDialog, QAbstractItemView
from PyQt5.QtCore import Qt
import os

from pyqt_files_already_exists_dialog import FilesAlreadyExistDialog


class FileListWidget(QListWidget):

    def __init__(self):
        super().__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__exists_dialog_not_ask_again_flag = False

        self.__extensions = []
        self.__basename_absname_dict = defaultdict(str)
        self.__show_filename_only_flag = False

    def __initUi(self):
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(True)

    def setExtensions(self, extensions: list):
        self.__extensions = extensions

    def addFilename(self, filename: str):
        item = QListWidgetItem(filename)
        absname = item.text()
        basename = os.path.basename(absname)
        self.__basename_absname_dict[basename] = absname
        if self.isFilenameOnly():
            item.setText(basename)
        else:
            item.setText(absname)
        self.addItem(item)

    def addFilenames(self, filenames: list):
        exists_file_lst = []
        not_exists_file_lst = []
        for filename in filenames:
            filename_to_find = os.path.basename(filename) if self.isFilenameOnly() else filename
            items = self.findItems(filename_to_find, Qt.MatchFixedString)
            if items:
                exists_file_lst.append(items[0])
            else:
                not_exists_file_lst.append(filename)
        if exists_file_lst:
            dialog = FilesAlreadyExistDialog()
            dialog.setDontAskAgainChecked(self.__exists_dialog_not_ask_again_flag)
            dialog.setExistFiles(exists_file_lst)
            reply = dialog.exec()
            if reply == QDialog.Accepted:
                for filename in not_exists_file_lst:
                    self.addFilename(filename)
                return
            else:
                return
        else:
            for filename in not_exists_file_lst:
                self.addFilename(filename)

    def setFilenameOnly(self, f: bool):
        self.__show_filename_only_flag = f
        self.__execShowingBaseName(f)

    def remove(self, item: QListWidgetItem):
        filename = item.text()
        self.takeItem(self.row(item))
        self.__basename_absname_dict.pop(os.path.basename(filename))

    def getSelectedFilenames(self) -> list:
        items = self.selectedItems()
        filenames = [item.text() for item in items]
        return filenames

    def removeSelectedRows(self):
        items = self.selectedItems()
        if items:
            items = reversed(items)
            for item in items:
                self.remove(item)

    def clear(self):
        for i in range(self.count() - 1, -1, -1):
            self.remove(self.item(i))
        super().clear()

    def isFilenameOnly(self) -> bool:
        return self.__show_filename_only_flag

    def getAbsFilename(self, basename: str):
        return self.__basename_absname_dict[basename]

    def __getExtFilteredFiles(self, lst):
        if len(self.__extensions) > 0:
            return list(map(lambda x: x if os.path.splitext(x)[-1] in self.__extensions else None, lst))
        else:
            return lst

    def __getFilenames(self, urls):
        return list(map(lambda x: x.path()[1:], urls))

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()

    def dragMoveEvent(self, e):
        pass

    def dropEvent(self, e):
        filenames = [file for file in self.__getExtFilteredFiles(
            self.__getFilenames(e.mimeData().urls())) if file]
        self.addFilenames(filenames)
        super().dropEvent(e)

    def __execShowingBaseName(self, f: bool):
        self.__show_filename_only_flag = f
        items = [self.item(i) for i in range(self.count())]
        if f:
            for item in items:
                absname = item.text()
                basename = os.path.basename(absname)
                item.setText(basename)
        else:
            for item in items:
                basename = item.text()
                absname = self.__basename_absname_dict[basename]
                item.setText(absname)
