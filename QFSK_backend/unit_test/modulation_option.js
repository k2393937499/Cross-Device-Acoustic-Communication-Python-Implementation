import axios from 'axios';

const option = "8bit";

axios.post('http://127.0.0.1:5000/modulation_option', {option: option})
  .then(response => {
    console.log('Success:', response.data);
  })
  .catch(error => {
    console.error('Error:', error);
  });
