import sys

from PySide6.QtCore import QStringListModel
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QListView,
    QPushButton,
    QStyle,
    QVBoxLayout,
    QWidget,
)


class RoboControlPredefinedCommandsWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("String List Model Example")

        self.string_list_model = QStringListModel()

        self.list_view = QListView()
        self.list_view.setModel(self.string_list_model)
        self.list_view.setSelectionMode(QListView.SelectionMode.ExtendedSelection)
        self.list_view.setDragEnabled(True)
        self.list_view.setEditTriggers(QListView.EditTrigger.NoEditTriggers)

        self.add_button = QPushButton("Add current")

        self.add_button.setIcon(
            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOkButton)),
        )

        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.setIcon(
            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogResetButton)),
        )
        self.remove_button.clicked.connect(self.remove_selected_item)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.remove_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.list_view)
        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

    def add_element(self, text: str) -> None:
        item_list = self.string_list_model.stringList()
        item_list.append(text)
        self.string_list_model.setStringList(item_list)

    def remove_selected_item(self) -> None:
        selected_indexes = self.list_view.selectedIndexes()
        item_list = self.string_list_model.stringList()
        skip_idx = {index.row() for index in selected_indexes}

        index = 0
        for idx, val in enumerate(item_list):
            if idx not in skip_idx:
                item_list[index] = val
                index += 1
        skip_indexes = len(item_list) - len(skip_idx)
        self.string_list_model.setStringList(item_list[:skip_indexes])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RoboControlPredefinedCommandsWidget()
    window.show()
    sys.exit(app.exec())