<template>
    <div class="results">
        <p class="h1 mb-3">Результат прохождения теста</p>
        <div class="alert alert-info display-6" role="alert">
            {{ calculate_results()  }}
        </div>
    </div>
</template>



<script>
import axios from 'axios'

export default {
  name: 'QuestionaryView',
  props: { id: { type: String, default: null } },
  data() { return { result_set: null } },
  mounted() {
    axios
        .get('/api/v1/questionary/' + this.$route.params.id + '/result')
        .then(response => { this.result_set = response.data })
        .catch(error => { console.log(error) })
  },
  methods: {
    calculate_results() {
      var total_count = 0;  // Количество вопросов
      var total_correct = 0;  // Количество правильных ответов
      var percentage = 0;  // Процент правильных ответов

      for ( var set in this.result_set ) {
        total_count++;
        if( this.result_set[set].answer['is_valid'] != false ) { total_correct++; }
      }
      percentage = total_correct * 100 / total_count
      if ( percentage ) { return `${ total_correct }/${ total_count } - ${ percentage.toFixed(2) }% правильных ответов` }
    }
  }
}
</script>