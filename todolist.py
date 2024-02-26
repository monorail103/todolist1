import sys
import os
import json
import random
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QDateEdit, QListWidgetItem,QMessageBox
from datetime import datetime,timedelta
from PySide6.QtGui import QFont,QColor


class TodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ToDo List')
        self.setup_ui()
        self.load_todo_list()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # ToDoリスト表示用のウィジェット
        self.todo_list_widget = QListWidget()
        layout.addWidget(self.todo_list_widget)

        # ランダムやることおすすめボタン
        rec_button = QPushButton('今日やるおすすめ')
        rec_button.clicked.connect(self.rec_todo)

        #ボタン表示

        layout.addWidget(rec_button)

        # やること入力欄と日付入力欄、登録ボタンのレイアウト
        todo_input_layout = QHBoxLayout()
        self.todo_input = QLineEdit()
        self.todo_date = QDateEdit()
        self.todo_date.setCalendarPopup(True)  # 日付選択用のカレンダーポップアップを有効化
        self.todo_date.setDate(datetime.today().date()) #現在の日付に設定
        add_button = QPushButton('追加')
        add_button.clicked.connect(self.add_todo)
        add_button2 = QPushButton('完了')
        add_button2.clicked.connect(self.delete_todo)

        todo_input_layout.addWidget(self.todo_input)
        todo_input_layout.addWidget(self.todo_date)
        todo_input_layout.addWidget(add_button)
        todo_input_layout.addWidget(add_button2)

        # フォントの設定
        font = QFont()
        font.setPointSize(16)  # フォントサイズを16に設定
        self.todo_list_widget.setFont(font)

        layout.addLayout(todo_input_layout)

        # ウィンドウサイズの変更
        self.resize(600, 400)

    def add_todo(self):
        # やることと日付を取得
        todo_text = self.todo_input.text()
        todo_date = self.todo_date.date().toString("yyyy-MM-dd")
        if todo_text:
            #表示形式調整
            todo_item = f"{todo_text.ljust(30)} - {todo_date.rjust(15)}"

            # 日付文字列をdatetimeオブジェクトに変換
            date_str = todo_date
            dt2 = datetime.strptime(date_str, "%Y-%m-%d").date()
            dt1 = datetime.today().date()
            dt3 = dt2- dt1
            # ToDoアイテムを作成し、リストに追加
            todo_item = f"{todo_text} - {todo_date} - 締め切りまでの残り日数{dt3.days}日"
            item = QListWidgetItem(todo_item)
            self.todo_list_widget.addItem(item)
            # 入力欄をクリアし、日付を現在の日付にリセット
            self.todo_input.clear()
            self.todo_date.setDate(datetime.today().date())
            # ToDoリストを日付順にソート
            self.sort_todo_list()
            # リストを保存
            self.save_todo_list()

    def delete_todo(self, item):
        # 選択されたToDoアイテムを削除
        for item in self.todo_list_widget.selectedItems():
            self.todo_list_widget.takeItem(self.todo_list_widget.row(item))
        # リストを保存
        self.save_todo_list()

    def rec_todo(self):
        # ToDoリストのアイテム数が0の場合はエラーメッセージを表示
        if self.todo_list_widget.count() == 0:
            QMessageBox.warning(self, "現在", "todo要素はありません。")
            return

        # ランダムにToDoアイテムを選択してメッセージボックスで表示
        random_todo = random.choice([self.todo_list_widget.item(i).text() for i in range(self.todo_list_widget.count())])
        QMessageBox.information(self, "Random ToDo", random_todo)

    def sort_todo_list(self):
        # ToDoリストのアイテムを取得し、日付でソート
        items = sorted([self.todo_list_widget.item(i).text() for i in range(self.todo_list_widget.count())],
                        key=lambda x: datetime.strptime(x.split(" - ")[1], "%Y-%m-%d"))
        # ToDoリストをクリアして、ソート済みのアイテムを追加
        self.todo_list_widget.clear()
        self.todo_list_widget.addItems(items)
    def save_todo_list(self):
        # ToDoリストの内容をファイルに保存
        todo_items = [self.todo_list_widget.item(i).text() for i in range(self.todo_list_widget.count())]
        with open('todo_list.json', 'w') as f:
            json.dump(todo_items, f)

    def load_todo_list(self):
        # ファイルからToDoリストの内容を読み込んで表示
        if os.path.exists('todo_list.json'):
            with open('todo_list.json', 'r') as f:
                todo_items = json.load(f)
                # 残り日付を再構築
                todo_text = [todo.split(' - ')[0] for todo in todo_items]
                dates = [todo.split(' - ')[1] for todo in todo_items]
                for i in range(len(todo_text)):
                    # 要素を取り出して文字列型に変換する
                    first_element_as_str = str(dates[i])
                    date_str = first_element_as_str
                    dt2 = datetime.strptime(date_str, "%Y-%m-%d").date()
                    today = datetime.today().date()
                    global dt3
                    dt3 = dt2 - today

                    self.color_chenge()

                    #明日になった時の動作確認用
                    #tomorrow = today + timedelta(days=1)
                    #dt3 = dt2- tomorrow

                    # 結果の表示
                    global redtodo
                    if redtodo == 0:
                        todo_item = f"{todo_text[i]} - {dates[i]} - 締め切りまでの残り日数{dt3.days}日"
                    else:
                        todo_item = f"{todo_text[i]} - {dates[i]} - 締め切り日を過ぎています"
                    item = QListWidgetItem(todo_item)
                    self.todo_list_widget.addItem(item)

    def color_chenge(self):
        global dt3
        dt4 = float(dt3.days)
        if dt4 < 1:
            global redtodo
            redtodo = 1
        else:
            redtodo = 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    todo_app = TodoApp()
    todo_app.show()
    sys.exit(app.exec_())
