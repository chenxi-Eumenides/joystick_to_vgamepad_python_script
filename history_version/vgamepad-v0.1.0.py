class Gamepad():
    def __init__(self) -> None:
        '''
        需要安装 'pygame' 'vgamepad' 'time' 这三个模块：pip install <模块名>
        '''
        try:
            import pygame
            import vgamepad
            import threading
            from time import sleep, time
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "需要 'pygame' 'vgamepad' 'time' 三个模块。请 ‘pip install <模块名>’ 安装")

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

        # 初始化vgamepad
        self.__gamepad__ = vgamepad.VX360Gamepad()
        self.__gamepad__.reset()
        self.__gamepad_keys__ = vgamepad.XUSB_BUTTON

        # 继承函数
        self.sleep = sleep
        self.time = time
        
        # 获取线程对象
        self.threading = threading

        # 创建变量
        self.__create_private_values__()
        self.__create_public_values__()
        pass

    def start(self) -> None:
        self.__control_loop__()
        pass

    def stop(self) -> None:
        self.running = False
        pass

    def press(self, key: str, x: float = 1.0, y: float = 1.0, delay: float = 0.0, update: bool = True) -> None:
        if type(key) == tuple:
            x = key[1]
            y = key[2] if len(key) > 2 else y
            key = key[0]
        if key in self.__gamepad_output__['button']:
            self.press_button(key, delay=delay, update=update)
        elif key in self.__gamepad_output__['dpad']:
            self.press_dpad(key, delay=delay, update=update)
        elif key in self.__gamepad_output__['axis']:
            self.press_axis(key=key, x=x, y=y, delay=delay, update=update)
        pass

    def press_button(self, key: str, delay: float = 0.0, update: bool = True) -> None:
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

    def press_dpad(self, key: str, delay: float = 0.0, update: bool = True) -> None:
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

    def press_axis(self, key: str, x: float = 0.0, y: float = 0.0, delay: float = 0.0, update: bool = True) -> None:
        if type(key) == tuple:
            x = key[1]
            y = key[2] if len(key) > 2 else y
            key = key[0]
        if key in ['L', 'R']:
            self.__gamepad_output__['axis'][key](x, y)
            if self.log:
                print("press axis   : %s (%.2f , %.2f)" % (key, x, y))
            self.sleep(delay)
            if update:
                self.update()
        elif key in ['LZ', 'RZ']:
            self.__gamepad_output__['axis'][key](x)
            if self.log:
                print("press axis   : %s (%.2f)" % (key, x))
            self.sleep(delay)
            if update:
                self.update()
        pass

    def release(self, key: str, delay: float = 0.0, update: bool = True) -> None:
        if type(key) == tuple:
            key = key[0]
        if key in self.__gamepad_output__['button']:
            self.release_button(key=key, delay=delay, update=update)
        elif key in self.__gamepad_output__['dpad']:
            self.release_dpad(key=key, delay=delay, update=update)
        elif key in self.__gamepad_output__['axis']:
            self.release_axis(key=key, delay=delay, update=update)
        pass

    def release_button(self, key: str, delay: float = 0.0, update: bool = True) -> None:
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

    def release_dpad(self, key: str, delay: float = 0.0, update: bool = True) -> None:
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

    def release_axis(self, key: str, delay: float = 0.0, update: bool = True) -> None:
        if type(key) == tuple:
            key = key[0]
        if key in ['L', 'R']:
            self.__gamepad_output__['axis'][key](0.0, 0.0)
            if self.log:
                print("release axis   : %s" % (key))
            self.sleep(delay)
            if update:
                self.update()
        elif key in ['LZ', 'RZ']:
            self.__gamepad_output__['axis'][key](0.0)
            if self.log:
                print("release axis   : %s" % (key))
            self.sleep(delay)
            if update:
                self.update()
        pass

    def click(self, key: str, x: float = 0.0, y: float = 0.0, time: float = 0.2, delay: float = 0.0, update: bool = True) -> None:
        if type(key) == tuple:
            x = key[1]
            y = key[2] if len(key) > 2 else y
            key = key[0]
        if key in self.__gamepad_output__['button']:
            self.click_button(key=key, time=time, delay=delay, update=update)
        elif key in self.__gamepad_output__['dpad']:
            self.click_dpad(key=key, time=time, delay=delay, update=update)
        elif key in self.__gamepad_output__['axis']:
            self.click_axis(key=key, x=x, y=y, time=time,
                            delay=delay, update=update)
        pass

    def click_button(self, key: str, time: float = 0.2, delay: float = 0.0, update: bool = True) -> None:
        if key in self.__gamepad_output__['button']:
            self.press_button(key=key, delay=time, update=update)
            self.release_button(key=key, delay=delay, update=update)
        pass

    def click_dpad(self, key: str, time: float = 0.2, delay: float = 0.0, update: bool = True) -> None:
        if key in self.__gamepad_output__['dpad']:
            self.press_dpad(key=key, delay=time, update=update)
            self.release_dpad(key=key, delay=delay, update=update)
        pass

    def click_axis(self, key: str, x: float = 0.0, y: float = 0.0, time: float = 0.2, delay: float = 0.0, update: bool = True) -> None:
        if type(key) == tuple:
            x = key[1]
            y = key[2] if len(key) > 2 else y
            key = key[0]
        if key in self.__gamepad_output__['axis']:
            self.press_axis(key=key, x=x, y=y, delay=time, update=update)
            self.release_axis(key=key, delay=delay, update=update)
        pass

    def reset_all(self, update: bool = True) -> None:
        self.__gamepad__.reset()
        self.pressed_keys = []
        if update:
            self.update()
        pass

    def reset_pressed(self, update: bool = True) -> None:
        for _ in range(len(self.pressed_keys)):
            if self.pressed_keys[0] in ['up', 'down', 'left', 'right']:
                self.release_dpad(
                    self.pressed_keys[0], delay=0.0, update=False)
            else:
                self.release_button(
                    self.pressed_keys[0], delay=0.0, update=False)
        if update:
            self.update()
        pass

    def update(self) -> None:
        self.__gamepad__.update()
        pass

    def record(self, aciton: str, key: str, value: None = None) -> None:
        line = "%.4f : %s    %s" % (self.time()-self.__recording_start_time__, aciton, key) + (f"  {value}\n" if value else "\n")
        print(line)
        self.__record_cache__.append(line)
        pass
    
    def write(self, str:list[str]) -> None:
        with open(self.record_file, 'a+') as file:
            for line in self.__record_cache__:
                file.write(line)
        file.close()
        self.__record_cache__ = []
        pass
        
    def help(self,action:str='all') -> None:
        print("内容没完成")
        help_content={
            '脚本': [
                "按顺序同时按下 上键，A键，",
            ],
            '': [
            ],
            '': [
            ],
        }
        if action == 'all':
            for content in help_content:
                for line in content.values():
                    print(line)
        else:
            if action in help_content.keys():
                for line in help_content[action]:
                    print(line)
        pass
        
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
    def script_demo(instance) -> None:
        instance.press_button('B', delay=0.1)
        instance.release_button('B')
        instance.press_button('A', delay=0.1)
        instance.release_button('A')
        pass

    @staticmethod
    def script_record(instance) -> None:
        instance.__recording__ = True
        instance.__recording_start_time__ = instance.time()
        with open(instance.record_file, 'wt') as file:
            file.write("%.4f : %s\n" % (instance.time(
            )-instance.__recording_start_time__, "start recording"))
        file.close()
        pass

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
    def script_input(instance) -> None:
        if instance.__recording__:
            instance.__recording__ = False
        i = 0
        print("所有脚本有:")
        for script in instance.all_scripts:
            print(
                f" {i}. {script['name']}   :  {script['description']}  ({script['keys']})")
            i += 1
        print("输入序号激活脚本:")
        index = input()
        if index.isdigit():
            instance.__script_list__.append(instance.all_scripts[int(index)])
            print(f"{script['name']} 添加成功。")
        else:
            print("取消输入")
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

    def __control_loop__(self) -> None:
        print("开始转发手柄输入")
        self.running = True
        while self.running:
            loop = False

            # 执行脚本
            self.__start_script__()

            # 处理按键
            for event in self.__pygame_event__.get():
                loop = True
                # 按键按下
                if event.type == self.__joytype__['down']:
                    self.press_button(self.__joystick_input__[
                                      'button'][event.button])
                    if self.__recording__:
                        self.record('press  ', self.__joystick_input__[
                            'button'][event.button])
                    if self.__match_script__():
                        pass

                # 按键松开
                elif event.type == self.__joytype__['up']:
                    self.release_button(self.__joystick_input__[
                                        'button'][event.button])
                    if self.__recording__:
                        self.record('release', self.__joystick_input__[
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
                            if self.__recording__:
                                self.record('release', 'left')
                        if 'right' in self.pressed_keys:
                            self.release_dpad('right')
                            if self.__recording__:
                                self.record('release', 'right')
                    if key != '':
                        self.press_dpad(key)
                        if self.__recording__:
                            self.record('press  ', key)
                        if self.__match_script__():
                            pass
                    # 上下
                    if event.value[1] == 1:
                        key = 'up'
                    elif event.value[1] == -1:
                        key = 'down'
                    else:
                        key = ''
                        if 'up' in self.pressed_keys:
                            self.release_dpad('up')
                            if self.__recording__:
                                self.record('release', 'up')
                        if 'down' in self.pressed_keys:
                            self.release_dpad('down')
                            if self.__recording__:
                                self.record('release', 'down')
                    if key != '':
                        self.press_dpad(key)
                        if self.__recording__:
                            self.record('press  ', key)
                        if self.__match_script__():
                            pass

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
                            if self.__recording__:
                                self.record('press  ', 'L', (self.__axis__[
                                            'L'][0], self.__axis__['L'][1]))
                    elif event.axis == 1:
                        value = round(-event.value*0.99, 3)
                        if abs(self.__axis__['L'][1]+value) > step:
                            if abs(value) > 1.0*self.dead_range['L']:
                                self.__axis__['L'][1] = value
                            else:
                                self.__axis__['L'][1] = 0.0
                            self.press_axis(
                                'L', self.__axis__['L'][0], self.__axis__['L'][1])
                            if self.__recording__:
                                self.record('press  ', 'L', (self.__axis__[
                                            'L'][0], self.__axis__['L'][1]))
                    elif event.axis == 2:
                        value = round(event.value*0.99, 3)
                        if abs(self.__axis__['R'][0]-value) > step:
                            if abs(value) > 1.0*self.dead_range['R']:
                                self.__axis__['R'][0] = value
                            else:
                                self.__axis__['R'][0] = 0.0
                            self.press_axis(
                                'R', self.__axis__['R'][0], self.__axis__['R'][1])
                            if self.__recording__:
                                self.record('press  ', 'R', (self.__axis__[
                                            'R'][0], self.__axis__['R'][1]))
                    elif event.axis == 3:
                        value = round(-event.value*0.99, 3)
                        if abs(self.__axis__['R'][1]-value) > step:
                            if abs(value) > 1.0*self.dead_range['R']:
                                self.__axis__['R'][1] = value
                            else:
                                self.__axis__['R'][1] = 0.0
                            self.press_axis(
                                'R', self.__axis__['R'][0], self.__axis__['R'][1])
                            if self.__recording__:
                                self.record('press  ', 'R', (self.__axis__[
                                            'R'][0], self.__axis__['R'][1]))
                    elif event.axis == 4:
                        value = round((event.value+1.02)/2.1, 3)
                        if abs(self.__axis__['LZ']-value) > step:
                            if value > 1.0*self.dead_range['LZ']:
                                self.__axis__['LZ'] = value
                            else:
                                self.__axis__['LZ'] = 0.0
                            self.press_axis('LZ', self.__axis__['LZ'])
                            if self.__recording__:
                                self.record('press  ', 'LZ',
                                            (self.__axis__['LZ']))
                    elif event.axis == 5:
                        value = round((event.value+1.02)/2.1, 3)
                        if abs(self.__axis__['RZ']-value) > step:
                            if value > 1.0*self.dead_range['RZ']:
                                self.__axis__['RZ'] = value
                            else:
                                self.__axis__['RZ'] = 0.0
                            self.press_axis('RZ', self.__axis__['RZ'])
                            if self.__recording__:
                                self.record('press  ', 'RZ',
                                            (self.__axis__['RZ']))

            # 更新按键
            if loop:
                self.update()
                self.write(self.__record_cache__)
            self.__loop_count__ += 1
            self.sleep(0.0001)
        pass

    def __dict2obj__(self, d: dict) -> object:
        return type('', (), d)()

    def __match_script__(self) -> bool:
        if self.log:
            print(self.pressed_keys)
        for script in self.all_scripts:
            if len(list(script['keys'])) <= 0 or len(list(script['keys'])) != len(self.pressed_keys):
                continue
            if script['ordered']:
                if self.pressed_keys == script['keys']:
                    self.__script_list__.append(script)
                    return True
            else:
                if sorted(self.pressed_keys) == sorted(script['keys']):
                    self.__script_list__.append(script)
                    return True
        return False

    def __start_script__(self) -> None:
        for script in self.__script_list__:
            self.reset_pressed()
            print(f"script start   : {script['name']}")
            self.sleep(0.01)
            script['script'](self)
            self.sleep(0.01)
            print(f"script stop    : {script['name']}")
        self.__script_list__ = []
        pass

    def __create_public_values__(self) -> None:
        # 录制内容文件
        self.record_file: str = "record.txt"
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
            'backpack_switch_type_left': ('R', -0.99, 0.0),
            'backpack_switch_type_right': ('R', 0.99, 0.0),
            'backpack_switch_page_left':  'LT',
            'backpack_switch_page_right':  'RT',
            'gui_switch_left': ('LZ', 0.99),
            'gui_switch_right': ('RZ', 0.99),
        })
        # 所有的脚本
        self.all_scripts: list[dict] = [
            {
                'name': "demo",
                'description': "啥事不干。",
                'script': self.script_demo,
                'keys': [],
                'ordered': False,
            },
            {
                'name': "操作录制",
                'description': "录制所有的操作，再次打开‘手动激活脚本’可停止录制。",
                'script': self.script_record,
                'keys': [],
                'ordered': False,
            },
            {
                'name': "停止程序",
                'description': "停止程序",
                'script': self.script_stop,
                'keys': [],
                'ordered': False,
            },
            {
                'name': "帮助",
                'description': "输出帮助文本。",
                'script': self.script_help,
                'keys': [],
                'ordered': False,
            },
            {
                'name': "手动激活脚本",
                'description': "",
                'script': self.script_input,
                'keys': ['up', 'A', 'X'],
                'ordered': True,
            },
            {
                'name': "台阶风弹",
                'description': "在有高低差的地方风弹。",
                'script': self.script_fly,
                'keys': ['up', 'Y', 'A'],
                'ordered': True,
            },
        ]
        # 可用的脚本
        self.available_scripts = self.__get_available_scripts__(
            self.all_scripts)
        # 死区范围
        self.dead_range: dict = {'L': 0.1, 'R': 0.1, 'LZ': 0.1, 'RZ': 0.1}
        # log
        self.log: bool = False
        # 是否在运行
        self.running: bool = False
        pass

    def __create_private_values__(self) -> None:
        self.__script_list__ = []
        self.__loop_count__ = 0
        self.__recording__ = False
        self.__record_cache__: list[str] = []
        self.__recording_start_time__ = self.time()
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

    def __get_available_scripts__(self, all_scripts: list[dict]) -> list[dict]:
        available_scripts = []
        for script in all_scripts:
            if list(script['keys']) != []:
                available_scripts.append(script)
        return available_scripts


gp = Gamepad()
# gp.log = True
# gp.add_script(script=script_test_0, name='test', keys=['up','left','A','X'], ordered=False)
gp.start()
