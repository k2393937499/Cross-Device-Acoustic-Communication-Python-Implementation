# 前后端逻辑
## 概览
实现数字通信，能对声波原始数据进行调制，或对文字的utf-8编码进行调制
- 设备1：录音模块、选择调制方式模块、发送模块
- 设备2：录音模块、选择调制方式模块、输出模块

## 模块和接口
### 录音模块
功能：
- 设置录音时长，进行录音，将wav保存到本地

接口：
<details>
<summary>/record</summary>
类型：POST

描述：实现录音功能，由于`sounddevice`库的限制，必须提前设置录音时长

参数：
```
{
    "time": 5
}
```

返回：
```
{
    "status": "success",
    "status_code": xxx,
    "data": {
        "record_status": "done"
    }
}
```
</details>

### 调制方式选择模块
功能：
- 选择调制原始声波或调制utf-8编码

接口：
<details>
<summary>/modulation_option</summary>
类型：POST

描述：选择直接对原始声波进行调制，或者对汉字utf-8编码进行调制

参数：
```
{
    "option": Literal["8bit", "16bit", "utf-8"]
}
```

返回：
```
{
    "status": "success",
    "status_code": xxx,
    "data": option
}
```
</details>

## 发送模块
功能：
调制信号并发送

接口：
<details>
<summary>/send</summary>
类型：POST

描述：调制信号并发送

参数：
```
record["data"]["record_status"]
```

返回：
```
{
    "status": "success",
    "status_code": xxx,
    "data": "finished to send wave"
}
```
</details>

## 输出模块
功能：
根据调制方式的不同，选择解调出声波或汉字，并进行播放

接口：
<details>
<summary>/output</summary>
类型：POST

描述：解调并输出

参数：
```
modulation_option["data"]
```

返回：
```
{
    "status": "success",
    "status_code": xxx,
    "data": "strating to output sound"
}
```
</details>