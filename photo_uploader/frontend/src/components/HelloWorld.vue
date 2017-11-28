<template>
  <div class="hello">
    <photo-uploader :height="300" />
  </div>
</template>

<script>
import PhotoUploader from '@/components/PhotoUploader'

export default {
  name: 'HelloWorld',
  components: {PhotoUploader},
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.hello {
  width: 50%;
  margin: 0 auto;
}
</style>
