<template>
  <div class="questionary">
    <div class="container-sm">
        <div v-for="set in questionary_set" class="currency">

          <!-- Кастомное сообщение об ошибке -->
          <div class="alert alert-danger" role="alert" v-if="custom_alert_msg">{{ custom_alert_msg  }}</div>

          <!-- Отображаем текст вопроса -->
          <p class="h3 mt-5">{{ set.text }}</p>

            <!-- Отображаем ответы -->
            <div class="row mt-5 mb-5">
                <div v-for="answer in set.answer" class="col-md-3">
                    <input type="radio" :id="'answer_' + answer.pk" :value=answer.pk class="form-check-input" v-model="pickedAnswer">
                    <label :for="'answer_' + answer.pk" class="form-check-label ms-3">{{ answer.text }}</label>
                </div>
            </div>

            <div v-if="next_page_url">  <!-- Если переменная next_page_url не null, тогда выполняем nextQuestion -->
                <form class="ms-3 me-3" @submit.prevent="nextQuestion">
                    <button type="submit" class="btn btn-primary">Следующий вопрос</button>
                </form>
            </div>
            <div v-else>  <!-- Если переменная next_page_url null, тогда выполняем submitForm -->
                <form class="ms-3 me-3" @submit.prevent="submitForm">
                    <button type="submit" class="btn btn-primary">Результат</button>
                </form>
            </div>

        </div>  <!-- div.currency -->
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
      pickedAnswer: null,
      custom_alert_msg: null
    }
  },
  mounted() {
    axios
        .get('/api/v1/questionary/' + this.$route.params.id + '/')
        .then(response => {
          this.next_page_url = response.data.next,
          this.questionary_set = response.data.results
        })
        .catch(error => { console.log(error) })
  },
  methods: {
    async send_data_to_back() {
        const formData = {
            questionary: this.$route.params.id,
            answer: this.pickedAnswer
        }  // Формируем необходимые данные для сервера

        // Посылаем данные на сервер
        await axios
            .post('/api/v1/questionary/user-answer/', formData)
            .then(response => { console.log(response) })
            .catch(error => { console.log(error) })
    },

    nextQuestion(e) {
        if( this.pickedAnswer != null ) {
            this.send_data_to_back();  // Посылаем ответ на сервер

            this.custom_alert_msg = null;  // Обнуляем сообщение об ошибке
            this.pickedAnswer = null;  // Обнуляем выбранный ответ. Переносится на следующий вопрос.

            // Переходим на следующую страницу
            axios
                .get( this.next_page_url )
                .then(response => {
                  this.next_page_url = response.data.next,
                  this.questionary_set = response.data.results
                })
                .catch(error => { console.log(error) })
        } else { this.custom_alert_msg = 'Чтобы приступить к следующему вопросу, нужно ответить на текущий' }
    },

    submitForm(e) {
        this.send_data_to_back();  // Посылаем последний ответ на сервер
        this.$router.push('/questionary/' + this.$route.params.id + '/results/')  // Делаем редирект на View с результатом
    }
  }
}
</script>