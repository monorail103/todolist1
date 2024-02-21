import Pyside11 as g
app = g.QApplication(g.sys.argv)
todo_app = g.TodoApp()
todo_app.show()
g.sys.exit(app.exec_())
