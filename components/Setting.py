import toml
from pathlib import Path


class TranslationConfig:
    def __init__(self, file_name: str = 'zh_CN'):
        self.translations = {}
        1 if self.load_config(file_name) else self.load_config(file_name)

    def load_config(self, file_name: str = 'zh_CN'):
        self.config_file = 'localization/'+file_name+'.toml'
        try:
            with open(self.config_file, 'r', encoding='utf-8') as file:
                self.translations = toml.load(file)
            return True
        except:
            Path('localization').mkdir(parents=True, exist_ok=True)
            Path(self.config_file).touch()
            with open(self.config_file, 'wt', encoding='utf-8') as file:
                file.write("language = \"zh_CN\"\n\
\n\
# 脚本部分\n\
script_start = \"脚本启动\"\n\
script_end = \"脚本结束\"\n\
# 菜单脚本\n\
menu_script_name = \"菜单脚本\"\n\
menu_script_desc = \"启动无按键触发的脚本\"\n\
# 录制脚本\
record_script_name = \"录制脚本\"\n\
record_script_desc = \"录制手柄操作, 并保存到文件\"\n\
# 帮助脚本\n\
help_script_name = \"帮助\"\n\
help_script_desc = \"打印帮助信息\"\n\
help_script_content = \"同时按住脚本设定的按键即可启用脚本。注意，有些脚本有按键顺序的要求。\\n无按键触发的可通过‘手动激活脚本’触发\\n脚本触发期间，无法操控\\n觉得不满意的可以自行修改代码。\\n以下脚本可直接通过按键触发。\\n\"\n\
help_script_sorted = \"有顺序\"\n\
help_script_not_sorted = \"无顺序\"\n\
# 荒野之息飞弹\n\
botw_fly_script_name= \"荒野之息-飞弹\"\n\
botw_fly_script_desc= \"荒野之息飞弹, 需要有高低差\"")
            return False

    def get_from_key(self, key: str = ''):
        if key in self.translations:
            return self.translations[key]
        else:
            return f"ERROR : didn`t find key: {key}."


# 摇杆设置
rocker: dict[str, float] = {
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

# 录制文件保存路径
record_file_path: str = './record.txt'

# 浮点数精度误差
float_delta: float = 0.000001

# 是否开启log
is_log: bool = False

# 使用到的按键数量(不包括摇杆等)
used_key_count: int = 14

# 语言配置
language: str = 'zh_CN'
translation = TranslationConfig(language)
