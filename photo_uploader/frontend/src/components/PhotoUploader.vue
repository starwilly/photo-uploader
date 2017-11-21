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
  <button @click="pixelate">Pixelate</button>
  <button @click="upload">Upload</button>

</div>
</template>

<script>
import VueCropper from 'vue-cropperjs'
import * as axios from 'axios'

function startPixelate (img, canvas, cropData) {
  const ctx = canvas.getContext('2d')
  ctx.mozImageSmoothingEnabled = false
  ctx.webkitImageSmoothingEnabled = false
  ctx.imageSmoothingEnabled = false
  // // cache scaled width and height
  const w = cropData.width * 0.1
  const h = cropData.height * 0.1

  // // draw original image to the scaled size
  ctx.drawImage(img, 0, 0, w, h)

  // // then draw that scaled image thumb back to fill canvas
  // // As smoothing is off the result will be pixelated
  ctx.drawImage(canvas, 0, 0, w, h, cropData.x, cropData.y, cropData.width, cropData.height)
  return canvas
}

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
    pixelate () {
      // const size = 25 * 0.01
      const cropper = this.$refs.cropper
      const croppedCanvas = cropper.getCroppedCanvas()
      const cropData = cropper.getData()

      // console.log(croppedCanvas)
      // console.log('cropBoxData', cropBoxData)

      cropper.clear()
      const canvas = cropper.getCroppedCanvas()

      const img = new Image()

      img.onload = function () {
        const pixelatedCanvas = startPixelate(this, canvas, cropData)
        cropper.replace(pixelatedCanvas.toDataURL(this.imgType))
      }
      img.src = croppedCanvas.toDataURL(this.imgType)

      // function test () {
      //   const ctx = canvas.getContext('2d')
      //   ctx.mozImageSmoothingEnabled = false
      //   ctx.webkitImageSmoothingEnabled = false
      //   ctx.imageSmoothingEnabled = false
      //   // // cache scaled width and height
      //   const w = canvas.width * 0.05
      //   const h = canvas.height * 0.05

      //   // // draw original image to the scaled size
      //   ctx.drawImage(img, 0, 0, w, h)

      //   // // then draw that scaled image thumb back to fill canvas
      //   // // As smoothing is off the result will be pixelated
      //   ctx.drawImage(canvas, 0, 0, w, h, 0, 0, canvas.width, canvas.height)

      //   cropper.replace(canvas.toDataURL(this.imgType))
      // }
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
