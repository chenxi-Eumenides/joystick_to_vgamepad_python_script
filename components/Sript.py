from typing import Union, Callable
from .Setting import record_file_path
from .Keys import Key
from time import time


class Script():
    """脚本类

    script_id: 脚本的id\n
    desc: 脚本的描述\n
    keys: 脚本的触发按键, 为空列表则需要通过菜单脚本触发\n
    sorted: 脚本按键是否有顺序要求, True 为有按键顺序要求\n
    action: 脚本执行的动作, 如果为函数对象, 则为执行函数, 若为列表, 则按列表内容执行按键
    """

    def __init__(self, script_id: str, desc: str = '', keys: list[int] = [], sorted: bool = False, action: Union[Callable, list] = None) -> None:
        """脚本类

        :param script_id: 脚本的id
        :param desc: 脚本的描述
        :param keys: 脚本的触发按键, 为空列表则需要通过菜单脚本触发
        :param sorted: 脚本按键是否有顺序要求, True 为有按键顺序要求
        :param action: 脚本执行的动作, 如果为函数对象, 则为执行函数, 若为列表, 则按列表内容执行按键
        """
        self.script_id: str = script_id
        self.desc: str = desc
        self.keys: list[int] = keys
        self.sorted: bool = sorted
        self.action: Union[Callable, list] = action
        self.__check_valid__()
        pass

    def __check_valid__(self) -> None:
        if type(self.script_id) != str:
            raise ValueError("id 需要是一个 str 值")
        if type(self.desc) != str:
            raise ValueError("desc 需要是一个 str 值")
        if type(self.keys) != list:
            raise ValueError("keys 需要是一个 list 值")
        if type(self.sorted) != bool:
            raise ValueError("sorted 需要是一个 bool 值")
        if not callable(self.action) and type(self.action) != list:
            raise ValueError("acation 需要是一个 list 值或者是 可调用的函数")
        pass


class Script_Manager():
    def __init__(self) -> None:
        # 是否在运行脚本
        self.running: bool = False
        # 不可按键触发的脚本列表
        self.scripts_list_with_no_keys: list[Script] = []
        # 可按键触发的脚本列表
        self.scripts_list_with_keys: list[Script] = []
        #
        self.__script_steps__ = []
        # 是否在录制脚本
        self.__recording__: bool = False
        # 录制内容缓存
        self.__recording_cache__: list[str] = []
        # 脚本运行开始时间
        self.__recording_start_time__: float = time()
        # 添加菜单脚本
        self.scripts_list_with_keys.append(Script(
            script_id='脚本选择',
            desc='选择执行的脚本',
            keys=[Key.name_to_id['up'], Key.name_to_id['A'], Key.name_to_id['X']],
            sorted=True,
            action=self.__script_menu__,
        ))
        # 添加录制脚本
        self.scripts_list_with_keys.append(Script(
            script_id='录制按键',
            desc='录制按键并保存为文件',
            keys=[Key.name_to_id['left'],
                  Key.name_to_id['A'], Key.name_to_id['X']],
            sorted=True,
            action=self.__record_start__,
        ))

        pass

    # x
    def __run_script__(self, script: Script) -> None:
        """根据脚本的操作, 进行触发

        :param script: 脚本对象
        """
        self.running = True
        if callable(script.action):
            script.action()
        # skip = 
        return 

    # x
    def __stop_script__(self) -> None:
        self.running = False
        return {
            'key': False,
            'dpad': False,
            'LR': False,
            'LRT': False,
        }

    # x
    def __run_script_step__(self) -> None:
        key_id: int = 0
        key_value: tuple = ()
        return {key_id: key_value}

    def __check_script__(self, key_list: list[int]) -> None:
        """检查脚本是否触发
        """
        for script in self.scripts_list_with_keys:
            if len(script.keys) <= 0:
                continue
            if script.sorted:
                if script.keys == key_list:
                    self.__run_script__(script)
                    pass
            else:
                if sorted(script.keys) == sorted(key_list):
                    self.__run_script__(script)
                    pass
        pass

    def add_script(self, script: Script) -> bool:
        try:
            if type(script.script_id) == str and type(script.desc) == str and type(script.keys) == list and type(script.sorted) == bool:
                if callable(script.action) or type(script.action) == list:
                    if script.keys == []:
                        self.scripts_list_with_no_keys.append(script)
                    else:
                        self.scripts_list_with_keys.append(script)
        except:
            return False
        return True

    def __script_menu__(self) -> None:
        if self.__recording__:
            self.__record_stop__()
        print("按键触发脚本有:")
        for script in self.scripts_list_with_keys:
            print(
                f"   {script.script_id:<10} ( {script.desc} )\n",
                f"   触发按键: {' '.join([Key.id_to_name[i] for i in script.keys])} ( {'有顺序' if script.sorted else '无顺序'} )",
            )
        i = 0
        print("可选脚本有:")
        for script in self.scripts_list_with_no_keys:
            print(
                f"{i:>3} : {script.script_id:<10} ({script.desc})\n",
            )
            i += 1
        pass

    def __record_start__(self) -> None:
        """开始录制按键
        """
        self.__recording__ = True
        self.__recording_start_time__ = self.time()
        self.__recording_cache__.append(
            f"{round(time()-self.__recording_start_time__,4):<7} : " +
            "-- Record START --" +
            "\n"
        )
        pass

    def __record_stop__(self) -> None:
        """停止录制按键并保存
        """
        self.__recording__ = False
        self.__recording_cache__.append(
            f"{round(time()-self.__recording_start_time__,4):<7} : " +
            "-- Record STOP --" +
            "\n"
        )
        with open(record_file_path, 'wt') as file:
            for line in self.__record_cache__:
                file.write(line)
        self.__record_cache__ = []
        pass

    def __record__(self, key: Key) -> None:
        """录入按键信息

        :param key_id: 按键id
        :param key_value: 按键值
        """
        self.__record_cache__.append(
            f"{round(time()-self.__recording_start_time__,4):<7} : " +
            f"{key.id:<2} {key.value:<10} [" +
            "将%s键%s" % (
                Key.id_to_name[key.id],
                f"移至{key.value}" if type(
                    key.value[0]) != bool else "按下" if key.value[0] else "松开"
            ) +
            "]\n"
        )
        pass
