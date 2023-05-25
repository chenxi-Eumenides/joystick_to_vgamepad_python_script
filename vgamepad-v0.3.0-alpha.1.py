from threading import Thread
from time import sleep, time

from components.Gamepad import Gamepad
from components.Joystick import Joystick
from components.Sript import Script_Manager
from components.Keys import default_keys
from components.Setting import is_log


class Virtual_Gamepad():
    def __init__(self) -> None:
        """gamepad实例

        开始运行请使用start()函数
        """

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
            if not self.script_manager.running:
                self.joystick.__reset_skip__()
                # 检查历史按键是否符合脚本触发
                self.script_manager.__check_script__(
                    self.gamepad.history_keys_id)
            # 添加脚本按键

            # 处理手柄按键输入
            self.joystick.get_input_value(self.keys)
            # 更新所有按键
            # sleep(0.00005)
            self.gamepad.flush_vgamepad(self.keys)
            # 更新历史按键列表
            self.gamepad.__update_history_keys__(self.keys)
            #

            # 保存录制
            # if self.__recording__:
            #     for key_id, key_value in changed_keys:
            #         self.__record__(key_id, key_value)
            # 输出log
            if is_log:
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

    # error

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
    vg = Virtual_Gamepad()
    # vg.log = True
    vg.start()
