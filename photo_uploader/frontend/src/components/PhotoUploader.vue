<template>
<div class="center">
  <input type="file" name="image" accept="image/*" @change="setImage"/>
  <br />
  <div style="max-width: 900px; display: inline-block;">
      <vue-cropper
          ref="cropper"
          :guides="true"
          :view-mode="2"
          drag-mode="crop"
          :auto-crop="false"
          :auto-crop-area="0.5"
          :min-container-width="250"
          :min-container-height="180"
          :background="true"
          :rotatable="true"
          :src="imgSrc"
          alt="Source Image"
          :img-style="{ width: '400px', height: '300px' }"
          >
      </vue-cropper>
  </div>
  <br>
  <button @click="startCrop">Select</button>
  <button @click="cropImage">Crop</button>
  <button @click="upload">Upload</button>

</div>
</template>

<script>
import VueCropper from 'vue-cropperjs'
import * as axios from 'axios'

export default {
  name: 'PhotoUploader',
  components: {
    'vue-cropper': VueCropper
  },
  data () {
    return {
      uploadUrl: 'http://localhost:8000/api/upload',
      imgSrc: '',
      cropImg: '',
      imgType: ''
    }
  },
  computed: {
    imgExtension () {
      if (this.imgType.indexOf('/') > 0) {
        return this.imgType.split('/')[1]
      }
      return ''
    }
  },
  methods: {
    imageuploaded (res) {
      if (res.success) {
        alert(res.success)
      }
    },
    setImage (e) {
      const file = e.target.files[0]
      const reader = new FileReader()

      if (!file.type.includes('image/')) {
        alert('Please select an image file')
        return
      }

      this.imgType = file.type

      reader.onload = (event) => {
        this.imgSrc = event.target.result
        // replace src and rebuild the cropper
        this.$refs.cropper.replace(event.target.result)
      }

      reader.readAsDataURL(file)
    },
    startCrop () {
      // console.log(this.$refs.cropper.cropper.crop())
      // this.$refs.cropper.crop()
    },
    cropImage () {
      const newImgSrc = this.$refs.cropper.getCroppedCanvas().toDataURL(this.imgType)
      this.$refs.cropper.replace(newImgSrc)
    },
    upload () {
      this.$refs.cropper.getCroppedCanvas().toBlob((blob) => {
        const formData = new FormData()
        const fileName = 'image.' + this.imgExtension

        formData.append('file', blob, fileName)
        axios.post(this.uploadUrl, formData)
          .then(resp => {
            alert('Upload image successfully')
          })
      }, this.imgType)
    }
  }
}
</script>
