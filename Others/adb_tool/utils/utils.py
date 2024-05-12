class Util:
    """各种工具类函数"""
    @staticmethod
    def center_window(root, target_window, relative_size=3, calculate_size=0):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        width_min_size = 400

        width = max(screen_width // relative_size, width_min_size)
        height = max(screen_height // relative_size, calculate_size * 50)

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        target_window.geometry('%dx%d+%d+%d' % (width, height, x, y))
        target_window.update()

    @staticmethod
    def is_ip_legal(ip):
        """工具函数，判断传入ip是否合法"""

        # ip地址元素拆分
        segments = ip.split('.')
        if segments[0] == "":
            return "ip地址不能为空！请重新输入"
        elif len(segments) != 4:
            return "ip地址格式错误！请重新输入！"
        for segment in segments:
            if not segment.isdigit():
                return "ip地址只能输入纯数字！请重新输入！"
            num = int(segment)
            if num < 0 or num > 255:
                return "ip地址中有超出255的值！请重新输入！"
        return 0    # ip地址正确合法
