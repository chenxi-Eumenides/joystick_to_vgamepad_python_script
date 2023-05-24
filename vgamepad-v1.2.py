from typing import Union, TypeAlias, Callable
KEY_ID_TYPE: TypeAlias = int
KEY_VALUE_TYPE: TypeAlias = tuple[Union[bool, float]]


class Gamepad():
    def __init__(self) -> None:
        """gamepad实例

        开始运行请使用start()函数
        """
        self.__init_pygame__()
        self.__init_vgamepad__()
        self.__init_others__()
        self.__init_values__()
        self.__init_scripts__()
        pass

    class Script():
        def __init__(self, id: str, desc: str = '', keys: list[int] = [], sorted: bool = False, action: Union[Callable, list] = None) -> None:
            self.id: str = id
            self.desc: str = desc
            self.keys: list[int] = keys
            self.sorted: bool = sorted
            self.action: Union[Callable, list] = action
            pass

    def __init_pygame__(self) -> None:
        '''导入并初始化pygame
        '''
        try:
            # import pygame
            from pygame import init, joystick, event, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION, JOYAXISMOTION
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "需要 'pygame' ，请 ‘pip install pygame’ 安装。")

        init()
        joystic_count = joystick.get_count()
        if joystic_count > 1:
            print("有%d个手柄已连接，请输入需要的手柄(1-%d)。" % (joystic_count, joystic_count))
            joystic_count = int(input())
        self.__joystick__ = joystick.Joystick(joystic_count-1)
        self.__pygame_event__ = event
        self.__joystick__.init()
        self.__key_type__ = {
            'keyDown': JOYBUTTONDOWN,
            'keyUp': JOYBUTTONUP,
            'keyDpad': JOYHATMOTION,
            'keyAxis': JOYAXISMOTION,
        }
        pass

    def __init_vgamepad__(self) -> None:
        '''导入并初始化vgamepad
        '''
        try:
            # import vgamepad
            from vgamepad import VX360Gamepad, XUSB_BUTTON
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "需要 'vgamepad' ，请 ‘pip install vgamepad 安装。")

        self.__gamepad__ = VX360Gamepad()
        self.__gamepad__.reset()
        self.__gamepad_keys__ = XUSB_BUTTON
        pass

    def __init_others__(self) -> None:
        '''导入并继承一些其他模块
        '''
        try:
            from time import sleep, time
            from threading import Thread
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "需要 'time'。请 ‘pip install <模块名>’ 安装。")

        self.sleep = sleep
        self.time = time
        self.thread = Thread
        pass

    def __init_values__(self) -> None:
        '''初始化一些必备的初始值
        '''
        # 默认键值
        self.__default_keys_value__: dict[KEY_ID_TYPE, KEY_VALUE_TYPE] = {
            0: (False,),  # A
            1: (False,),  # B
            2: (False,),  # X
            3: (False,),  # Y
            4: (False,),  # LB
            5: (False,),  # RB
            6: (False,),  # -
            7: (False,),  # +
            8: (False,),  # LP
            9: (False,),  # RP
            10: (False,),  # left
            11: (False,),  # right
            12: (False,),  # up
            13: (False,),  # down
            14: (0.0, 0.0),  # L (x,y)
            15: (0.0, 0.0),  # R (x,y)
            16: (0.0,),  # LT
            17: (0.0,),  # RT
        }
        # 辅助记忆的按键名对应id
        self.keys_id: dict[str, KEY_ID_TYPE] = {
            'A': 0,
            'B': 1,
            'X': 2,
            'Y': 3,
            'LB': 4,
            'RB': 5,
            '-': 6,
            '+': 7,
            'LP': 8,
            'RP': 9,
            'left': 10,
            'right': 11,
            'up': 12,
            'down': 13,
            'L': 14,
            'R': 15,
            'LT': 16,
            'RT': 17,
        }
        # 辅助记忆的id对应按键名
        self.id_keys: dict[str, KEY_ID_TYPE] = {
            0: 'A',
            1: 'B',
            2: 'X',
            3: 'Y',
            4: 'LB',
            5: 'RB',
            6: '-',
            7: '+',
            8: 'LP',
            9: 'RP',
            10: 'right',
            11: 'left',
            12: 'up',
            13: 'down',
            14: 'L',
            15: 'R',
            16: 'LT',
            17: 'RT',
        }
        # 给 vgamepad 的输出信号
        self.__gamepad_key_id__ = [
            self.__gamepad_keys__.XUSB_GAMEPAD_A,
            self.__gamepad_keys__.XUSB_GAMEPAD_B,
            self.__gamepad_keys__.XUSB_GAMEPAD_X,
            self.__gamepad_keys__.XUSB_GAMEPAD_Y,
            self.__gamepad_keys__.XUSB_GAMEPAD_LEFT_SHOULDER,
            self.__gamepad_keys__.XUSB_GAMEPAD_RIGHT_SHOULDER,
            self.__gamepad_keys__.XUSB_GAMEPAD_BACK,
            self.__gamepad_keys__.XUSB_GAMEPAD_START,
            self.__gamepad_keys__.XUSB_GAMEPAD_LEFT_THUMB,
            self.__gamepad_keys__.XUSB_GAMEPAD_RIGHT_THUMB,
            self.__gamepad_keys__.XUSB_GAMEPAD_DPAD_LEFT,
            self.__gamepad_keys__.XUSB_GAMEPAD_DPAD_RIGHT,
            self.__gamepad_keys__.XUSB_GAMEPAD_DPAD_UP,
            self.__gamepad_keys__.XUSB_GAMEPAD_DPAD_DOWN,
            self.__gamepad__.left_joystick_float,
            self.__gamepad__.right_joystick_float,
            self.__gamepad__.left_trigger_float,
            self.__gamepad__.right_trigger_float,
        ]
        # 摇杆死区设置
        self.rocker_setting: dict[str, float] = {
            14: {
                'inside': 0.1,
                'outside': 0.1,
                'curve': None,
            },
            15: {
                'inside': 0.1,
                'outside': 0.1,
                'curve': None,
            },
            17: {
                'inside': 0.1,
                'outside': 0.1,
                'curve': None,
            },
            17: {
                'inside': 0.1,
                'outside': 0.1,
                'curve': None,
            },
        }
        # 历史按键列表
        self.__history_keys_list__: list[KEY_ID_TYPE] = []
        # 运行开始时间
        self.__start_time__: float = self.time()
        # 录制内容缓存
        self.__recording_cache__: list[str] = []
        # 录制文件保存路径
        self.record_file_path: str = './record.txt'
        # 标识符
        # 是否开始log
        self.log: bool = False
        # 是否在运行主循环
        self.__main_loop_running__: bool = False
        # 是否在运行脚本
        self.__script_running__: bool = False
        # 是否要跳过某些按键
        self.__skip__: dict[bool] = {
            'key': False,
            'dpad': False,
            'LR': False,
            'LRT': False,
        }
        # 是否在录制脚本
        self.__recording__: bool = False
        pass

    def __init_scripts__(self) -> None:
        # 不可按键触发的脚本列表
        self.scripts_list_with_no_keys: dict = {}
        # 可按键触发的脚本列表
        self.scripts_list_with_keys: dict = {}
        #
        self.__script_steps__ = []
        # 脚本运行开始时间
        self.__recording_start_time__: float = self.__start_time__
        # 添加菜单脚本
        self.scripts_list_with_keys['menu'] = self.Script(
            id='脚本选择',
            desc='选择执行的脚本',
            keys=[self.keys_id['up'], self.keys_id['A'], self.keys_id['X']],
            sorted=True,
            action=self.__script_menu__,
        )
        # 添加录制脚本
        self.scripts_list_with_keys['record'] = self.Script(
            id='录制按键',
            desc='录制按键并保存为文件',
            keys=[self.keys_id['left'], self.keys_id['A'], self.keys_id['X']],
            sorted=True,
            action=self.__record_start__,
        )
        pass

    def __main_loop__(self) -> None:
        '''主循环。处理流程手柄的接收与转发、脚本的检测和处理
        '''
        print("start to input")
        self.__main_loop_running__ = True
        axis_value: dict[KEY_ID_TYPE, KEY_VALUE_TYPE] = {
            14: (0.0, 0.0),  # L (x,y)
            15: (0.0, 0.0),  # R (x,y)
        }
        # 开始主循环
        while self.__main_loop_running__:
            # 检查历史按键是否符合脚本触发
            self.__check_script__()
            # 添加脚本按键

            # 处理手柄按键输入
            changed_value: dict[KEY_ID_TYPE, KEY_VALUE_TYPE] = axis_value
            skip_value: dict[KEY_ID_TYPE, KEY_VALUE_TYPE] = {}
            for event in self.__pygame_event__.get():
                # 按键按下
                if event.type == self.__key_type__['keyDown']:
                    if not self.__skip__['key']:
                        changed_value[event.button] = (True,)
                    else:
                        skip_value[event.button] = (True,)
                    pass
                # 按键松开
                elif event.type == self.__key_type__['keyUp']:
                    if not self.__skip__['key']:
                        changed_value[event.button] = (False,)
                    else:
                        skip_value[event.button] = (False,)
                    pass
                # 十字键
                elif event.type == self.__key_type__['keyDpad']:
                    # 左右
                    if event.value[0] == -1:
                        # 左
                        if not self.__skip__['dpad']:
                            changed_value[10] = (True,)
                        else:
                            skip_value[10] = (True,)
                        pass
                    elif event.value[0] == 1:
                        # 右
                        if not self.__skip__['dpad']:
                            changed_value[11] = (True,)
                        else:
                            skip_value[11] = (True,)
                        pass
                    else:
                        # 中间
                        if not self.__skip__['dpad']:
                            changed_value[10] = (False,)
                            changed_value[11] = (False,)
                        else:
                            skip_value[10] = (False,)
                            skip_value[11] = (False,)
                        pass
                    # 上下
                    if event.value[1] == 1:
                        # 上
                        if not self.__skip__['dpad']:
                            changed_value[12] = (True,)
                        else:
                            skip_value[12] = (True,)
                        pass
                    elif event.value[1] == -1:
                        # 下
                        if not self.__skip__['dpad']:
                            changed_value[13] = (True,)
                        else:
                            skip_value[13] = (True,)
                        pass
                    else:
                        # 中间
                        if not self.__skip__['dpad']:
                            changed_value[12] = (False,)
                            changed_value[13] = (False,)
                        else:
                            skip_value[12] = (False,)
                            skip_value[13] = (False,)
                        pass
                # 摇杆与ZL/RL
                elif event.type == self.__key_type__['keyAxis']:
                    if event.axis == 0 and not self.__skip__['LR']:
                        # LX 左右方向
                        changed_value[14] = (
                            self.__get_axis_value__(event.value, 14),
                            changed_value[14][1],
                        )
                        pass
                    elif event.axis == 1 and not self.__skip__['LR']:
                        # LX 上下方向
                        changed_value[14] = (
                            changed_value[14][0],
                            self.__get_axis_value__(-event.value, 14),
                        )
                        pass
                    elif event.axis == 2 and not self.__skip__['LR']:
                        # RX 左右方向
                        changed_value[15] = (
                            self.__get_axis_value__(event.value, 15),
                            changed_value[15][1],
                        )
                        pass
                    elif event.axis == 3 and not self.__skip__['LR']:
                        # RX 上下方向
                        changed_value[15] = (
                            changed_value[15][0],
                            self.__get_axis_value__(-event.value, 15),
                        )
                        pass
                    elif event.axis == 4 and not self.__skip__['LRT']:
                        # LT
                        changed_value[16] = (
                            self.__get_axis_value__(event.value, 16),
                        )
                        pass
                    elif event.axis == 5 and not self.__skip__['LRT']:
                        # RT
                        changed_value[17] = (
                            self.__get_axis_value__(event.value, 17),
                        )
                        pass
            # 更新所有按键
            self.sleep(0.00005)
            self.flush_vgamepad(changed_value)
            # 更新历史按键列表
            self.__update_history_keys_list__(changed_value)
            #

            # 保存当前的左右摇杆值
            axis_value = {
                14: changed_value[14],
                15: changed_value[15],
            }
            # 输出log
            if self.log:
                if abs(changed_value[14][0]) <= 0.0001 and abs(changed_value[14][1]) <= 0.0001:
                    changed_value.pop(14, None)
                if abs(changed_value[15][0]) <= 0.0001 and abs(changed_value[15][1]) <= 0.0001:
                    changed_value.pop(15, None)
                if changed_value != {}:
                    print(changed_value, self.__history_keys_list__)
        pass

    def __run_script__(self, name: str) -> None:
        self.__script_running__ = True
        pass

    def __stop_script__(self) -> None:
        self.__script_running__ = False
        self.__skip__['key'] = False
        self.__skip__['dpad'] = False
        self.__skip__['LR'] = False
        self.__skip__['LRT'] = False
        pass

    def __run_script_step__(self) -> None:
        key_id: int = 0
        key_value: tuple = ()
        return {key_id: key_value}

    def __check_script__(self) -> None:
        for name, script in self.scripts_list_with_keys.items():
            if len(script.keys) <= 0:
                continue
            if script.sorted:
                if script.keys == self.__history_keys_list__:
                    self.__run_script__(name)
                    pass
            else:
                if sorted(script.keys) == sorted(self.__history_keys_list__):
                    self.__run_script__(name)
                    pass
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

    def __update_history_keys_list__(self, keys: dict[KEY_ID_TYPE, KEY_VALUE_TYPE]) -> None:
        """根据本次按键变动, 维护一个有顺序的历史按键列表

        注意, 在python 3.7以下的版本中可能会造成按键太快, 导致无法正确识别按键谁在前谁在后的问题

        :param keys: 变动的键列表
        """
        for key_id, key_value in keys.items():
            if 0 <= key_id and key_id <= 13:
                # 如果是按下按键且没按下去过, 那么就往列表里添加这个键id
                if key_value[0] and key_id not in self.__history_keys_list__:
                    self.__history_keys_list__.append(key_id)
                # 如果是松开按键且按下去过, 那么就将这个列表里的键id及其之前的所有键id全删除
                elif not key_value[0] and key_id in self.__history_keys_list__:
                    del self.__history_keys_list__[:self.__history_keys_list__.index(
                        key_id)+1]
        pass

    def flush_vgamepad(self, keys: dict[KEY_ID_TYPE, KEY_VALUE_TYPE], delay: float = 0.00005) -> None:
        """更新给出的所有键

        :param keys: 键列表，KEY_ID_TYPE为0-17的整数，KEY_VALUE_TYPE为封装好的tuple
        :param delay: 更新手柄状态后的延迟, 默认 0.0001
        """
        for key_id, key_value in keys.items():
            if 0 <= key_id and key_id <= 13:
                if key_value[0]:
                    self.__gamepad__.press_button(
                        self.__gamepad_key_id__[key_id])
                else:
                    self.__gamepad__.release_button(
                        self.__gamepad_key_id__[key_id])
            elif 14 <= key_id and key_id <= 15:
                self.__gamepad_key_id__[key_id](*key_value)
            elif 16 <= key_id and key_id <= 17:
                self.__gamepad_key_id__[key_id](*key_value)
        self.__gamepad__.update()
        self.sleep(delay)
        pass

    def press_list(self, keys: dict[KEY_ID_TYPE, KEY_VALUE_TYPE], delay: float = 0.0, update=True) -> None:
        """按下给出的所有键

        :param keys: 键列表, KEY_ID_TYPE为0-17的整数, KEY_VALUE_TYPE为封装好的tuple
        :param delay: 更新虚拟手柄状态后的延迟, 默认 0.0
        :param update: 是否更新虚拟手柄状态, 默认 True
        """
        for key_id, key_value in keys.items():
            self.press(key_id, key_value, delay=0.0, update=False)
        if update:
            self.update()
        self.sleep(delay)
        pass

    def press(self, key_id: KEY_ID_TYPE, key_value: KEY_VALUE_TYPE, delay: float = 0.0, update=True) -> None:
        """按下单个按键

        :param key_id: 键ID, 0-17的整数
        :param key_value: 键值
        :param delay: 更新虚拟手柄状态后的延迟, 默认 0.0
        :param update: 是否更新虚拟手柄状态, 默认 True
        """
        if key_id < 14 and key_id >= 0:
            self.__gamepad__.press_button(self.__gamepad_key_id__[key_id])
        else:
            self.__gamepad_key_id__[key_id](*key_value)
        if update:
            self.update()
        self.sleep(delay)
        pass

    def release_list(self, keys: dict[KEY_ID_TYPE, KEY_VALUE_TYPE], delay: float = 0.0, update=True) -> None:
        """松开给出的所有键

        :param keys: 键列表, KEY_ID_TYPE为0-17的整数, KEY_VALUE_TYPE在这个函数中随意就行
        :param delay: 更新虚拟手柄状态后的延迟, 默认 0.0
        :param update: 是否更新虚拟手柄状态, 默认 True
        """
        for key_id in keys.keys():
            self.release(key_id, delay=0.0, update=False)
        if update:
            self.update()
        self.sleep(delay)
        pass

    def release(self, key_id: KEY_ID_TYPE, delay: float = 0.0, update=True) -> None:
        """松开单个按键

        :param key_id: 键ID, 0-17的整数
        :param delay: 更新虚拟手柄状态后的延迟, 默认 0.0
        :param update: 是否更新虚拟手柄状态, 默认 True
        """
        if key_id <= 13 and key_id >= 0:
            self.__gamepad__.press_button(self.__gamepad_key_id__[key_id])
        elif key_id >= 14 and key_id <= 15:
            self.__gamepad_key_id__[key_id](0.0, 0.0)
        elif key_id >= 16 and key_id <= 17:
            self.__gamepad_key_id__[key_id](0.0)
        if update:
            self.update()
        self.sleep(delay)
        pass

    def click_list(self, keys: dict[KEY_ID_TYPE, KEY_VALUE_TYPE], time: float = 0.1, delay: float = 0.0, update=True) -> None:
        """点按给出的所有按键

        :param keys: 键列表
        :param time: 按下时间, 默认 0.1s
        :param delay: 松开后的延迟时间, 默认 0.0s
        :param update: 是否更新虚拟手柄的状态, 默认 True, 为False时等于松开给出的所有按键
        """
        for key_id, key_value in keys.items():
            self.press(key_id, key_value, delay=time, update=False)
        if update:
            self.update()
        for key_id in keys.keys():
            self.release(key_id, delay=delay, update=False)
        if update:
            self.update()
        pass

    def click(self, key_id: KEY_ID_TYPE, key_value: KEY_VALUE_TYPE, time: float = 0.1, delay: float = 0.0, update=True) -> None:
        """点按单个按键

        :param key_id: 键ID
        :param key_value: 键值
        :param time: 按下时间, 默认 0.1s
        :param delay: 松开后的延迟时间, 默认 0.0s
        :param update: 是否更新虚拟手柄状态, 默认 True, 为False时等于松开这个按键
        """
        self.press(key_id, key_value, time, update)
        self.release(key_id, delay, update)
        pass

    def reset_vgamepad(self) -> None:
        """重置虚拟手柄至初始状态
        """
        self.__gamepad__.reset()
        pass

    def update(self) -> None:
        """将当前虚拟手柄的状态更新到实际输出中
        """
        self.__gamepad__.update()
        pass

    def start(self) -> None:
        """开始运行
        """
        self.__main_loop__()
        pass

    def create_values_for_BotW(self) -> None:
        """创建一些荒野之息中专用的值, 方便使用, 默认不创建
        """
        # 方便荒野之息中使用的按键对应表
        self.BotW_keys = {
            'run': {0: (None,)},
            'jump': {3: (None,)},
            'paragliders': {3: (None,)},
            'attack':  {2: (None,)},
            'power':  {4: (None,)},
            'defense':  {16: (0.99,)},
            'throw_weapon':  {},
            'bow':  ('RZ', 0.99),
            'gui_power':  'up',
            'gui_weapon':  'right',
            'gui_second_hand':  'left',
            'gui_horse':  'down',
            'confirm':  'B',
            'cancel':  'A',
            'open_backpack':  '+',
            'open_map':  '-',
            'move_front': ('L', 0.0, 0.99),
            'move_back': ('L', 0.0, -0.99),
            'move_left': ('L', -0.99, 0.0),
            'move_right': ('L', 0.99, 0.0),
            'backpack_switch_left': 'left',
            'backpack_switch_right':  'right',
            'backpack_switch_up':  'up',
            'backpack_switch_down':  'down',
            'backpack_switch_type_left': ('R', -0.99, 0.0),
            'backpack_switch_type_right': ('R', 0.99, 0.0),
            'backpack_switch_page_left':  'LT',
            'backpack_switch_page_right':  'RT',
            'gui_switch_left': ('LZ', 0.99),
            'gui_switch_right': ('RZ', 0.99),
        }

    def __script_menu__(self) -> None:
        if self.__recording__:
            self.__record_stop__()
        print("按键触发脚本有:")
        for script in self.scripts_list_with_keys.keys():
            print(
                f"   {script.id:<10} ({script.desc})\n",
                f"   {script.keys} {'有顺序' if script.sorted else '无顺序'}"
            )
        i = 0
        print("可选脚本有:")
        for script in self.scripts_list_with_no_keys.keys():
            print(
                f"{i:>3} : {script.id:<10} ({script.desc})\n",
            )
            i += 1
        pass

    def __record_start__(self) -> None:
        """开始录制按键
        """
        self.__recording__ = True
        self.__recording_start_time__ = self.time()
        self.__recording_cache__.append(
            f"{round(self.time()-self.__recording_start_time__,4):<7} : " +
            "-- Record START --" +
            "\n"
        )
        pass

    def __record_stop__(self) -> None:
        """停止录制按键并保存
        """
        self.__recording__ = False
        self.__recording_cache__.append(
            f"{round(self.time()-self.__recording_start_time__,4):<7} : " +
            "-- Record STOP --" +
            "\n"
        )
        with open(self.record_file_path, 'wt') as file:
            for line in self.__record_cache__:
                file.write(line)
        self.__record_cache__ = []
        pass

    def record(self, key_id: int, key_value: tuple) -> None:
        """录入按键信息

        :param key_id: 按键id
        :param key_value: 按键值
        """
        self.__record_cache__.append(
            f"{round(self.time()-self.__recording_start_time__,4):<7} : " +
            f"{key_id:<2} {key_value:<10} [" +
            "将%s键%s" % (self.id_keys[key_id], f"移至{key_value}" if type(key_value[0]) != bool else "按下" if key_value[0] else "松开") +
            "]\n"
        )
        pass

    # error

    def add_script(self, script, name: str, keys: list[str] = [], description: str = '', ordered: bool = True) -> int:
        '''
        添加自己的脚本。
        params:
            script      :  脚本函数。
            name        :  脚本名称。
            keys        :  脚本激活按键 (空列表为不激活)。
            description :  脚本描述。
            ordered     :  按键是否按照顺序 (False为无顺序)。
        '''
        if not callable(script):
            return 1
        try:
            self.all_scripts.append({
                'name': name,
                'description': description,
                'script': script,
                'keys': keys,
                'ordered': ordered,
            })
        except:
            return 1
        self.available_scripts = self.__get_available_scripts__(
            self.all_scripts)
        return 0

    @staticmethod
    def script_stop(instance) -> None:
        instance.__recording__ = False
        instance.running = False
        pass

    @staticmethod
    def script_help(instance) -> None:
        print("同时按住脚本设定的按键即可启用脚本。注意，有些脚本有按键顺序的要求。")
        print("无按键触发的可通过‘手动激活脚本’触发")
        print("脚本触发期间，无法操控（我懒得改多线程了）")
        print("觉得不满意的可以自行修改代码。")
        print("以下脚本可直接通过按键触发。")
        for script in instance.available_scripts:
            print(
                f"{script['name']}  :  {script['keys']} {'有顺序' if script['ordered'] else '无顺序'}")
        print("")
        pass

    @staticmethod
    def script_fly(instance) -> None:
        # 持盾往前跑后取消盾
        instance.press(instance.BotW_keys.defense, delay=1)
        instance.press(instance.BotW_keys.move_front, delay=0.3)
        instance.release(instance.BotW_keys.defense, delay=0.05)
        # 起跳并放圆形炸弹后拉弓
        instance.press(instance.BotW_keys.jump, delay=0.02)
        instance.press(instance.BotW_keys.power, delay=0.2)
        instance.press(instance.BotW_keys.bow, delay=0.05)
        instance.release(instance.BotW_keys.jump, delay=0.05)
        instance.release(instance.BotW_keys.power, delay=0.05)
        instance.release(instance.BotW_keys.bow, delay=0.05)
        # 切方形炸弹并放方形炸弹
        instance.press(instance.BotW_keys.gui_power, delay=0.05)
        instance.click(instance.BotW_keys.gui_switch_right,
                       time=0.2, delay=0.05)
        instance.release(instance.BotW_keys.gui_power, delay=0.05)
        instance.click(instance.BotW_keys.power, time=0.2, delay=0.05)
        # 切圆形炸弹
        instance.press(instance.BotW_keys.gui_power, delay=0.05)
        instance.click(instance.BotW_keys.gui_switch_left,
                       time=0.2, delay=0.05)
        instance.release(instance.BotW_keys.gui_power, delay=0.05)
        # 引爆
        instance.click(instance.BotW_keys.power, time=0.1, delay=0.05)
        instance.press(instance.BotW_keys.paragliders, delay=1)
        # for _ in range(10):
        #    instance.press(instance.BotW_keys.paragliders, delay=0.2)
        pass


if __name__ == "__main__":
    gp = Gamepad()
    gp.log = True
    gp.start()
