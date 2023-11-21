import sys
import sqlite3
import datetime
import csv

from pyqtgraph import mkPen

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QFileDialog, QTableWidgetItem, QButtonGroup

from MainWindow import Ui_MainWindow
from Registration_Window import UI_RegistrationWindow
from ChangeMarks import Change


# Класс основного окна приложения
class HeadWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, connection, user_id):
        super().__init__()
        super().setupUi(self)
        self.setWindowIcon(QIcon('chocolate.png'))
        self.setWindowTitle('Твой школьный дневник')
        self.initUI(connection, user_id)

    def initUI(self, connection, user_id):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.user_id = user_id
        self.big_dict = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}, 10: {}, 11: {}}

        # Прописываем связи сигналов со слотами
        self.save_dz_btn.clicked.connect(self.save_dz)
        self.delete_dz_btn.clicked.connect(self.delete_dz)
        self.delete_complete_dz_btn.clicked.connect(self.delete_complete_dz)
        self.refresh_tomorrow_dz_btn.clicked.connect(self.refresh_tomorrow_dz)
        self.refresh_undo_dz_btn.clicked.connect(self.refresh_undo_dz)
        self.take_from_file_btn.clicked.connect(self.friends_from_file)
        self.take_to_file_btn.clicked.connect(self.friends_to_file)
        self.add_friend_btn.clicked.connect(self.add_friend)
        self.delete_friend_id_btn.clicked.connect(self.delete_friend)
        self.build_graf_btn.clicked.connect(self.build_graf)
        self.delete_all_marks_btn.clicked.connect(self.delete_all_marks)
        self.add_change_mark_btn.clicked.connect(self.add_change_mark)

        # Создаем группу радио-кнопок и добавляем кнопки в нее
        self.buttons_group = QButtonGroup()
        self.buttons_group.addButton(self.radioButton_1)
        self.buttons_group.addButton(self.radioButton_2)
        self.buttons_group.addButton(self.radioButton_3)
        self.buttons_group.addButton(self.radioButton_4)
        self.buttons_group.addButton(self.radioButton_5)
        self.buttons_group.addButton(self.radioButton_6)
        self.buttons_group.addButton(self.radioButton_7)
        self.buttons_group.addButton(self.radioButton_8)
        self.buttons_group.addButton(self.radioButton_9)
        self.buttons_group.addButton(self.radioButton_10)

        # Загружаем картинки
        self.pixmap = QPixmap('kot_heart.png')
        self.lable_picture_kot_heart.setPixmap(self.pixmap)
        self.pixmap_2 = QPixmap('china_kot.png')
        self.picture_china_kot.setPixmap(self.pixmap_2)

        # Вызываем нужные функции, чтобы при входе в приложение сразу прогружались виджеты
        self.show_dz()
        self.write_in_big_dict()
        self.print_info_friends()
        self.complite_f_lable()

    def show_dz(self):
        # Загружаем список заданий из базы данных в виджеты
        result = self.cursor.execute("""SELECT subject,task,data,yes_no 
                                        FROM homework
                                        WHERE user_id = ?""",
                                        (self.user_id,)).fetchall()
        if result:
            self.comboBox_1.setCurrentText(result[0][0])
            self.lineEdit_1.setText(result[0][1])
            self.dateEdit_1.setDate(datetime.date(int(result[0][2][6:]),
                                                  int(result[0][2][3:5]),
                                                  int(result[0][2][:2])))
            self.checkBox_1.setChecked(bool(result[0][3]))
            self.comboBox_2.setCurrentText(result[1][0])
            self.lineEdit_2.setText(result[1][1])
            self.dateEdit_2.setDate(datetime.date(int(result[1][2][6:]),
                                                  int(result[1][2][3:5]),
                                                  int(result[1][2][:2])))
            self.checkBox_2.setChecked(bool(result[1][3]))
            self.comboBox_3.setCurrentText(result[2][0])
            self.lineEdit_3.setText(result[2][1])
            self.dateEdit_3.setDate(datetime.date(int(result[2][2][6:]),
                                                  int(result[2][2][3:5]),
                                                  int(result[2][2][:2])))
            self.checkBox_3.setChecked(bool(result[2][3]))
            self.comboBox_4.setCurrentText(result[3][0])
            self.lineEdit_4.setText(result[3][1])
            self.dateEdit_4.setDate(datetime.date(int(result[3][2][6:]),
                                                  int(result[3][2][3:5]),
                                                  int(result[3][2][:2])))
            self.checkBox_4.setChecked(bool(result[3][3]))
            self.comboBox_5.setCurrentText(result[4][0])
            self.lineEdit_5.setText(result[4][1])
            self.dateEdit_5.setDate(datetime.date(int(result[4][2][6:]),
                                                  int(result[4][2][3:5]),
                                                  int(result[4][2][:2])))
            self.checkBox_5.setChecked(bool(result[4][3]))
            self.comboBox_6.setCurrentText(result[5][0])
            self.lineEdit_6.setText(result[5][1])
            self.dateEdit_6.setDate(datetime.date(int(result[5][2][6:]),
                                                  int(result[5][2][3:5]),
                                                  int(result[5][2][:2])))
            self.checkBox_6.setChecked(bool(result[5][3]))
            self.comboBox_7.setCurrentText(result[6][0])
            self.lineEdit_7.setText(result[6][1])
            self.dateEdit_7.setDate(datetime.date(int(result[6][2][6:]),
                                                  int(result[6][2][3:5]),
                                                  int(result[6][2][:2])))
            self.checkBox_7.setChecked(bool(result[6][3]))
            self.comboBox_8.setCurrentText(result[7][0])
            self.lineEdit_8.setText(result[7][1])
            self.dateEdit_8.setDate(datetime.date(int(result[7][2][6:]),
                                                  int(result[7][2][3:5]),
                                                  int(result[7][2][:2])))
            self.checkBox_8.setChecked(bool(result[7][3]))
            self.comboBox_9.setCurrentText(result[8][0])
            self.lineEdit_9.setText(result[8][1])
            self.dateEdit_9.setDate(datetime.date(int(result[8][2][6:]),
                                                  int(result[8][2][3:5]),
                                                  int(result[8][2][:2])))
            self.checkBox_9.setChecked(bool(result[8][3]))
            self.comboBox_10.setCurrentText(result[9][0])
            self.lineEdit_10.setText(result[9][1])
            self.dateEdit_10.setDate(datetime.date(int(result[9][2][6:]),
                                                   int(result[9][2][3:5]),
                                                   int(result[9][2][:2])))
            self.checkBox_10.setChecked(bool(result[9][3]))
            self.comboBox_11.setCurrentText(result[10][0])
            self.lineEdit_11.setText(result[10][1])
            self.dateEdit_11.setDate(datetime.date(int(result[10][2][6:]),
                                                   int(result[10][2][3:5]),
                                                   int(result[10][2][:2])))
            self.checkBox_11.setChecked(bool(result[10][3]))

    def write_in_big_dict(self):
        # Сохраняем задачи в словарь
        self.big_dict[1] = {'subject': self.comboBox_1.currentText(),
                            'task': self.lineEdit_1.text(),
                            'data': self.dateEdit_1.text(),
                            'yes_no': self.checkBox_1.isChecked()}
        self.big_dict[2] = {'subject': self.comboBox_2.currentText(),
                            'task': self.lineEdit_2.text(),
                            'data': self.dateEdit_2.text(),
                            'yes_no': self.checkBox_2.isChecked()}
        self.big_dict[3] = {'subject': self.comboBox_3.currentText(),
                            'task': self.lineEdit_3.text(),
                            'data': self.dateEdit_3.text(),
                            'yes_no': self.checkBox_3.isChecked()}
        self.big_dict[4] = {'subject': self.comboBox_4.currentText(),
                            'task': self.lineEdit_4.text(),
                            'data': self.dateEdit_4.text(),
                            'yes_no': self.checkBox_4.isChecked()}
        self.big_dict[5] = {'subject': self.comboBox_5.currentText(),
                            'task': self.lineEdit_5.text(),
                            'data': self.dateEdit_5.text(),
                            'yes_no': self.checkBox_5.isChecked()}
        self.big_dict[6] = {'subject': self.comboBox_6.currentText(),
                            'task': self.lineEdit_6.text(),
                            'data': self.dateEdit_6.text(),
                            'yes_no': self.checkBox_6.isChecked()}
        self.big_dict[7] = {'subject': self.comboBox_7.currentText(),
                            'task': self.lineEdit_7.text(),
                            'data': self.dateEdit_7.text(),
                            'yes_no': self.checkBox_7.isChecked()}
        self.big_dict[8] = {'subject': self.comboBox_8.currentText(),
                            'task': self.lineEdit_8.text(),
                            'data': self.dateEdit_8.text(),
                            'yes_no': self.checkBox_8.isChecked()}
        self.big_dict[9] = {'subject': self.comboBox_9.currentText(),
                            'task': self.lineEdit_9.text(),
                            'data': self.dateEdit_9.text(),
                            'yes_no': self.checkBox_9.isChecked()}
        self.big_dict[10] = {'subject': self.comboBox_10.currentText(),
                             'task': self.lineEdit_10.text(),
                             'data': self.dateEdit_10.text(),
                             'yes_no': self.checkBox_10.isChecked()}
        self.big_dict[11] = {'subject': self.comboBox_11.currentText(),
                             'task': self.lineEdit_11.text(),
                             'data': self.dateEdit_11.text(),
                             'yes_no': self.checkBox_11.isChecked()}

    def save_dz(self):
        # Вызываем функцию сохранния задач в словарь
        self.write_in_big_dict()
        # Сохраняем задачи в базу данных
        # Если в базе данных что-то есть - удаляем и перезаписываем
        if self.cursor.execute("""SELECT id 
                                  FROM homework WHERE user_id = ?""",
                                  (self.user_id,)).fetchall():
            self.cursor.execute("""DELETE FROM homework 
                                   WHERE user_id = ?""",
                                   (self.user_id,))
            self.connection.commit()
        for i in range(1, 12):
            self.cursor.execute("""INSERT INTO homework(str_id, user_id,subject,task,data,yes_no)
                                   VALUES(?, ?, ?, ?, ?, ?)""",
                                (i, self.user_id,
                                 self.big_dict[i]['subject'],
                                 self.big_dict[i]['task'],
                                 self.big_dict[i]['data'],
                                 self.big_dict[i]['yes_no']))
            self.connection.commit()
        self.statusbar.showMessage('Задачи успешно сохранены:)')
        # Обновляем кол-во сделанных задач
        self.complite_f_lable()

    def delete_dz(self):
        number, ok_pressed = QInputDialog.getInt(
            self, "Удаление задачи", "Выберите номер задачи:",
            1, 1, 11, 1)
        self.big_dict[number] = {}
        self.cursor.execute("""UPDATE homework 
                               SET subject = 'Алгебра', 
                                   task = '', 
                                   data = '01.01.2000', 
                                   yes_no = 0
                               WHERE user_id = ? AND str_id = ?""",
                               (self.user_id, number))
        self.connection.commit()
        self.show_dz()
        self.statusbar.showMessage('Задача успешно удалена:) Пожалуйста, сохраните изменения!')

    def delete_complete_dz(self):
        self.cursor.execute("""UPDATE homework 
                               SET subject = 'Алгебра', 
                                   task = '', 
                                   data = '01.01.2000', 
                                   yes_no = 0
                               WHERE user_id = ? AND yes_no = 1""",
                               (self.user_id,))
        self.connection.commit()
        self.show_dz()
        self.statusbar.showMessage('Сделанные задачи успешно удалены:) Пожалуйста, сохраните изменения!')

    def complite_f_lable(self):
        # Обновляем кол-во сделанных задач
        count = 0
        for el in self.big_dict:
            if self.big_dict[el]['yes_no']:
                count += 1
        self.labe_complite.setText(f'Завершено: {count}')

    def refresh_tomorrow_dz(self):
        stroka = ''
        self.listWidget_tomorrow.clear()
        today = datetime.date.today()
        tasks = []
        for el in self.big_dict:
            per = self.big_dict[el]['data']
            data = datetime.date(int(per[6:]), int(per[3:5]), int(per[:2]))
            if (data - today).days == 1:
                tasks.append(self.big_dict[el]['task'])
        for elem in tasks:
            stroka += ' * ' + elem + '\n'
        self.listWidget_tomorrow.addItem(stroka)
        self.statusbar.showMessage('Задачи на завтра обновлены:)')

    def refresh_undo_dz(self):
        predmet = self.comboBox_subject.currentText()
        tasks = []
        stroka = ''
        self.listWidget_undo.clear()
        for el in self.big_dict:
            per = self.big_dict[el]['task']
            if self.big_dict[el]['subject'] == predmet and not self.big_dict[el]['yes_no']:
                tasks.append(per)
        for elem in tasks:
            if elem != '':
                stroka += ' * ' + elem + '\n'
        self.listWidget_undo.addItem(stroka)
        self.statusbar.showMessage('Несделанные задачи обновлены:)')

    def friends_from_file(self):
        file = QFileDialog.getOpenFileName(
            self, 'Выбрать csv-файл', '', 'csv-файл (*.csv);;Все файлы (*)')[0]
        with open(file, encoding='utf8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for index, row in enumerate(reader):
                friend = row[0]
                phone = row[1]
                vk = row[2]
                self.cursor.execute("""INSERT INTO schoolmates(user_id, fio,phone,vk) 
                                       VALUES(?,?,?,?)""",
                                       (self.user_id, friend, phone, vk))
                self.connection.commit()
        self.print_info_friends()
        self.statusbar.showMessage('Список из файла загружен:)')

    def friends_to_file(self):
        try:
            name_file, ok_pressed = QInputDialog.getText(self,
                                                         "Сохранение файла", "Введите название файла (без расширения)")
            if ok_pressed:
                file_str = name_file + '.csv'
            with open(file_str, 'w', newline='', encoding='utf8') as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
                for i in range(self.tableWidget.rowCount()):
                    row = []
                    for j in range(1, self.tableWidget.columnCount()):
                        item = self.tableWidget.item(i, j)
                        if item is not None:
                            row.append(item.text())
                    writer.writerow(row)
            self.statusbar.showMessage(f'Список сохранён в файл {file_str}')
        except Exception as e:
            self.statusbar.showMessage('Проверьте свой ввод, пожалуйста:)')
            print(e)

    def print_info_friends(self):
        # Вносим список одноклассников в TableWidget
        result = self.cursor.execute("""SELECT id, fio, phone, vk 
                                        FROM schoolmates 
                                        WHERE user_id = ?""",
                                        (self.user_id,)).fetchall()
        if not result:
            self.tableWidget.clear()
            return
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.setHorizontalHeaderLabels(['id', 'ФИО', 'Телефон', 'ВК'])

    def add_friend(self):
        fio = self.lineEdit_fio.text()
        if not fio:
            self.statusbar.showMessage('ФИО нужно ввести обязательно:)')
            return
        phone = self.lineEdit_phone.text()
        vk = self.lineEdit_vk.text()
        self.cursor.execute("""INSERT INTO schoolmates(user_id,fio,phone,vk) 
                               VALUES(?,?,?,?)""",
                               (self.user_id, fio, phone, vk))
        self.connection.commit()
        self.print_info_friends()
        self.statusbar.showMessage('Одноклассник успешно добавлен:)')

    def delete_friend(self):
        id = self.lineEdit_id_friend.text()
        result = self.cursor.execute("""SELECT fio 
                                        FROM schoolmates 
                                        WHERE id = ?""",
                                        (id,)).fetchall()
        if list(result):
            self.cursor.execute("""DELETE FROM schoolmates 
                                   WHERE id = ?""",
                                   (id,))
            self.connection.commit()
            self.statusbar.showMessage('Одноклассник успешно удалён:)')
            self.print_info_friends()
        else:
            self.statusbar.showMessage('Кто это?')

    def build_graf(self):
        # Строим график оценок
        # Если в базе данных меньше 2-х оценок - не строим график и выводим предупреждение в statusbar
        if self.buttons_group.checkedButton():
            subject = self.buttons_group.checkedButton().text()
            result = self.cursor.execute("""SELECT quoter, mark 
                                            FROM marks
                                            WHERE subject = ? AND user_id = ?""",
                                            (subject, self.user_id)).fetchall()
            if len(result) >= 2:
                marks = [x[1] for x in result]
                quoters = [x[0] for x in result]
                self.graphicsView.clear()
                self.graphicsView.setBackground((255, 228, 196))
                pen = mkPen((115, 72, 52), width=3)
                self.graphicsView.plot(quoters, marks, pen=pen)
                self.statusbar.showMessage('График построен:)')

            else:
                self.statusbar.showMessage('Пока не хватает оценок')

    def delete_all_marks(self):
        result = self.cursor.execute("""SELECT mark 
                                        FROM marks
                                        WHERE user_id = ?""",
                                        (self.user_id,)).fetchall()
        if list(result):
            self.cursor.execute("""DELETE FROM marks
                                   WHERE user_id = ?""",
                                   (self.user_id,))
            self.statusbar.showMessage('Все оценки удалены:)')
            self.connection.commit()
        else:
            self.statusbar.showMessage('У вас пока нет оценок, удалять нечего')

    def add_change_mark(self):
        try:
            self.form = Change_Marks(self.user_id, self.connection)
            self.form.show()
            self.statusbar.showMessage("""Ваши оценки успешно сохранены! Постройте график заново:)""")
        except Exception as e:
            print(e)


# Дополнительное окно для ввода оценки за четверть
class Change_Marks(QMainWindow, Change):
    def __init__(self, user_id, connection):
        super().__init__()
        super().setupUi(self)
        self.setWindowIcon(QIcon('chocolate.png'))
        self.setWindowTitle('Сохранить/изменить оценку')
        self.initUI(user_id, connection)

    def initUI(self, user_id, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.user_id = user_id
        self.Ok_btn.clicked.connect(self.press_ok)

    def press_ok(self):
        subject = self.comboBox_subject.currentText()
        quater = self.comboBox_quater.currentText()
        mark = self.comboBox_mark.currentText()
        if not subject or not quater or not mark:
            self.statusbar.showMessage("Пожалуйста, заполните все поля!")
            return
        result = self.cursor.execute("""SELECT id 
                                        FROM marks 
                                        WHERE user_id = ? AND subject = ? AND quoter = ?""",
                                        (self.user_id, subject, quater)).fetchall()
        if result:
            self.cursor.execute("""UPDATE marks 
                                   SET mark = ?
                                   WHERE user_id = ? AND subject = ? AND quoter = ?""",
                                   (mark, self.user_id, subject, quater))
            self.connection.commit()
        else:
            self.cursor.execute("""INSERT INTO marks(user_id,subject,quoter,mark) 
                                   VALUES(?,?,?,?)""",
                                   (self.user_id, subject, quater, mark))
            self.connection.commit()
        self.close()


# Класс окна регистрации и входа
class Registration(QMainWindow, UI_RegistrationWindow):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.setWindowIcon(QIcon('chocolate.png'))
        self.setWindowTitle('Твой школьный дневник')
        self.initUI()

    def initUI(self):
        self.regist_btn.clicked.connect(self.registration)
        self.vhod_btn.clicked.connect(self.vhod)
        self.connection = sqlite3.connect('QT_DataBase.db')
        self.cursor = self.connection.cursor()
        self.login_lineEdit.setText('Логин')
        self.password_lineEdit.setText('Пароль')
        self.pixmap = QPixmap('kot_klubok.png')
        self.picture_lable.setPixmap(self.pixmap)

    def registration(self):
        self.login = self.login_lineEdit.text()
        self.password = self.password_lineEdit.text()
        try:
            if self.login and self.password:
                result = list(self.cursor.execute("""SELECT login 
                                                     FROM users""").fetchall())
                logins = list(map(lambda x: x[0], result))
                if self.login not in logins:
                    self.cursor.execute("""INSERT INTO users(login, password)
                                           VALUES (?, ?)""",
                                           (self.login, self.password))
                    self.connection.commit()
                    self.statusbar.showMessage('Регистрация прошла успешно. Теперь вы можете войти:)')
                else:
                    self.statusbar.showMessage('Вы уже регистрировались ранее. Можете входить:)')
            else:
                self.statusbar.showMessage('Заполните оба поля, пожалуйста:)')
        except Exception as e:
            print(e)

    def vhod(self):
        self.login = self.login_lineEdit.text()
        self.password = self.password_lineEdit.text()
        result = self.cursor.execute("""SELECT login 
                                        FROM users
                                        WHERE login = ? AND password = ?""",
                                        (self.login, self.password)).fetchone()
        if result:
            self.user_id = (self.cursor.execute("""SELECT id 
                                                   FROM users
                                                   WHERE login = ? AND password = ?""",
                                                   (self.login, self.password)).fetchone())[0]
            self.second_window = HeadWindow(self.connection, self.user_id)
            self.second_window.show()
            self.close()
        else:
            self.statusbar.showMessage('Простите, вы ввели что-то не то. Перепроверьте себя:)')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Registration()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
