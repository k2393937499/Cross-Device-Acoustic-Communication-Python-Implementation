<div align="center">

# 跨设备声学通信Ptyhon实现

使用QFSK和卷积编码实现声学数字通信. 

[English](../README.md) | 中文

</div>

## 介绍
[示例视频（待办）](/#)

这个项目通过传播比特流，实现了跨设备的声学数字通信。项目有以下特点：
1. **数字通信** ：信号被转化为比特流，调制后通过正弦波进行传输。
2. **AI支持** ：由于扬声器支持的符号率较低，为了提高传输效率，添加了基于AI的语音文字相互转换模块。
3. **误码率优化** ：为了减小误码率（BER），使用了QFSK调制和卷积编码。
4. **网页支持** ：为了使项目易于体验，添加了基于`VUE.js`的前端交互。

## 项目结构
![项目结构图（待办）](/#)

项目可以传输原始的声波或汉字的二进制UTF-16编码。

跨设备通信时，信号的发射和接收通过电脑的扬声器与麦克风实现，硬件的特性限制了符号率，导致传输效率很低。例如，发送一个1秒的原始声波（16比特，5000采样率，200符号率）的耗时为

$$0.05 \times (5000 / 2) * 16 = 2000s$$

这就是为什么我们添加了AI支持，通过直接传递字符的UTF-16编码，大大提高传输效率。

以下为项目使用的模块以及他们的功能：
1. **录音模块** ：以5000采样频率录音（主要受限于原始声波传输）。
2. **QFSK模块** ：为不同符号对设置不同的频率，不使用QPSK的原因是当信号相位发生变化时，扬声器播放的声音会失真。
3. **语音文字转换模块** ：为了实现UTF-16编码，首先识别出文字，在将其进行调制和播放。
4. **卷积编码** ：当传输UTF-16编码时，误码率必须为0\%，所以我们添加了卷积编码来尽可能防止误码的发生。

## 环境配置
1. 克隆仓库
2. 安装前后端依赖，需要确保您的设备有`Python`和`node.js`，然后运行：

```cd QFSK_communication```

```cd QFSK_backend```

```pip install -r requirements.txt```

```npm install```

```cd ../QFSK_frontend```

```npm install```

> 注意
> 安装最新版`torchaudio`时，会自动将环境中的`torch`更新为最新版，所以您可能需要一个新的虚拟环境来进行安装

## 快速开始
1. 在 `QFSK_communication/QFSK_backend/` 路径下, 运行 `python app.py` 以启动后端。
2. 在 `QFSK_communication/QFSK_frontend/` 路径下, 运行 `npm run dev` 以启动前端。
3. 访问本地端口 `http://localhost:5123` 来尝试网页交互。

关于单元测试：
1. 您可以单独为每个模块运行单元测试，所有单元测试都保存在 `QFSK_backend/unit_test` 中。
2. 运行 `*.py` 测试，在 `QFSK_communication/QFSK_backend/` 路径下, 运行 `python -m unit_test.modulation_utf`。
3. 运行 `*.js` 测试，在 `QFSK_communication/QFSK_backend/` 路径下, 运行 `python app.py` ，接着运行 `node unit_test/record.js` 以查看结果。

## 待办
- [x] 上传代码.
- [x] 添加中文README.
- [ ] Desigin the webpage.
- [ ] Add quantitative experiment.
- [ ] Upload demo video.
