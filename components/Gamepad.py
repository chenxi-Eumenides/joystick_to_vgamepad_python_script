from vgamepad import VX360Gamepad, XUSB_BUTTON
from .Keys import Key
from time import sleep, time
from typing import Union


class Gamepad():
    def __init__(self) -> None:
        '''
        '''
        # 初始化gamepad
        self.vgamepad = VX360Gamepad()
        self.vgamepad.reset()

        # gamepad 键id
        self.ouput_id = [
            XUSB_BUTTON.XUSB_GAMEPAD_A,
            XUSB_BUTTON.XUSB_GAMEPAD_B,
            XUSB_BUTTON.XUSB_GAMEPAD_X,
            XUSB_BUTTON.XUSB_GAMEPAD_Y,
            XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
            XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
            XUSB_BUTTON.XUSB_GAMEPAD_BACK,
            XUSB_BUTTON.XUSB_GAMEPAD_START,
            XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
            XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
            XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
            XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
            XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
            XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
        ]
        # gamepad 摇杆函数
        self.ouput_func = [
            self.vgamepad.left_joystick_float,
            self.vgamepad.right_joystick_float,
            self.vgamepad.left_trigger_float,
            self.vgamepad.right_trigger_float,
        ]
        # self.ouput = self.ouput_id+self.ouput_func
        self.history_keys_id: list[int] = []
        # self.keys = keys
        pass

    def flush_vgamepad(self, keys: Union[dict[int, Key], list[Key]], delay: float = 0.00005) -> None:
        """当键的状态为1有更新时, 更新该键

        :param keys: 键列表
        :param delay: 更新手柄状态后的延迟, 默认 0.0001
        """
        if type(keys) == dict:
            keys_list: list[Key] = list(keys.values())
        elif type(keys) == list:
            keys_list: list[Key] = keys
        else:
            raise ValueError("keys类型不对, 应当是list或dict")
        for key in keys_list:
            if key.__status__ == 1:
                if key.type in ['key', 'dpad']:
                    if key.value[0]:
                        self.vgamepad.press_button(
                            self.ouput_id[key.id])
                    else:
                        self.vgamepad.release_button(
                            self.ouput_id[key.id])
                elif key.type in ['L', 'R', 'LRT']:
                    self.ouput_func[key.id-14](*key.value)
        self.sync_vgamepad()
        sleep(delay)
        pass

    def flush_vgamepad_for_script(self, action: dict[Union[int, str], tuple[Union[bool, float]]], keys: Union[dict[int, Key], list[Key]]) -> None:
        """根据键id与值, 直接更新虚拟手柄状态

        (由于无论是否有状态改变, flush_vgamepad都会同步vgamepad, 所以本函数不会同步键状态)

        :param actions: 脚本中的一步
        :param keys: 按键列表
        """
        if type(keys) == dict:
            keys_list: list[Key] = list(keys.values())
        elif type(keys) == list:
            keys_list: list[Key] = keys
        else:
            raise ValueError("keys类型不对, 应当是list或dict")
        for action_id, action_value in action.items():
            if type(action_id) == str:
                pass
            elif type(action_id) == int:
                keys_list[action_id].set_value(*action_value)
        pass

    def reset_by_key_type(self, key_types: list[str], keys: Union[dict[int, Key], list[Key]]) -> None:
        """将特定类型的按键重置

        :param key_types: 按键类型
        :param keys: 按键列表
        """
        if type(keys) == dict:
            keys_list: list[Key] = list(keys.values())
        elif type(keys) == list:
            keys_list: list[Key] = keys
        else:
            raise ValueError("keys类型不对, 应当是list或dict")
        for key_type in key_types:
            if key_types == 'key':
                for i in range(0, 10):
                    keys_list[i].set_value(False)
            elif key_type == 'dpad':
                for i in range(10, 14):
                    keys_list[i].set_value(False)
        pass

    def press(self, key: Key, delay: float = 0.0, update=True) -> None:
        """按下单个按键

        :param key: 键对象
        :param delay: 更新虚拟手柄状态后的延迟, 默认 0.0
        :param update: 是否更新虚拟手柄状态, 默认 True
        """
        if key.type in ['key', 'dpad']:
            self.vgamepad.press_button(self.ouput_id[key.id])
        elif key.type in ['L', 'R', 'LRT']:
            self.ouput_func[key.id-14](*key.value)
        key.set_status(4)
        if update:
            self.sync_vgamepad()
        sleep(delay)
        pass

    def release(self, key: Key, delay: float = 0.0, update=True) -> None:
        """松开单个按键

        :param key: 键对象
        :param delay: 更新虚拟手柄状态后的延迟, 默认 0.0
        :param update: 是否更新虚拟手柄状态, 默认 True
        """
        if key.type in ['key', 'dpad']:
            self.vgamepad.release_button(self.ouput_id[key.id])
        elif key.type in ['L', 'R', 'LRT']:
            self.ouput_func[key.id-14](*key.value)
        key.set_status(4)
        if update:
            self.sync_vgamepad()
        sleep(delay)
        pass

    def press_list(self, keys: Union[dict[int, Key], list[Key]], delay: float = 0.0, update=True) -> None:
        """按下给出的所有键

        :param keys: 键列表
        :param delay: 更新虚拟手柄状态后的延迟, 默认 0.0
        :param update: 是否更新虚拟手柄状态, 默认 True
        """
        if type(keys) == dict:
            keys_list: list[Key] = list(keys.values())
        elif type(keys) == list:
            keys_list: list[Key] = keys
        else:
            raise ValueError("keys类型不对, 应当是list或dict")
        for key in keys_list:
            self.press(key, delay=0.0, update=False)
        if update:
            self.sync_vgamepad()
        sleep(delay)
        pass

    def release_list(self, keys: Union[dict[int, Key], list[Key]], delay: float = 0.0, update=True) -> None:
        """松开给出的所有键

        :param keys: 键列表, KEY_ID_TYPE为0-17的整数, KEY_VALUE_TYPE在这个函数中随意就行
        :param delay: 更新虚拟手柄状态后的延迟, 默认 0.0
        :param update: 是否更新虚拟手柄状态, 默认 True
        """
        if type(keys) == dict:
            keys_list: list[Key] = list(keys.values())
        elif type(keys) == list:
            keys_list: list[Key] = keys
        else:
            raise ValueError("keys类型不对, 应当是list或dict")
        for key in keys_list:
            self.release(key, delay=0.0, update=False)
        if update:
            self.sync_vgamepad()
        sleep(delay)
        pass

    def click_list(self, keys: Union[dict[int, Key], list[Key]], time: float = 0.1, delay: float = 0.0, update=True) -> None:
        """点按给出的所有按键

        :param keys: 键列表
        :param time: 按下时间, 默认 0.1s
        :param delay: 松开后的延迟时间, 默认 0.0s
        :param update: 是否更新虚拟手柄的状态, 默认 True, 为False时等于松开给出的所有按键
        """
        if type(keys) == dict:
            keys_list: list[Key] = list(keys.values())
        elif type(keys) == list:
            keys_list: list[Key] = keys
        else:
            raise ValueError("keys类型不对, 应当是list或dict")
        for key in keys_list:
            self.press(key, delay=time, update=False)
        if update:
            self.sync_vgamepad()
        for key in keys_list:
            self.release(key, update=False)
        if update:
            self.sync_vgamepad()
        pass

    def click(self, key: Key, time: float = 0.1, delay: float = 0.0, update=True) -> None:
        """点按单个按键

        :param key: 键对象
        :param time: 按下时间, 默认 0.1s
        :param delay: 松开后的延迟时间, 默认 0.0s
        :param update: 是否更新虚拟手柄状态, 默认 True, 为False时等于松开这个按键
        """
        self.press(key, time, update)
        self.release(key, delay, update)
        pass

    def reset_one(self, key: Key) -> None:
        if key.type in ['key', 'dpad']:
            key.set_value(False)
        elif key.type in ['L', 'R']:
            key.set_value(0.0, 0.0)
        else:
            key.set_value(0.0)
        pass

    def reset_vgamepad(self) -> None:
        """重置虚拟手柄至初始状态
        """
        self.vgamepad.reset()
        pass

    def sync_vgamepad(self) -> None:
        """将当前状态同步到虚拟手柄中
        """
        self.vgamepad.update()
        pass

    def __update_history_keys__(self, keys: Union[dict[int, Key], list[Key]]) -> None:
        """维护一个有顺序的历史按键列表

        注意, 在python 3.7以下的版本中可能会造成按键太快, 导致无法正确识别按键谁在前谁在后的问题

        :param keys: 变动的键列表
        """
        if type(keys) == dict:
            keys_list: list[Key] = list(keys.values())
        elif type(keys) == list:
            keys_list: list[Key] = keys
        else:
            raise ValueError("keys类型不对, 应当是list或dict")
        for key in keys_list:
            if key.__status__ == 1 and key.type in ['key', 'dpad']:
                # 如果是按下按键且没按下去过, 那么就往列表里添加这个键id
                if key.value[0] and key.id not in self.history_keys_id:
                    self.history_keys_id.append(key.id)
                # 如果是松开按键且按下去过, 那么就将这个列表里的键id及其之前的所有键id全删除
                elif not key.value[0] and key.id in self.history_keys_id:
                    del self.history_keys_id[:self.history_keys_id.index(
                        key.id)+1]
        pass
