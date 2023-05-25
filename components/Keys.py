
from typing import Union, Callable
from .Setting import float_delta, used_key_count


class Key():
    """键类

    id(int): 键id\n
    type(str): 键类型 (key/dpad/LR/LRT)\n
    value(tuple(bool | float)): 键值\n
    status(bool): 键是否被更新
    """
    # 键id的数量
    count: int = used_key_count+4
    # 辅助记忆的按键名对应id
    name_to_id: dict[str, int] = {
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
    id_to_name: dict[int, str] = {
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
        10: 'left',
        11: 'right',
        12: 'up',
        13: 'down',
        14: 'L',
        15: 'R',
        16: 'LT',
        17: 'RT',
    }
    # 辅助记忆的id对应键类型
    id_to_type: dict[int, str] = {
        0: 'key',
        1: 'key',
        2: 'key',
        3: 'key',
        4: 'key',
        5: 'key',
        6: 'key',
        7: 'key',
        8: 'key',
        9: 'key',
        10: 'dpad',
        11: 'dpad',
        12: 'dpad',
        13: 'dpad',
        14: 'LR',
        15: 'LR',
        16: 'LRT',
        17: 'LRT',
    }

    def __init__(self, id: Union[int, str], value1: Union[bool, float] = None, value2: float = None) -> None:
        (self.id, self.name, self.type) = self.__check_id__(id)
        self.value = self.__check_value__(value1, value2)
        self.__status__: int = 0
        pass

    def __check_id__(self, id: Union[int, str]) -> tuple[int, str, str]:
        """检查id是否符合要求

        :param id: 键id
        :raises ValueError: 键id不符合要求
        :return: 键id
        """
        key_id = -1
        key_name = ''
        key_type = ''
        # 检查 id
        if type(id) == str:
            if id in Key.name_to_id.keys():
                key_id = Key.name_to_id[id]
            else:
                raise ValueError("id 的值应当在 Key.keys_to_id 的键中")
        elif type(id) == int:
            if 0 <= id and id < Key.count:
                key_type = Key.id_to_type[id]
                key_name = Key.id_to_name[id]
                key_id = int(id)
            else:
                raise ValueError("id 的值应当在 0~17 之间(包含)")
        else:
            raise ValueError("id 的值应当为 int 或 str")
        return (key_id, key_name, key_type)

    def __check_value__(self, value1: Union[bool, float] = None, value2: float = None) -> tuple[Union[bool, float]]:
        """检查键值是否符合要求

        :param value1: 值1, 不传入则为默认值
        :param value2: 值2, 不传入则为默认值
        :raises ValueError: 键id在 0~13 间时, value1 应当为 bool 值
        :raises ValueError: 键id为 14,15 时, value1 和 value2 应当为 float 值, 且在 -1.0~1.0 之间
        :raises ValueError: 键id为 16,17 时, value1 应当为 float 值, 且在0.0~1.0 之间
        :return tuple[bool | float]
        """
        # 检查按键的值
        if 0 <= self.id and self.id <= 13:
            if value1 == None:
                value1 = False
            if type(value1) == bool:
                return (value1,)
            else:
                raise ValueError("当 id 在 0~13 间时, value1 应当为 bool 类型")
        # 检查摇杆的值
        elif 14 <= self.id and self.id <= 15:
            if value1 == None:
                value1 = 0.0
            if value2 == None:
                value2 = 0.0
            if type(value1) == float and -1.0 <= value1 and value1 <= 1.0 and type(value2) == float and -1.0 <= value2 and value2 <= 1.0:
                return (value1, value2)
            else:
                raise ValueError(
                    "当 id 为 14,15 时, value1 和 value2 都需要是一个 float 值, 且值应当在 -1.0~1.0 之间(包含)")
        # 检查肩键的值
        elif 16 <= self.id and self.id <= 17:
            if value1 == None:
                value1 = False
            if type(value1) == float and -1.0 <= value1 and value1 <= 1.0:
                return (value1,)
            else:
                raise ValueError(
                    "当 id 为 16,17 时, value1 需要是一个 float 值, 且值应当在 -1.0~1.0 之间(包含)")
        return None

    def __value_eq__(self, value1: tuple[Union[bool, float]], value2: tuple[Union[bool, float]]) -> bool:
        if value1 == value2:
            return True
        elif self.type == 'LR':
            if abs(value1[0]-value2[0]) <= float_delta and abs(value1[1]-value2[1]) <= float_delta:
                return True
        elif self.type == 'LRT':
            if abs(value1[0]-value2[0]) <= float_delta:
                return True
        return False

    def set_value(self, value1: Union[bool, float] = None, value2: float = None, *, status: int = 1) -> 'Key':
        """设置键值

        :param value1: 值1, 不传入则为默认值
        :param value2: 值2, 不传入则为默认值
        """
        new_value = self.__check_value__(value1, value2)
        if not self.__value_eq__(new_value, self.value):
            self.set_status(status)
            self.value = new_value
        else:
            self.set_status(0)
        return self

    def set_status(self, status: int) -> 'Key':
        """设置键的状态

        :param status: 0 为 无状态;1 为有更新; 2 为被跳过; 3 为手动修改过键值
        """
        if status < 0 or status > 3:
            status = 0
        self.__status__ = status
        return self


default_keys: dict[int, Key] = {
    0: Key(0, False),  # A
    1: Key(1, False),  # B
    2: Key(2, False),  # X
    3: Key(3, False),  # Y
    4: Key(4, False),  # LB
    5: Key(5, False),  # RB
    6: Key(6, False),  # -
    7: Key(7, False),  # +
    8: Key(8, False),  # LP
    9: Key(9, False),  # RP
    10: Key(10, False),  # left
    11: Key(11, False),  # right
    12: Key(12, False),  # up
    13: Key(13, False),  # down
    14: Key(14, 0.0, 0.0),  # L (x,y)
    15: Key(15, 0.0, 0.0),  # R (x,y)
    16: Key(16, 0.0),  # LT
    17: Key(17, 0.0),  # RT
}
