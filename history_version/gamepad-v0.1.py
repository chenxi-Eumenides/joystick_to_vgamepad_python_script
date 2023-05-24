class Gamepad():
    def __init__(self) -> None:
        '''
        需要安装 'pygame' 'vgamepad' 'threading' 'time' 这四个模块：pip install <模块名>
        '''
        try:
            import pygame
            import vgamepad
            import threading
            from time import sleep, time
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "需要 'pygame' 'vgamepad' 'threading' 'time' 四个模块。")
        
        # 初始化pygame,获取手柄
        pygame.init()
        self.__joystick__ = pygame.joystick.Joystick(0)
        self.__joystick__.init()
        self.__pygame_event__ = pygame.event
        self.__joytype__ = {
            'down': pygame.JOYBUTTONDOWN,
            'up': pygame.JOYBUTTONUP,
            'axis': pygame.JOYAXISMOTION,
            'dpad': pygame.JOYHATMOTION,
        }

        # 初始化vgamepad,
        self.__gamepad__ = vgamepad.VX360Gamepad()
        self.__gamepad__.reset()
        self.__gamepad_keys__ = vgamepad.XUSB_BUTTON

        # 创建变量
        self.__create_private_values__()
        self.__create_public_values__()

        # 获取线程对象
        self.threading = threading

        # 公开变量与函数
        self.sleep = sleep
        self.time = time
        pass

    def start_script_loop(self) -> None:
        self.__thread_script_flag__ = True
        self.__thread_script__ = self.threading.Thread(
            target=self.__script_loop__)
        self.__thread_script__.start()
        pass

    def start_control_loop(self) -> None:
        self.__thread_control_flag__ = True
        self.__thread_control__ = self.threading.Thread(
            target=self.__control_loop__)
        self.__thread_control__.start()
        pass

    def stop_loop(self) -> None:
        self.__thread_control_flag__ = False
        self.__thread_script_flag__ = False
        pass

    def press(self, key: str, x: float = 1.0, y: float = 1.0, delay: float = 0.0, update: bool = False) -> None:
        if type(key) == tuple:
            x = key[1]
            y = key[2] if len(key) > 2 else y
            key = key[0]
        if key in self.__gamepad_output__['button']:
            self.press_button(key)
        elif key in self.__gamepad_output__['dpad']:
            self.press_dpad(key)
        elif key in self.__gamepad_output__['axis']:
            self.press_axis(key=key, x=x, y=y)
        self.sleep(delay)
        if update:
            self.update()
        pass

    def press_button(self, key: str, delay: float = 0.0, update: bool = False) -> None:
        if key in self.__gamepad_output__['button']:
            if key not in self.pressed_keys:
                self.pressed_keys.append(key)
            self.__gamepad__.press_button(
                self.__gamepad_output__['button'][key])
            if self.log:
                print("press button : %s" % (key))
            self.sleep(delay)
        if update:
            self.update()
        pass

    def press_dpad(self, key: str, delay: float = 0.0, update: bool = False) -> None:
        if key in self.__gamepad_output__['dpad']:
            if key not in self.pressed_keys:
                self.pressed_keys.append(key)
            self.__gamepad__.press_button(self.__gamepad_output__['dpad'][key])
            if self.log:
                print("press dpad   : %s" % (key))
            self.sleep(delay)
        if update:
            self.update()
        pass

    def press_axis(self, key: str, x: float, y: float = 0.0, delay: float = 0.0, update: bool = False) -> None:
        if type(key) == tuple:
            x = key[1]
            y = key[2] if len(key) > 2 else y
            key = key[0]
        if key in ['L', 'R']:
            self.__gamepad_output__['axis'][key](x, y)
            if self.log:
                print("press axis   : %s (%.2f , %.2f)" % (key, x, y))
            self.sleep(delay)
        elif key in ['LZ', 'RZ']:
            self.__gamepad_output__['axis'][key](x)
            if self.log:
                print("press axis   : %s (%.2f)" % (key, x))
            self.sleep(delay)
        if update:
            self.update()
        pass

    def release(self, key: str, delay: float = 0.0, update: bool = False) -> None:
        if type(key) == tuple:
            key = key[0]
        if key in self.__gamepad_output__['button']:
            self.release_button(key=key)
        elif key in self.__gamepad_output__['dpad']:
            self.release_dpad(key=key)
        elif key in self.__gamepad_output__['axis']:
            self.release_axis(key=key)
        self.sleep(delay)
        if update:
            self.update()
        pass

    def release_button(self, key: str, delay: float = 0.0, update: bool = False) -> None:
        if key in self.__gamepad_output__['button']:
            if key in self.pressed_keys:
                self.pressed_keys.remove(key)
            self.__gamepad__.release_button(
                self.__gamepad_output__['button'][key])
            if self.log:
                print("release button : %s" % (key))
            self.sleep(delay)
        if update:
            self.update()
        pass

    def release_dpad(self, key: str, delay: float = 0.0, update: bool = False) -> None:
        if key in self.__gamepad_output__['dpad']:
            if key in self.pressed_keys:
                self.pressed_keys.remove(key)
            self.__gamepad__.release_button(
                self.__gamepad_output__['dpad'][key])
            if self.log:
                print("release dpad   : %s" % (key))
            self.sleep(delay)
        if update:
            self.update()
        pass

    def release_axis(self, key: str, delay: float = 0.0, update: bool = False) -> None:
        if type(key) == tuple:
            key = key[0]
        if key in ['L', 'R']:
            self.__gamepad_output__['axis'][key](0.0, 0.0)
            if self.log:
                print("release axis   : %s" % (key))
            self.sleep(delay)
        elif key in ['LZ', 'RZ']:
            self.__gamepad_output__['axis'][key](0.0)
            if self.log:
                print("release axis   : %s" % (key))
            self.sleep(delay)
        if update:
            self.update()
        pass

    def click(self, key: str, time: float = 0.2, delay: float = 0.0, update: bool = False) -> None:
        if key in self.__gamepad_output__['button']:
            self.click_button(key=key, time=time)
        elif key in self.__gamepad_output__['dpad']:
            self.click_dpad(key=key, time=time)
        self.sleep(delay)
        if update:
            self.update()
        pass

    def click_button(self, key: str, time: float = 0.2, delay: float = 0.0, update: bool = False) -> None:
        if key in self.__gamepad_output__['button']:
            self.press_button(key=key)
            self.sleep(time)
            self.release_button(key=key)
            self.sleep(delay)
        if update:
            self.update()
        pass

    def click_dpad(self, key: str, time: float = 0.2, delay: float = 0.0, update: bool = False) -> None:
        if key in self.__gamepad_output__['dpad']:
            self.press_dpad(key=key)
            self.sleep(time)
            self.release_dpad(key=key)
            self.sleep(delay)
        if update:
            self.update()
        pass

    def reset(self, key: str, update: bool = False) -> None:
        self.release(key=key)
        if update:
            self.update()
        pass

    def reset_all(self) -> None:
        self.__gamepad__.reset()
        self.pressed_keys = []
        self.update()
        pass

    def reset_pressed(self) -> None:
        for key in self.pressed_keys:
            if key in ['up', 'down', 'left', 'right']:
                self.release_dpad(key)
            else:
                self.release_button(key)
        self.update()
        pass

    def update(self) -> None:
        self.__gamepad__.update()
        pass

    def add_script(self, script, script_name: str, keys: list[str] = [], script_description: str = '', sort: bool = True) -> int:
        '''
        添加自己的脚本。
        '''
        if not callable(script):
            return 1
        try:
            self.scripts[script_name] = {
                'name': script_name,
                'press_keys': keys,
                'description': script_description,
                'script': script,
                'sort': sort}
        except:
            return 1
        return 0

    def script_demo(instance) -> None:
        instance.press_button('B', update=True)
        instance.sleep(0.1)
        instance.release_button('B', update=True)
        instance.press_button('A', update=True)
        instance.sleep(0.1)
        instance.release_button('A', update=True)
        pass

    def script_fly(instance) -> None:
        instance.sleep(1)
        # 持盾往前跑后取消盾
        instance.press(instance.BotW_keys.defense, delay=0.5, update=True)
        instance.press(instance.BotW_keys.move_front, delay=0.05, update=True)
        instance.release(instance.BotW_keys.defense, delay=0.05, update=True)
        # 起跳并放圆形炸弹后拉弓
        instance.press(instance.BotW_keys.jump, delay=0.05, update=True)
        instance.press(instance.BotW_keys.power, delay=0.05, update=True)
        instance.press(instance.BotW_keys.bow, delay=0.05, update=True)
        instance.release(instance.BotW_keys.jump, delay=0.05, update=True)
        instance.release(instance.BotW_keys.power, delay=0.05, update=True)
        instance.release(instance.BotW_keys.bow, delay=0.05, update=True)
        # 切方形炸弹并放方形炸弹
        instance.press(instance.BotW_keys.gui_power, delay=0.05, update=True)
        instance.click(instance.BotW_keys.gui_switch_right,
                       delay=0.05, update=True)
        instance.release(instance.BotW_keys.gui_power, delay=0.05, update=True)
        instance.click(instance.BotW_keys.power, delay=0.05, update=True)
        # 切圆形炸弹
        instance.press(instance.BotW_keys.gui_power, delay=0.05, update=True)
        instance.click(instance.BotW_keys.gui_switch_left,
                       delay=0.05, update=True)
        instance.release(instance.BotW_keys.gui_power, delay=0.05, update=True)
        # 引爆
        instance.click(instance.BotW_keys.power, delay=0.05, update=True)
        instance.press(instance.BotW_keys.paragliders, delay=0.05, update=True)
        instance.sleep(1)
        for _ in range(10):
            instance.press(instance.BotW_keys.paragliders,
                           delay=0.05, update=True)
            instance.sleep(0.1)
        pass

    def __control_loop__(self) -> None:
        print("开始转发手柄输入")
        while self.__thread_control_flag__:
            loop = False

            # 处理按键
            events = self.__pygame_event__.get()
            print(events) if events != [] else 1
            for event in events:
                loop = True
                # 按键按下
                if event.type == self.__joytype__['down']:
                    self.press_button(self.__joystick_input__[
                        'button'][event.button])

                # 按键松开
                elif event.type == self.__joytype__['up']:
                    self.release_button(self.__joystick_input__[
                                        'button'][event.button])

                # 十字键
                elif event.type == self.__joytype__['dpad']:
                    # 左右
                    if event.value[0] == 1:
                        key = 'right'
                    elif event.value[0] == -1:
                        key = 'left'
                    else:
                        key = ''
                        if 'left' in self.pressed_keys:
                            self.release_dpad('left')
                        if 'right' in self.pressed_keys:
                            self.release_dpad('right')
                    if key != '':
                        self.press_dpad(key)
                    # 上下
                    if event.value[1] == 1:
                        key = 'up'
                    elif event.value[1] == -1:
                        key = 'down'
                    else:
                        key = ''
                        if 'up' in self.pressed_keys:
                            self.release_dpad('up')
                        if 'down' in self.pressed_keys:
                            self.release_dpad('down')
                    if key != '':
                        self.press_dpad(key)

                # 摇杆与ZL/RL
                elif event.type == self.__joytype__['axis']:
                    step = 0.02
                    if event.axis == 0:
                        value = round(event.value*0.99, 3)
                        if abs(self.__axis__['L'][0]-value) > step:
                            if abs(value) > 1.0*self.dead_range['L']:
                                self.__axis__['L'][0] = value
                            else:
                                self.__axis__['L'][0] = 0.0
                            self.press_axis(
                                'L', self.__axis__['L'][0], self.__axis__['L'][1])
                    elif event.axis == 1:
                        value = round(-event.value*0.99, 3)
                        if abs(self.__axis__['L'][1]+value) > step:
                            if abs(value) > 1.0*self.dead_range['L']:
                                self.__axis__['L'][1] = value
                            else:
                                self.__axis__['L'][1] = 0.0
                            self.press_axis(
                                'L', self.__axis__['L'][0], self.__axis__['L'][1])
                    elif event.axis == 2:
                        value = round(event.value*0.99, 3)
                        if abs(self.__axis__['R'][0]-value) > step:
                            if abs(value) > 1.0*self.dead_range['R']:
                                self.__axis__['R'][0] = value
                            else:
                                self.__axis__['R'][0] = 0.0
                            self.press_axis(
                                'R', self.__axis__['R'][0], self.__axis__['R'][1])
                    elif event.axis == 3:
                        value = round(-event.value*0.99, 3)
                        if abs(self.__axis__['R'][1]-value) > step:
                            if abs(value) > 1.0*self.dead_range['R']:
                                self.__axis__['R'][1] = value
                            else:
                                self.__axis__['R'][1] = 0.0
                            self.press_axis(
                                'R', self.__axis__['R'][0], self.__axis__['R'][1])
                    elif event.axis == 4:
                        value = round((event.value+1.02)/2.05, 3)
                        if abs(self.__axis__['LZ']-value) > step:
                            if value > 1.0*self.dead_range['LZ']:
                                self.__axis__['LZ'] = value
                            else:
                                self.__axis__['LZ'] = 0.0
                            self.press_axis('LZ', self.__axis__['LZ'])
                    elif event.axis == 5:
                        value = round((event.value+1.02)/2.05, 3)
                        if abs(self.__axis__['RZ']-value) > step:
                            if value > 1.0*self.dead_range['RZ']:
                                self.__axis__['RZ'] = value
                            else:
                                self.__axis__['RZ'] = 0.0
                            self.press_axis('RZ', self.__axis__['RZ'])

            # 更新按键
            if loop:
                self.update()
            self.__loop_count__ += 1
            self.sleep(0.0001)
        pass

    def __start_script__(self) -> None:
        for script in self.__script_list__:
            # self.reset_all()
            self.sleep(0.01)
            print(f"script start   : {script['name']}")
            script['script'](self)
            self.sleep(0.01)
            print(f"script stop    : {script['name']}")
        self.__script_list__ = []
        pass

    def __script_loop__(self) -> None:
        while self.__thread_script_flag__:
            print("script loop started")
            self.sleep(1)
        pass

    def __create_public_values__(self) -> None:
        # 按下去的键
        self.pressed_keys = []
        # 可使用的按键
        self.keys = ['A',  'B', 'X', 'Y', 'LT', 'RT', '-', '+', 'LP',
                     'RP', 'left', 'right', 'up', 'down', 'L', 'R', 'LZ', 'RZ']
        # 方便荒野之息中使用的按键对应表
        self.BotW_keys = self.__dict2obj__({
            'run': 'A',
            'jump': 'Y',
            'paragliders': 'Y',
            'attack':  'X',
            'power':  'LT',
            'defense':  ('LZ', 0.99),
            'throw_weapon':  'RT',
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
            'backpack_switch_type_left': ('L', -0.99, 0.0),
            'backpack_switch_type_right': ('L', 0.99, 0.0),
            'backpack_switch_page_left':  'LT',
            'backpack_switch_page_right':  'RT',
            'gui_switch_left': ('L', -0.99, 0.0),
            'gui_switch_right': ('L', 0.99, 0.0),
        })
        # 内置的脚本列表
        self.scripts = self.__get_script__()
        # 死区范围
        self.dead_range = {'L': 0.1, 'R': 0.1, 'LZ': 0.1, 'RZ': 0.1}
        # log
        self.log: bool = False
        # 是否在运行
        self.running: bool = False
        pass

    def __create_private_values__(self) -> None:
        self.__script_list__ = []
        self.__loop_count__ = 0
        self.__thread_control_flag__ = True
        self.__thread_script_flag__ = True
        # 左右摇杆的位置
        self.__axis__ = {
            'L': [0.0, 0.0],
            'R': [0.0, 0.0],
            'LZ': 0.0,
            'RZ': 0.0
        }
        # 从 pygame 中获取的 手柄输入信号 的对应表
        self.__joystick_input__ = {
            'button': {
                0: 'A',
                1: 'B',
                2: 'X',
                3: 'Y',
                4: 'LT',
                5: 'RT',
                6: '-',
                7: '+',
                8: 'LP',
                9: 'RP',
            },

        }
        # 给 vgamepad 的输出信号 的对应表
        self.__gamepad_output__ = {
            'button': {
                'A': self.__gamepad_keys__.XUSB_GAMEPAD_A,
                'B': self.__gamepad_keys__.XUSB_GAMEPAD_B,
                'X': self.__gamepad_keys__.XUSB_GAMEPAD_X,
                'Y': self.__gamepad_keys__.XUSB_GAMEPAD_Y,
                'LT': self.__gamepad_keys__.XUSB_GAMEPAD_LEFT_SHOULDER,
                'RT': self.__gamepad_keys__.XUSB_GAMEPAD_RIGHT_SHOULDER,
                '-': self.__gamepad_keys__.XUSB_GAMEPAD_BACK,
                '+': self.__gamepad_keys__.XUSB_GAMEPAD_START,
                'LP': self.__gamepad_keys__.XUSB_GAMEPAD_LEFT_THUMB,
                'RP': self.__gamepad_keys__.XUSB_GAMEPAD_RIGHT_THUMB,
            },
            'dpad': {
                'left': self.__gamepad_keys__.XUSB_GAMEPAD_DPAD_LEFT,
                'right': self.__gamepad_keys__.XUSB_GAMEPAD_DPAD_RIGHT,
                'up': self.__gamepad_keys__.XUSB_GAMEPAD_DPAD_UP,
                'down': self.__gamepad_keys__.XUSB_GAMEPAD_DPAD_DOWN,
            },
            'axis': {
                'L': self.__gamepad__.left_joystick_float,
                'R': self.__gamepad__.right_joystick_float,
                'LZ': self.__gamepad__.left_trigger_float,
                'RZ': self.__gamepad__.right_trigger_float,
            },
        }
        pass

    def __get_script__(self) -> None:
        # 内置的脚本列表
        return {
            "demo": {
                'name': "demo脚本",
                'description': "啥事不干。",
                'script': self.script_demo,
                'press_keys': [],
                'sort': False,
            },
            "fly": {
                'name': "台阶风弹",
                'description': "在有高低差的地方风弹。",
                'script': self.script_fly,
                'press_keys': ['up', 'A', 'Y'],
                'sort': True,
            },
        }
        pass

    def __dict2obj__(self, d: dict) -> object:
        return type('', (), d)()


gp = Gamepad()
gp.log = True
gp.start_control_loop()
# gp.start_script_loop()
input()
gp.stop_loop()
