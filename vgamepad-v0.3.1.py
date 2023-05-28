from time import time

from components.Gamepad import Gamepad
from components.Joystick import Joystick
from components.Sript import Script_Manager, Script
from components.Keys import default_keys, Key
from components.Setting import is_log, translation, language, float_delta


class Virtual_Gamepad():
    def __init__(self) -> None:
        """gamepad实例

        开始运行请使用start()函数
        """

        # 加载设置
        self.language = language
        self.translation = translation
        self.log = is_log

        # 初始化
        self.joystick = Joystick()
        self.gamepad = Gamepad()
        self.script_manager = Script_Manager()
        self.keys = default_keys

        # 运行开始时间
        self.__start_time__: float = time()

        # 标识符
        # 是否在运行主循环
        self.__main_loop_running__: bool = False
        pass

    def __main_loop__(self) -> None:
        '''主循环。处理流程手柄的接收与转发、脚本的检测和处理
        '''
        print("start to input")
        # 开始主循环
        while self.__main_loop_running__:
            # 重置按键状态
            for key in self.keys.values():
                key.set_status(0)
            # 脚本运行相关
            if not self.script_manager.running and time()-self.script_manager.last_time >= self.script_manager.script_cooldown_time+float_delta:
                self.joystick.__reset_skip__()
                # 检查历史按键是否符合脚本触发
                self.script_manager.__check_script__(
                    self.gamepad.history_keys_id)
            elif self.script_manager.running_script == None and self.script_manager.next_script != None:
                # 如果当前没有正在运行的脚本, 但有还没运行的脚本, 就运行下一个脚本
                # self.gamepad.reset_one(
                #     self.keys[self.gamepad.history_keys_id[-1]])
                self.gamepad.reset_by_key_type(['key', 'dpad'], self.keys)
                self.script_manager.__run_script__(
                    self.script_manager.next_script)
            elif self.script_manager.running_script != None and self.script_manager.running:
                # 如果 当前有正在运行的脚本, 就执行脚本内容
                if self.script_manager.need_keys_update:
                    # 根据脚本设置需要跳过的按键类型
                    self.joystick.skip = self.script_manager.running_script.skip_key_type
                    # 如果到了需要更新按键的时间
                    if time()-self.script_manager.last_time >= self.script_manager.wait_time + float_delta:
                        try:
                            # 获取迭代值
                            next_step = next(
                                self.script_manager.script_steps_iter)
                            # 更新手柄
                            self.gamepad.flush_vgamepad_for_script(
                                next_step, self.keys)
                            # 更新当前时间
                            self.script_manager.last_time = time()
                            # 获取并更新下一步的间隔时间
                            self.script_manager.wait_time = next_step["delay"]
                        except StopIteration:
                            # 如果迭代到底了, 就停止脚本
                            self.script_manager.__stop_script__()
            # 处理手柄按键输入
            self.joystick.get_input_value(self.keys)
            # 更新所有按键
            # sleep(0.00005)
            self.gamepad.flush_vgamepad(self.keys)
            # 更新历史按键列表
            self.gamepad.__update_history_keys__(self.keys)
            # 保存录制
            if self.script_manager.__recording__:
                self.script_manager.__record__(self.keys)
            # 输出log
            if self.log:
                update = {}
                for key in self.keys.values():
                    if key.__status__ == 1:
                        update[key.id] = key.value
                if update != {}:
                    print(update, "  -  ", self.gamepad.history_keys_id)
        pass

    def start(self) -> None:
        """开始运行
        """
        self.__main_loop_running__ = True
        self.__main_loop__()
        pass

    def create_values_for_BotW(self) -> None:
        """创建一些荒野之息中专用的值, 方便使用, 默认不创建
        """
        # 方便荒野之息中使用的按键对应表
        self.BotW_keys = {
            'run': {Key.name_to_id['A']: (None,)},
            'jump': {Key.name_to_id['Y']: (None,)},
            'paragliders': {Key.name_to_id['Y']: (None,)},
            'attack':  {Key.name_to_id['X']: (None,)},
            'power':  {Key.name_to_id['LB']: (None,)},
            'defense':  {Key.name_to_id['LT']: (0.99,)},
            'throw_weapon':  {Key.name_to_id['R']: (None,)},
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


if __name__ == "__main__":
    vg = Virtual_Gamepad()
    # 添加荒野之息飞弹脚本
    vg.script_manager.scripts_list_with_keys.append(Script(
        script_id=translation.get_from_key('botw_fly_script_name'),
        desc=translation.get_from_key('botw_fly_script_desc'),
        keys=[Key.name_to_id['up'], Key.name_to_id['A'], Key.name_to_id['Y']],
        sorted=True,
        action=[
            # 持盾往前跑后取消盾
            {"delay": 1, Key.name_to_id['LT']: (0.99,), },
            {"delay": 0.05, Key.name_to_id['L']:(0.0, 0.99), Key.name_to_id['LT']:(0.0,), Key.name_to_id['A']:(True,)},
            # 起跳并放圆形炸弹后拉弓
            {"delay": 0.05, Key.name_to_id['Y']:(True,)},
            {"delay": 0.1, Key.name_to_id['LB']:(True,)},
            {"delay": 0.05, Key.name_to_id['RT']:(0.9,)},
            {"delay": 0.02, Key.name_to_id['Y']:(False,), Key.name_to_id['LB']:(False,)},
            {"delay": 0.05, Key.name_to_id['RT']:(0.0,)},
            # 切方形炸弹并放方形炸弹
            {"delay": 0.05, Key.name_to_id['up']:(True,)},
            {"delay": 0.1, Key.name_to_id['RB']:(True,)},
            {"delay": 0.05, Key.name_to_id['RB']:(False,)},
            {"delay": 0.05, Key.name_to_id['up']:(False,)},
            {"delay": 0.1, Key.name_to_id['LB']:(True,)},
            {"delay": 0.05, Key.name_to_id['LB']:(False,)},
            # 切圆形炸弹
            {"delay": 0.05, Key.name_to_id['up']:(True,)},
            {"delay": 0.1, Key.name_to_id['LB']:(True,)},
            {"delay": 0.05, Key.name_to_id['LB']:(False,)},
            {"delay": 0.05, Key.name_to_id['up']:(False,)},
            # 引爆
            {"delay": 0.1, Key.name_to_id['LB']:(True,)},
            {"delay": 1.5, Key.name_to_id['LB']:(False,)},
            # 开伞
            {"delay": 0.05, Key.name_to_id['Y']:(True,)},
        ],
        skip_key_type={
            'key': True,
            'dpad': True,
            'L': True,
            'R': True,
            'LRT': True,
        }
    ))
    vg.log = True
    vg.start()
