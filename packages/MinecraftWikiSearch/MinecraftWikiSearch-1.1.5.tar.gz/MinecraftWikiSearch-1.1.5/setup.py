# coding:utf-8
from setuptools import setup, find_packages

setup(
    name='MinecraftWikiSearch',
    version='1.1.5',
    description='供机器人或者其他程序使用Minecraft Wiki查询的接口',
    author='MingxuanGame',
    author_email='mingxuangame@outlook.com',
    license='Apache-2.0',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'MinecraftWikiSearch=MinecraftWikiSearch.MinecraftWikiSearch:main'
        ]
    },
    packages=find_packages(),
)
