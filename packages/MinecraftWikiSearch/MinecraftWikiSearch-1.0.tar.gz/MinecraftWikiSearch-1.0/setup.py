# coding:utf-8
from setuptools import setup
setup(
    name='MinecraftWikiSearch',
    version='1.0',
    description='供机器人或者其他程序使用Minecraft Wiki查询的接口',
    author='MingxuanGame',
    author_email='mingxuangame@outlook.com',
    license='Apache-2.0',
    include_package_data=True,
    install_requires=[
        'beautifulsoup4>=4.9.3'
    ],
    py_modules=[
        'MinecraftWikiSearch',
    ],
    entry_points={
        'console_scripts': [
            'MinecraftWikiSearch=MinecraftWikiSearch:main'
        ]
    }
)
