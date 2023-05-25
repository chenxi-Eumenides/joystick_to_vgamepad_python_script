from vgamepad import VX360Gamepad, XUSB_BUTTON
from .Keys import Key
from time import sleep
from typing import Union


class Gamepad():
    def __init__(self) -> None:
        '''导入并初始化vgamepad
        '''
        # 初始化gamepad
        self.gamepad = VX360Gamepad()
        self.gamepad.reset()

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
        self.ouput_func = [
            self.gamepad.left_joystick_float,
            self.gamepad.right_joystick_float,
            self.gamepad.left_trigger_float,
            self.gamepad.right_trigger_float,
        ]
        self.ouput = self.ouput_id+self.ouput_func
        self.history_keys_id: list[int] = []
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
                        self.gamepad.press_button(
                            self.ouput[key.id])
                    else:
                        self.gamepad.release_button(
                            self.ouput[key.id])
                elif key.type in ['LR', 'LRT']:
                    self.ouput[key.id](*key.value)
        self.gamepad.update()
        sleep(delay)
        pass

    def press(self, key: Key, delay: float = 0.0, update=True) -> None:
        """按下单个按键

        :param key: 键对象
        :param delay: 更新虚拟手柄状态后的延迟, 默认 0.0
        :param update: 是否更新虚拟手柄状态, 默认 True
        """
        if key.type in ['key', 'dpad']:
            self.gamepad.press_button(self.ouput[key.id])
        elif key.type in ['LR', 'LRT']:
            self.ouput[key.id](*key.value)
        key.set_status(4)
        if update:
            self.update()
        sleep(delay)
        pass

    def release(self, key: Key, delay: float = 0.0, update=True) -> None:
        """松开单个按键

        :param key_id: 键ID, 0-17的整数
        :param delay: 更新虚拟手柄状态后的延迟, 默认 0.0
        :param update: 是否更新虚拟手柄状态, 默认 True
        """
        if key.type in ['key', 'dpad']:
            self.gamepad.release_button(self.ouput[key.id])
        elif key.type in ['LR', 'LRT']:
            self.ouput[key.id](*key.value)
        key.set_status(4)
        if update:
            self.update()
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
            self.update()
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
            self.update()
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
            self.update()
        for key in keys_list:
            self.release(key, update=False)
        if update:
            self.update()
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

    def reset(self) -> None:
        """重置虚拟手柄至初始状态
        """
        self.gamepad.reset()
        pass

    def update(self) -> None:
        """将当前虚拟手柄的状态更新到实际输出中
        """
        self.gamepad.update()
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
