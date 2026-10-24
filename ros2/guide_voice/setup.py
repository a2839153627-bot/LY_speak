import os
from glob import glob
from setuptools import find_packages, setup
# 包名 guide_voice：两个工作区原来都有 voice 包，终端 source 过巡检工作区时
# ros2 launch voice 会起错包。改名后命令唯一指向讲解语音。inner 模块仍叫 voice
# （entry_points 里的 voice.nodes.* 不动，import 全不变）。
package_name="guide_voice"
setup(name=package_name,version="0.1.0",packages=find_packages(exclude=["test"]),data_files=[("share/ament_index/resource_index/packages",["resource/"+package_name]),("share/"+package_name,["package.xml"]),(os.path.join("share",package_name,"launch"),glob("launch/*.launch.py")),(os.path.join("share",package_name,"config"),glob("config/*.yaml"))],install_requires=["setuptools"],zip_safe=True,entry_points={"console_scripts":["tts_sherpa_node = voice.nodes.tts_sherpa_node:main","tts_python_node = voice.nodes.tts_python_node:main"]})
