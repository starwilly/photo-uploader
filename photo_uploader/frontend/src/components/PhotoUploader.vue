<template>
<div class="center">
  <vue-core-image-upload
    class="btn btn-primary"
    :crop="false"
    @imageuploaded="imageuploaded"
    :max-file-size="5242880"
    input-of-file='file'
    :url="uploadUrl" >
  </vue-core-image-upload>
</div>
</template>

<script>
import VueCoreImageUpload from 'vue-core-image-upload'

export default {
  name: 'PhotoUploader',
  components: {
    'vue-core-image-upload': VueCoreImageUpload
  },
  data () {
    return {
      uploadUrl: 'http://localhost:8000/api/upload'
    }
  },
  methods: {
    imageuploaded (res) {
      if (res.success) {
        alert(res.success)
      }
    }
  }
}
</script>
