from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QDateEdit, QVBoxLayout
from PyQt5.QtCore import QDate




class rout_train_window(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Выберите дату")
        
        layout = QVBoxLayout(self)
        
        date_edit = QDateEdit(self)
        date_edit.setCalendarPopup(True)
        date_edit.setMinimumDate(QDate.currentDate())
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.button(QDialogButtonBox.Cancel).setText("Отмена")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(date_edit)
        layout.addWidget(button_box)