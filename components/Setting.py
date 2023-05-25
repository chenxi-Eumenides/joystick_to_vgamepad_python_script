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
float_delta: float = 0.01

# 是否开启log
is_log: bool = True

# 使用到的按键数量(不包括摇杆等)
used_key_count: int = 14
