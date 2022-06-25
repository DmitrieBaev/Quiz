<template>
  <nav class="py-2 bg-light border-bottom">
    <div class="container d-flex flex-wrap">
      <ul class="nav me-auto">
        <li class="nav-item"><router-link to="/" class="nav-link link-dark px-2 active" aria-current="page">Главная</router-link></li>
        <!-- <li class="nav-item"><a href="#" class="nav-link link-dark px-2">Pricing</a></li> -->
        <!-- <li class="nav-item"><a href="#" class="nav-link link-dark px-2">FAQs</a></li> -->
        <!-- <li class="nav-item"><a href="#" class="nav-link link-dark px-2">About</a></li> -->
      </ul>
      <ul class="nav" v-if="this.$store.state.token === ''">
        <li class="nav-item"><router-link to="/sign-in" class="nav-link link-dark px-2">Авторизация</router-link></li>
        <li class="nav-item"><router-link to="/sign-up" class="nav-link link-dark px-2">Регистрация</router-link></li>
      </ul>
      <ul class="nav" v-else>
        <li class="nav-item"><button @click=signout() class="btn nav-link link-dark px-2">Выход</button></li>
      </ul>
    </div>
  </nav>
  <router-view/>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  beforeCreate() {
    this.$store.commit('initializeStore')

    const token = this.$store.state.token
    if ( token ) {
      axios.defaults.headers.common['Authorization'] = 'Token ' + token
    } else {
      axios.defaults.headers.common['Authorization'] = ''
    }
  },

  methods: {
    async signout() {
      await axios
            .post('/api/v1/auth/token/logout/')
            .then(response => {
              console.log('Signed out')
            })
            .catch(error => {
              console.log(error)
            })
      axios.defaults.headers.common['Authorization'] = ''
      localStorage.removeItem('token')
      this.$store.commit('removeToken')

      this.$router.push('/')
    }
  }
}
</script>

<style lang="scss">
#app {
  /* font-family: Avenir, Helvetica, Arial, sans-serif; */
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  a {
    text-decoration: none;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
