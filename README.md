<div align="center">

# Cross-Device Acoustic Communication Python Implementation

Digital acoustic communication tools using QFSK and Convolutional Encode. 跨设备声学通信。

English | [中文](docs/README-zh.md)

</div>

## Introduction
[Demo_video (to be add)](/#)

This project enables cross-device acoustic communication by transmitting bitstreams through the air. The highlight are as follows:
1. **Digital Transmit** : Information is converted into a bitstream and transmitted via a sine wave.
2. **AI Support** : To transmit bitstream at low symbol rate, seppch2text and text2speech module are included.
3. **BER Optimization** : To minize the bit error rate (BER). QFSK modulation and Convolutional Encode are used before transmit.
4. **Web Supported** : To make it easier to get started, a web UI based `VUE.js` is added.

## Project Structure
![Project Structure (to be add)](/#)

This project can transmit the origin acoustic wave or transmit the UTF-16 encoding of each character.

Transmission and reception are achieved through the speaker and microphone, these devices limit the symbol rate, for example, the time cost of transmiting a 1s original acoustic wave (16bit, 5000 sample rate and 200 symbol rate) is:

$$0.05 \times (5000 / 2) * 16 = 2000s$$

This is why we add AI Support, so that we can transmit the UTF-16 encoding at much lower time cost.

The modules of this project and their usage are:
1. **Record Module** : record the sound at 5000 sample rate.
2. **QFSK Module** : set different frequence for different bit pair as the table. The reason for not using QPSK is that the phase differences of the sine wave can cause speaker distortion.

| bit pair | freq |
| :--: | :--: |
| ‘00’ | 2000 |
| ‘01’ | 1500 |
| ‘10’ | 1000 |
| ‘11’ | 500 |

3. **Speech2Text and Text2Speech** : To decode the character speaker said using UTF-16, we need recognize the speech first. Then encode the bitstream and play it. Whisper and ChatTTS is used in this module.

4. **Convlutional Encode** : When encode the UTF-16 bitstream, BER must be 0\%, so we add convlutional encode to correc error bits.

## Installation
1. Clone this repo
2. Install the backend and frontend dependence. You need to have `Python` and `node.js` reday, then run:

```cd QFSK_communication```

```cd QFSK_backend```

```pip install -r requirements.txt```

```npm install```

```cd ../QFSK_frontend```

```npm install```

> Note
> When install the latest `torchaudio`, it will update the torch into latest version, so you may need a new virtual environment.

## Quick Start
1. In `QFSK_communication/QFSK_backend/`, run `python app.py`.
2. In `QFSK_communication/QFSK_frontend/`, run `npm run dev`.
3. Try the web UI in `http://localhost:5173`.

About unit test:
1. You can run the unit test to test each module. All the unit test are storage in `QFSK_backend/unit_test`.
2. To run the `*.py` test, in `QFSK_communication/QFSK_backend/`, run `python -m unit_test.modulation_utf`
3. To run the `*.js` test, in `QFSK_communication/QFSK_backend/`, run `python app.py`, then run `node unit_test/record.js` et al.

## TODO
- [x] Release code.
- [x] Add Chinese README.
- [ ] Desigin the webpage.
- [ ] Add quantitative experiment.
- [ ] Upload demo video.

## Acknowledgements
to be done.

## Thanks to all the contributors
[![contributors](https://contrib.rocks/image?repo=k2393937499/Cross-Device-Acoustic-Communication-Python-Implementation)](https://github.com/k2393937499/Cross-Device-Acoustic-Communication-Python-Implementation/graphs/contributors)
