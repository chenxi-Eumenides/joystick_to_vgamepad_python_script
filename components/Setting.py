import toml


class TranslationConfig:
    def __init__(self, file_name: str = 'zh_CN'):
        self.translations = {}
        self.load_config(file_name)

    def load_config(self, file_name: str = 'zh_CN'):
        self.config_file = 'localization/'+file_name+'.toml'
        with open(self.config_file, 'r', encoding='utf-8') as file:
            self.translations = toml.load(file)

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
