from typing import Union, Callable, Iterator
from .Setting import record_file_path, translation
from .Keys import Key
from time import time
from datetime import datetime


class Script():
    """脚本类

    script_id: 脚本的id\n
    desc: 脚本的描述\n
    keys: 脚本的触发按键, 为空列表则需要通过菜单脚本触发\n
    sorted: 脚本按键是否有顺序要求, True 为有按键顺序要求\n
    action: 脚本执行的动作, 如果为函数对象, 则为执行函数, 若为列表, 则按列表内容执行按键
    skip_key_type: 脚本执行时要屏蔽的按键类型
    """

    def __init__(
        self,
        script_id: str,
        desc: str = '',
        keys: list[int] = [],
        sorted: bool = False,
        action: Union[Callable, list] = None,
        skip_key_type: dict[str, bool] = {
            'key': True,
            'dpad': True,
            'L': True,
            'R': True,
            'LRT': True,
        }
    ) -> None:
        """脚本类

        :param script_id: 脚本的id
        :param desc: 脚本的描述
        :param keys: 脚本的触发按键, 为空列表则需要通过菜单脚本触发
        :param sorted: 脚本按键是否有顺序要求, True 为有按键顺序要求
        :param action: 脚本执行的动作, 如果为函数对象, 则为执行函数, 若为列表, 则按列表内容执行按键
        :param skip_key_type: 脚本执行时要屏蔽的按键类型
        """
        self.script_id: str = script_id
        self.desc: str = desc
        self.keys: list[int] = keys
        self.sorted: bool = sorted
        self.action: Union[Callable, list] = action
        self.skip_key_type: dict[str, bool] = skip_key_type
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
        if type(self.skip_key_type) == dict:
            for name, value in self.skip_key_type.items():
                if name not in ['key', 'dpad', 'L', 'R', 'LRT'] or type(value) != bool:
                    raise ValueError(
                        "skip_key_type 的键需要是'key','dpad','L','R','LRT'中的一个, 且值为bool类型")
        else:
            raise ValueError("skip_key_type 需要是 dict 类型")
        pass


class Script_Manager():
    """脚本管理器, 负责脚本的激活检查, 运行/停止脚本, 添加脚本, 脚本状态管理
    """

    def __init__(self) -> None:
        # 是否在运行脚本
        self.running: bool = False
        # 不可按键触发的脚本列表
        self.scripts_list_with_no_keys: list[Script] = []
        # 可按键触发的脚本列表
        self.scripts_list_with_keys: list[Script] = []
        # 正在运行的脚本
        self.running_script: Union[Script, None] = None
        # 下一个运行的脚本
        self.next_script: Union[Script, None] = None
        # 脚本冷却时间
        self.script_cooldown_time: float = 0.5
        # 脚本是否需要按键更新
        self.need_keys_update: bool = False
        # 待运行的脚本动作
        self.script_steps_iter: Iterator = None
        # 脚本上次运行的时间
        self.last_time: float = time()
        # 脚本需要等待的时间
        self.wait_time: float = 0.0
        # 是否在录制脚本
        self.__recording__: bool = False
        # 录制内容缓存
        self.__recording_cache__: list[str] = []
        # 录制脚本运行开始时间
        self.__recording_start_time__: float = time()
        # 添加默认脚本
        self.__init_scripts__()
        pass

    def __run_script__(self, script: Script) -> None:
        """根据脚本的操作, 进行触发

        :param script: 脚本对象
        """
        self.running_script = script
        self.next_script = None
        self.last_time = time()
        self.wait_time = 0.0
        print(translation.get_from_key('script_start') + ' - ' + script.script_id)
        if callable(script.action):
            self.need_keys_update = False
            script.action()
            self.__stop_script__()
        elif type(script.action) == list:
            self.need_keys_update = True
            self.script_steps_iter = iter(script.action)
        pass

    def __stop_script__(self) -> None:
        """停止当前运行的脚本
        """
        print(translation.get_from_key('script_end') + ' - ' +
              self.running_script.script_id)
        self.running = False
        self.running_script = None
        self.need_keys_update = False
        self.script_steps_iter: Iterator = None
        self.last_time = time()
        pass

    def __check_script__(self, need_checked_list: list[int]) -> None:
        """检查脚本是否触发, 触发就设置为下一个运行的脚本
        """
        for script in self.scripts_list_with_keys:
            if len(script.keys) <= 0:
                continue
            if script.sorted:
                if script.keys == need_checked_list:
                    self.running = True
                    self.next_script: Script = script
                    return True
            else:
                if sorted(script.keys) == sorted(need_checked_list):
                    self.running = True
                    self.next_script: Script = script
                    return True
        return False

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

    def __init_scripts__(self) -> None:
        # 添加菜单脚本
        self.scripts_list_with_keys.append(Script(
            script_id=translation.get_from_key('menu_script_name'),
            desc=translation.get_from_key('menu_script_desc'),
            keys=[Key.name_to_id['up'], Key.name_to_id['A'], Key.name_to_id['X']],
            sorted=True,
            action=self.__script_menu__,
        ))
        # 添加录制脚本
        self.scripts_list_with_keys.append(Script(
            script_id=translation.get_from_key('record_script_name'),
            desc=translation.get_from_key('record_script_desc'),
            keys=[Key.name_to_id['left'],
                  Key.name_to_id['A'], Key.name_to_id['X']],
            sorted=True,
            action=self.__record_start__,
        ))
        # 添加帮助脚本
        self.scripts_list_with_no_keys.append(Script(
            script_id=translation.get_from_key('help_script_name'),
            desc=translation.get_from_key('help_script_desc'),
            keys=[],
            sorted=False,
            action=self.__script_help__,
        ))
        pass

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
        self.__recording_start_time__ = time()
        self.__recording_cache__.append(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.__recording_cache__.append(
            f"{round(time()-self.__recording_start_time__,4):<7} : " +
            "\n-- Record START --" +
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
        with open(record_file_path, 'wt', encoding="utf-8") as file:
            for line in self.__recording_cache__:
                file.write(line)
        self.__recording_cache__ = []
        pass

    def __record__(self, keys: dict[int, Key]) -> None:
        """录入按键信息

        :param key_id: 按键id
        :param key_value: 按键值
        """
        cache = ''
        for key in keys.values():
            if key.__status__ == 1:
                if key.type in ['L', 'R']:
                    if key.value[0] < 0.01 and key.value[1] < 0.01:
                        continue
                elif key.type in ['LRT']:
                    if key.value[0] < 0.01:
                        continue
                temp1 = f"{key.id:<2}" + " {}".format(key.value)
                temp2 = f" [将{Key.id_to_name[key.id]}键" + (f"移至{key.value}" if type(
                    key.value[0]) != bool else "按下" if key.value[0] else "松开") + "]"
                cache += f"{temp1:<20} {temp2:<30}"

        if cache != '':
            self.__recording_cache__.append(
                f"{round(time()-self.__recording_start_time__,4):<7} : " +
                cache + "\n"
            )
        pass

    def __script_help__(scripts_with_keys: list[Script]) -> None:
        print(translation.get_from_key('help_script_content'))
        for script in scripts_with_keys:
            print(
                f"{script['name']}  :  {script['keys']} {translation.get_from_key('help_script_sorted' if script['sorted'] else 'help_script_not_sorted')}")
        print("")
        pass
