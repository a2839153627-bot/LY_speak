from setuptools import setup

package_name = 'ly_speak_mission'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='smart',
    maintainer_email='smart@localhost',
    description='LY_Guide 讲解任务执行节点',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'guide_mission_node = ly_speak_mission.guide_mission_node:main',
        ],
    },
)
