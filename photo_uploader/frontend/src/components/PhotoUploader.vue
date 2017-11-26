<template>
<div class="center">

  <input type="file" name="image" accept="image/*" @change="setImage"/>
  <br>
  <input type="url"
         placeholder="http://wwww.example.com/test.png"
         v-model="urlToLoad"
         />
  <button @click="loadImageFromURL">Load</button>

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
import axios from 'axios'
import Darkroom from '@/utils/image/darkroom'

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
    imageuploaded (res) {
      if (res.success) {
        alert(res.success)
      }
    },
    setImage (e) {
      const file = e.target.files[0]

      if (!file.type.includes('image/')) {
        alert('Please select an image file')
        return
      }

      this.imgType = file.type
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
        this.cropper.replace(event.target.result)
      }
      reader.readAsDataURL(file)
    },
    loadImageFromURL () {
      const url = '/api/load-url'

      const handleSuccess = function (blob, request) {
        this.imgType = request.getResponseHeader('Content-Type')
        this.readImageFile(blob)
      }.bind(this)

      const handleError = function (errResp) {
        console.log(errResp)
      }
      // Use XMLHttpRequest since axios cannot handle json response
      // when we set responseType = `blob`
      const request = new XMLHttpRequest()
      request.onreadystatechange = function () {
        if (request.readyState === 4) {
          if (request.status >= 200 && request.status < 300) {
            handleSuccess(request.response, request)
          } else {
            handleError(request.response)
          }
        } else if (request.readyState === 2) {
          if (request.status === 200) {
            request.responseType = 'blob'
          } else {
            request.responseType = 'json'
          }
        }
      }
      request.open('POST', url, true)
      request.setRequestHeader('Content-Type', 'application/json;charset=utf-8')
      request.send(JSON.stringify({url: this.urlToLoad}))
    },
    upload () {
      this.cropper.getCroppedCanvas().toBlob((blob) => {
        const formData = new FormData()
        const fileName = 'image.' + this.imgExtension

        formData.append('file', blob, fileName)
        axios.post(this.uploadUrl, formData)
          .then(resp => {
            alert(resp.data.downloadLink)
          })
      }, this.imgType)
    }
  }
}
</script>
