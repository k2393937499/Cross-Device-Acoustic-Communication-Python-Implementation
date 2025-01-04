import axios from 'axios';

const option = "24bit";

axios.post('http://127.0.0.1:5000/modulation_option', {option: option})
  .then(response => {
    const bit = option;
    console.log('Success:', response.data);
  })
  .catch(error => {
    console.error('Error:', error);
  });

axios.post('http://127.0.0.1:5000/output')
.then(response => {
    console.log('Success:', response.data);
  })
  .catch(error => {
    console.error('Error:', error);
  });