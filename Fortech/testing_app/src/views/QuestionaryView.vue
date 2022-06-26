<template>
  <div class="questionary">
    <div class="container-sm">
        <div v-for="set in questionary_set" class="currency">
          <p class="h1">{{ set.questionary.caption }}</p>

          <div class="alert alert-danger" role="alert" v-if="custom_alert_msg">{{ custom_alert_msg  }}</div>

          <p class="h3 mt-5">{{ set.text }}</p>

            <div class="row mt-5 mb-5">
                <div v-for="answer in set.answer" class="col-md-3">
                    <input type="checkbox" :id="'answer_' + answer.pk" :value=answer.pk class="form-check-input" v-model="checkedAnswers">
                    <label :for="'answer_' + answer.pk" class="form-check-label ms-3">{{ answer.text }}</label>
                </div>
            </div>

        <div v-if="next_page_url">
            <form class="ms-3 me-3" @submit.prevent="nextQuestion">
                <button type="submit" class="btn btn-primary">Следующий вопрос</button>
            </form>
        </div>
        <div v-else>
            <form class="ms-3 me-3" @submit.prevent="submitForm">
                <button type="submit" class="btn btn-primary">Результат</button>
            </form>
        </div>

        </div>
        <hr>
        <span>Выбрано: {{ checkedAnswers }} => {{ checkedAnswers.length }}</span>
        <hr>
        <p>{{ id }}</p>
        <p>{{ this.$route.params }}</p>
        <hr>
        <p>TEST</p>
        <p>{{ next_page_url }}</p>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'QuestionaryView',
  props: {
    id: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      questionary_set: null,
      next_page_url: null,
      checkedAnswers: [],
      checked_answers_current: 0,
      custom_alert_msg: null
    }
  },
  mounted() {
    // const url = ( this.next_page_url ) ? this.next_page_url : ('/api/v1/questionary/' + this.$route.params.id + '/');
    axios
        .get('/api/v1/questionary/' + this.$route.params.id + '/')
        .then(response => {
          this.next_page_url = response.data.next,
          this.questionary_set = response.data.results
        })
        .catch(error => { console.log(error) })
  },
  methods: {
    nextQuestion(e) {
      if(this.checkedAnswers.length != this.checked_answers_current) {
      this.custom_alert_msg = null;
      this.checked_answers_current = this.checkedAnswers.length;

      axios
          .get(this.next_page_url)
          .then(response => {
            this.next_page_url = response.data.next,
            this.questionary_set = response.data.results
          })
          .catch(error => { console.log(error) })
      } else { this.custom_alert_msg = 'Чтобы приступить к следующему вопросу, нужно ответить на текущий' }
    },

    submitForm(e) {
      const formData = { answers: this.checkedAnswers }
      // this.custom_alert_msg = this.checkedAnswers

    axios
          .post('/api/v1/questionary/user-answer/', formData)
          .then(response => {
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