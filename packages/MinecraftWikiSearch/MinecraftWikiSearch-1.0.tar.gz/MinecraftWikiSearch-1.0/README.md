MinecraftWikiSearch
===============

供机器人或其他程序使用的Minecraft Wiki查询接口

请调用main函数（如果你没有开启*EasyInput*并且没有以命令形式调用或以命令形式调用未填写参数，请一定填写参数，否则或报错）

```python
main(arg=<参数>)
```

设置
-------

这是配置文件（config.json）的内容
```json
{
  "FasterLoad": true,
  "EasyInput": false,
  "EasyReturn": false
}
```

FasterLoad：如果启用它，程序将使用[BWiki的镜像站](https://wiki.biligame.com/mc) 以加快访问速度，否则将访问[原站](https://minecraft-zh.gamepedia.com)

EasyInput：将使用简单传入的方法（通过读取wiki.txt传入）

EasyReturn：将使用简单传承的方法（通过写入return.txt传出）