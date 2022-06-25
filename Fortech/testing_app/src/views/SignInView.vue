<template>
  <div class="sign-in">
    <h1>Авторизация</h1>

    <form class="ms-3 me-3" @submit.prevent="submitForm">
      <div class="mb-3 row">
        <label for="RegUName" class="col-sm-2 col-form-label">Логин: </label>
        <div class="col-md-10">
          <input id="RegUName" name="username" v-model="username" class="form-control">
        </div>
      </div>

      <div class="mb-3 row">
        <label for="RegUPWD" class="col-sm-2 col-form-label">Пароль: </label>
        <div class="col-md-10">
          <input id="RegUPWD" type="password" name="password" v-model="password" class="form-control">
        </div>
      </div>

      <button type="submit" class="btn btn-primary">Войти</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'SignInView',
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    submitForm(e) {
      const formData = {
        username: this.username,
        password: this.password
      }

      axios
          .post('/api/v1/auth/token/login/', formData)
          .then(response => {
            const token = response.data.auth_token
            this.$store.commit('setToken', token)
            localStorage.setItem('token', token)

            axios.defaults.headers.common['Authorization'] = "Token " + token

            this.$router.push('/')
            console.log(response)
          })
          .catch(error => {
            console.log(error)
          })
    }
  }
}
</script>