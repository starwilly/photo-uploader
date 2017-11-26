<template>
<div class="center">

  <input type="file" name="image" accept="image/*" @change="setImage"/>
  <br>
  <input type="url"
         placeholder="http://wwww.example.com/test.png"
         v-model="urlToLoad"
         />
  <button @click="loadURL">Load</button>

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
          :ready="onCropperReady"
          alt="Source Image"
          :img-style="{ width: '400px', height: '300px' }"
          >
      </vue-cropper>
  </div>
  <br>
  <button @click="startCrop">Select</button>
  <button @click="cropImage">Crop</button>
  <button @click="pixelate">Pixelate</button>
  <button @click="upload">Upload</button>

</div>
</template>

<script>
import VueCropper from 'vue-cropperjs'
// import axios from 'axios'
import Darkroom from '@/utils/image/darkroom'
import {
  uploadPhoto,
  loadImageFromURL
} from '@/api'

export default {
  name: 'PhotoUploader',
  components: {
    'vue-cropper': VueCropper
  },
  data () {
    return {
      uploadUrl: '/api/upload',
      imgSrc: '',
      imgType: '',
      urlToLoad: 'https://www.google.com.tw/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png',
      darkroom: null
    }
  },
  computed: {
    imgExtension () {
      if (this.imgType.indexOf('/') > 0) {
        return this.imgType.split('/')[1]
      }
      return ''
    },
    cropper () {
      return this.$refs.cropper
    }
  },
  methods: {
    onCropperReady () {
      this.darkroom = new Darkroom(this.cropper.getCroppedCanvas())
    },
    setImage (e) {
      const file = e.target.files[0]

      if (!file.type.includes('image/')) {
        alert('Please select an image file')
        return
      }

      // this.imgType = file.type
      this.readImageFile(file)
    },
    darkroomToCropper () {
      const url = this.darkroom.canvas.toDataURL(this.imgType)
      this.cropper.replace(url)
    },
    startCrop () {
      // console.log(this.$refs.cropper.cropper.crop())
      // this.$refs.cropper.crop()
    },
    cropImage () {
      const newImgSrc = this.cropper.getCroppedCanvas().toDataURL(this.imgType)
      this.cropper.replace(newImgSrc)
    },
    pixelate () {
      const cropData = this.cropper.getData(true)
      this.cropper.clear()
      this.darkroom.pixelate(cropData)
      this.darkroomToCropper()
    },
    readImageFile (file) {
      const reader = new FileReader()
      reader.onload = event => {
        this.imgType = file.type
        this.cropper.replace(event.target.result)
      }
      reader.readAsDataURL(file)
    },
    loadURL () {
      loadImageFromURL(this.urlToLoad)
        .then(resp => this.readImageFile(resp.data))
        .catch(err => {
          console.log(err.response)
        })
    },
    upload () {
      this.cropper.getCroppedCanvas().toBlob((blob) => {
        uploadPhoto(blob)
          .then(resp => {
            alert(resp.data.downloadLink)
          })
      }, this.imgType)
    }
  }
}
</script>
