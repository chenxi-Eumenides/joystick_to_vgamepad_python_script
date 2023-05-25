# **joystick_to_vgamepad_python_script**

#### English introduce
This is a python script that allows any gamepad to support macros, which can be triggered by both menus and keystrokes. Currently only windows is supported (because the vgamepad module only supports Windows).

#### 中文介绍
这是一个让任何手柄支持宏功能的python脚本，可以通过菜单和按键两种方式触发宏。目前只支持window平台（因为vgamepad模块只支持windows。）

## **not finished !!  没完成！！**

***

# How to use

## 1. install modules

```
pip install vgamepad
pip install pygame
# or
pip install -r requirements.txt
```

## 2. download scripts

```
git clone https://github.com/chenxi-Eumenides/joystick_to_vgamepad_python_script.git
```

or download all files use Web browsers. \
或者通过浏览器下载所有文件

## 3. start

Run this file directly. \
直接运行脚本

```
python path/to/vgamepad.py
# replace path/to/vgamepad.py to your file path
```

create a new python file. \
新建一个python文件

```
from .vgamepad import Virtual_Gamepad

vg = Virtual_Gamepad()
# vg.log = True # if you want
# vg.script_manager.add_script(...) # add script if you want # not finished
vg.start()
```

***
# ToDoList

#### English
- [x] Get joystick input
- [x] Virtual joystick output
- [ ] Macro support (v0.1.1 seems to work, but you have to write your own code tochange it, and I haven't written the usage, so I have to figure it out myself)
- [ ] Record macros (v0.3.0-alpha.1 now has the ability to record to a txt file, butit can't be triggered yet)
- [ ] Hover window interface
- [ ] The macro menu is fully implemented with the joystick

#### 中文
- [x] 获取手柄输入
- [x] 虚拟手柄输出
- [ ] 支持宏 (v0.1.1版本貌似是可以的，但要自己写代码改，我也没写用法，得自己琢磨)
- [ ] 录制宏 (v0.3.0-alpha.1版本有录制到txt文件的功能了，但现在还不能触发)
- [ ] 悬浮窗界面
- [ ] 完全用手柄实现宏菜单的操作

***
# Thanks

Thanks for [`vgamepad`]([http](https://github.com/yannbouteiller/vgamepad)) module. i use it to create a virtual gamepad. \
Thanks for [`pygame`](https://github.com/pygame/pygame) module. i use it to get real joystick input. \
Thanks for [`chatgpt`](https://chat.openai.com/chat). i am not a professional developer and chatgpt has helped me a lot.

