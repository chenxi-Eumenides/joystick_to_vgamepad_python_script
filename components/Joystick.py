from pygame import init, joystick, event, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION, JOYAXISMOTION
from .Keys import Key


class Joystick():
    def __init__(self) -> None:
        # 初始化pygame
        init()
        joystic_count = joystick.get_count()
        if joystic_count > 1:
            print("有%d个手柄已连接，请输入需要的手柄(1-%d)。" % (joystic_count, joystic_count))
            joystic_count = int(input())
        # 选择手柄
        self.joystick = joystick.Joystick(joystic_count-1)
        # 初始化手柄
        self.joystick.init()
        self.event = event
        # 是否要跳过某些按键
        self.skip: dict[str, bool] = {
            'key': False,
            'dpad': False,
            'L': False,
            'R': False,
            'LRT': False,
        }
        pass

    def get_input_value(self, keys_list: dict[int, Key]) -> None:
        """接收实体手柄按键事件, 并更改按键值

        :param keys_list: 所有的按键字典
        """
        # 接收按键事件
        for event in self.event.get():
            # 按键按下
            if event.type == JOYBUTTONDOWN:
                status = 1 if not self.skip['key'] else 2
                keys_list[event.button].set_value(True, status=status)
            # 按键松开
            elif event.type == JOYBUTTONUP:
                status = 1 if not self.skip['key'] else 2
                keys_list[event.button].set_value(False, status=status)
                pass
            # 十字键
            elif event.type == JOYHATMOTION:
                # 左右
                status = 1 if not self.skip['dpad'] else 2
                key = {}
                if event.value[0] == -1:
                    # 左
                    key[10] = True
                elif event.value[0] == 1:
                    # 右
                    key[11] = True
                else:
                    # 中间
                    key[10] = False
                    key[11] = False
                # 上下
                if event.value[1] == 1:
                    # 上
                    key[12] = True
                elif event.value[1] == -1:
                    # 下
                    key[13] = True
                else:
                    # 中间
                    key[12] = False
                    key[13] = False
                    pass
                for key_id, key_value in key.items():
                    keys_list[key_id].set_value(key_value, status=status)
            # 摇杆与ZL/RL
            elif event.type == JOYAXISMOTION:
                if event.axis == 0:
                    # LX 左右方向
                    key_id = 14
                    key_value1 = self.__get_axis_value__(event.value, 14)
                    key_value2 = keys_list[14].value[1]
                    status = 1 if not self.skip['L'] else 2
                    pass
                elif event.axis == 1:
                    # LX 上下方向
                    key_id = 14
                    key_value1 = keys_list[14].value[0]
                    key_value2 = self.__get_axis_value__(-event.value, 14)
                    status = 1 if not self.skip['L'] else 2
                    pass
                elif event.axis == 2:
                    # RX 左右方向
                    key_id = 15
                    key_value1 = self.__get_axis_value__(event.value, 15)
                    key_value2 = keys_list[15].value[1]
                    status = 1 if not self.skip['R'] else 2
                    pass
                elif event.axis == 3:
                    # RX 上下方向
                    key_id = 15
                    key_value1 = keys_list[15].value[0]
                    key_value2 = self.__get_axis_value__(-event.value, 15)
                    status = 1 if not self.skip['R'] else 2
                    pass
                elif event.axis == 4:
                    # LT
                    key_id = 16
                    key_value1 = self.__get_axis_value__(event.value, 16)
                    key_value2 = 0.0
                    status = 1 if not self.skip['LRT'] else 2
                    pass
                elif event.axis == 5:
                    # RT
                    key_id = 17
                    key_value1 = self.__get_axis_value__(event.value, 17)
                    key_value2 = 0.0
                    status = 1 if not self.skip['LRT'] else 2
                    pass
                keys_list[key_id].set_value(
                    key_value1,
                    key_value2,
                    status=status,
                )
        pass

    def __get_axis_value__(self, value: float, key_id: int) -> float:
        """将原始值转换为输出值, 不限制输入大小

        :param value: 输入的值
        :param key_id: 输入值对应的键ID, 不同键对应了不同的转换方式
        :return: 输出值
        """
        result = 0.0
        if key_id == 14:
            result = value*0.99
        elif key_id == 15:
            result = value*0.99
        elif key_id == 16:
            result = (value+1.01)/2.05
        elif key_id == 17:
            result = (value+1.01)/2.05
        return round(result, 4)

    def __reset_skip__(self) -> None:
        self.skip: dict[str, bool] = {
            'key': False,
            'dpad': False,
            'L': False,
            'R': False,
            'LRT': False,
        }
        pass
