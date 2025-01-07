<template>
  <div class="m-3">
    <p class="fs-3 fw-semibold">录音</p>
    <BFormSelect
        id="time"
        v-model="time_select"
        :options="[{text: 'Choose...', value: null}, 0.5, 1, 2, 3, 4, 5]"
      />
    <p>选择录音时长以开始录制：{{ time_select }}</p>
    <div class="d-grid gap-2">
      <BButton id="time_btn" variant="primary"
        @click="record" :disabled="time_btn_disable">
          {{ time_btn_text }}
      </BButton>
    </div>
  </div>

  <div class="m-3">
    <p class="fs-3 fw-semibold">选择压缩方式</p>
    <BFormSelect
        id="modulation_option"
        v-model="modulation_select"
        :options="[{text: 'Choose...', value: null}, '8bit', '16bit', 'utf-8']"
      />
    <p>当前压缩方式为：{{ modulation_text }}</p>
    <div class="d-grid gap-2">
      <BButton id="modulation_btn" variant="primary" @click="modulation">
          设置
      </BButton>
    </div>
  </div>

  <div class="m-3">
    <p class="fs-3 fw-semibold">发送调制信号</p>
    <p>utf-8模式识别到的文字为：{{ text }}</p>
    <div class="d-grid gap-2">
      <BButton id="send_btn" variant="primary" @click="send">
          发送
      </BButton>
    </div>
  </div>
</template>

<script setup>
import {ref} from 'vue';
import axios from 'axios';

const time_select = ref(null);
const time_btn_disable = ref(false);
const time_btn_text = ref("开始录音")
var record_status = null;
const modulation_select = ref(null);
const modulation_text = ref(null);
const text = ref(null);

const record = () => {
  if(time_select.value === null){
    alert("请选择时间");
    return;
  }

  time_btn_disable.value = true;
  time_btn_text.value = "录音中...";

  axios.post('http://127.0.0.1:5000/record', { time: time_select.value })
    .then(response => {
      time_btn_disable.value = false;
      time_btn_text.value = "开始录音";
      record_status = response.data['data']['record_status'];
      console.log(response.data);  // 请求成功时输出响应数据
    })
    .catch(error => {
      console.error(error);  // 请求失败时输出错误
    });
}

const modulation = () =>{
  if(modulation_select.value === null){
    alert("请选择调制比特数");
    return;
  }
  axios.post('http://127.0.0.1:5000/modulation_option', {option: modulation_select.value})
    .then(response => {
      modulation_text.value = modulation_select.value;
      console.log(response.data);
    })
    .catch(error => {
      console.error(error);
    })
}

const send = () => {
  if(record_status === null){
    alert("请先录制语音");
    return;
  }
  if(modulation_text === null){
    alert("请选择调制比特数")
    return;
  }
  axios.post('http://127.0.0.1:5000/send')
    .then(response => {
      if(modulation_select.value === 'utf-8'){
        text.value = response.data['data']
      }
        console.log(response.data);
      }
    )
    .catch(error => {
      console.error(error);
    })
}

</script>