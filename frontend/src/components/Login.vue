<template>
  <div>
      <CButton @click="create()">
        Test
        </CButton>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: "Login",
  methods: {
    create() {
      let temp;
      temp = axios.get(`http://127.0.0.1:8000/user/1`)
      console.log(temp)
    }
  }
};
</script>
