<template>
  <div class="sign-up">
    <h1>Регистрация</h1>
    <form class="ms-3 me-3" @submit.prevent="submitForm">
      <div class="mb-3 row">
        <label for="RegUName" class="col-sm-2 col-form-label">Логин: </label>
        <div class="col-md-10">
          <input id="RegUName" name="username" v-model="username" class="form-control">
        </div>
      </div>

      <div class="mb-3 row">
        <label for="RegUEmail" class="col-sm-2 col-form-label">E-mail: </label>
        <div class="col-md-10">
          <input id="RegUEmail" type="email" name="email" v-model="email" class="form-control">
        </div>
      </div>

      <div class="mb-3 row">
        <label for="RegUPWD" class="col-sm-2 col-form-label">Пароль: </label>
        <div class="col-md-10">
          <input id="RegUPWD" type="password" name="password" v-model="password" class="form-control">
        </div>
      </div>
      
      <button type="submit" class="btn btn-primary">Зарегистрироваться</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'SignUpView',
  data() {
    return {
      username: '',
      password: '',
      email: ''
    }
  },
  methods: {
    submitForm(e) {
      const formData = {
        username: this.username,
        password: this.password,
        email: this.email
      }

      axios
          .post('/api/v1/auth/users/', formData)
          .then(response => {
            this.$router.push('/log-in')
            console.log(response)
          })
          .catch(error => {
            console.log(error)
          })
    }
  }
}
</script>