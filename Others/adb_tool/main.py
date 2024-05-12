import tkinter as tk
from ui.main_window import MainWindow


def main():
    root = tk.Tk()
    app = MainWindow(root)
    app.initialize_ui()

    # 开启事件监控
    root.mainloop()


if __name__ == '__main__':
    main()
