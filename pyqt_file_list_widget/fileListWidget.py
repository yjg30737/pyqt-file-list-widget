from collections import defaultdict

from PyQt5.QtWidgets import QListWidgetItem, QDialog, QAbstractItemView
from PyQt5.QtCore import Qt
import os

from pyqt_files_already_exists_dialog import FilesAlreadyExistDialog
from pyqt_show_long_text_as_tooltip_list_widget import ShowLongTextAsToolTipListWidget


class FileListWidget(ShowLongTextAsToolTipListWidget):

    def __init__(self):
        super().__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__exists_dialog_not_ask_again_flag = False
        self.__duplicated_flag = True

        self.__extensions = []
        self.__basename_absname_dict = defaultdict(str)
        self.__show_filename_only_flag = False

    def __initUi(self):
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(True)

    def isDuplicatedEnabled(self) -> bool:
        return self.__duplicated_flag

    def setDuplicatedEnabled(self, f: bool):
        self.__duplicated_flag = f

    def setExtensions(self, extensions: list):
        self.__extensions = extensions

    def addFilename(self, filename: str):
        items = []
        basename = os.path.basename(filename)
        filename_to_find = self.__getFilenameToFind(filename)
        if self.isDuplicatedEnabled():
            # todo refactoring
            item = QListWidgetItem(filename_to_find)
            self.__basename_absname_dict[basename] = filename
            self.addItem(item)
        else:
            items = self.findItems(filename_to_find, Qt.MatchFixedString)
            if items:
                # reply = self.__execExistsDialog(items)
                self.setCurrentItem(items[0])
            else:
                # todo refactoring
                item = QListWidgetItem(filename_to_find)
                self.__basename_absname_dict[basename] = filename
                self.addItem(item)

    def __execExistsDialog(self, exists_file_lst):
        dialog = FilesAlreadyExistDialog()
        dialog.setDontAskAgainChecked(self.__exists_dialog_not_ask_again_flag)
        dialog.setExistFiles(exists_file_lst)
        reply = dialog.exec()

    def addFilenames(self, filenames: list):
        if self.isDuplicatedEnabled():
            for filename in filenames:
                self.addFilename(filename)
        else:
            duplicated_filenames = self.__getDuplicatedItems(filenames)
            if duplicated_filenames:
                self.__execExistsDialog(duplicated_filenames)
            else:
                for filename in filenames:
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
            removed_start_idx = self.row(items[0])
            cur_idx = removed_start_idx - 1
            if removed_start_idx == 0:
                cur_idx = 0
            items = list(reversed(items))
            for item in items:
                self.remove(item)
            self.setCurrentRow(cur_idx)

    def clear(self):
        for i in range(self.count() - 1, -1, -1):
            self.remove(self.item(i))
        super().clear()

    def isFilenameOnly(self) -> bool:
        return self.__show_filename_only_flag

    def __getDuplicatedItems(self, filenames: list) -> list:
        exists_file_lst = []
        for filename in filenames:
            filename_to_find = self.__getFilenameToFind(filename)
            items = self.findItems(filename_to_find, Qt.MatchFixedString)
            if items:
                exists_file_lst.append(items[0])
        return exists_file_lst

    def __getFilenameToFind(self, filename: str) -> str:
        filename_to_find = os.path.basename(filename) if self.isFilenameOnly() else filename
        return  filename_to_find

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
