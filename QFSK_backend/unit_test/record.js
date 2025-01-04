import axios from 'axios';

const time = 5;

axios.post('http://127.0.0.1:5000/record', { time: time })
  .then(response => {
    console.log('Success:', response.data);
  })
  .catch(error => {
    console.error('Error:', error);
  });
