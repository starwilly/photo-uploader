<template>
<div class="center"  >
  <div v-if="mode==='WAIT_FILE'" class="step">
    <div class="toolbox">
      <el-input type="url" v-model="urlToLoad" size="mini"
                placeholder="http://wwww.example.com/test.png">
        <el-button slot="append" icon="el-icon-search" @click="loadURL"></el-button>
      </el-input>
    </div>
    <el-upload action=""
              class="dropzone canvas-container"
              :style="{height: height}"
              accept="image/*"
              drag
              :on-change="setImage"
              :auto-upload="false"
              :limit="1">
      <div class="dropzone__content" :style="{height: height + 'px'}">
        <i class="el-icon-picture dropzone__icon"></i>
        <div class="el-upload__text">Drop image here or <em>click to choose file</em></div>
      </div>
    </el-upload>
  </div>

  <div v-if="mode==='EDIT'" class="step">
    <div class="toolbox">
      <el-button type="primary" size="mini" @click="cropImage">Crop</el-button>
      <el-button type="primary" size="mini" @click="pixelate">Pixelate</el-button>
      <el-button type="primary" size="mini" @click="upload"> Upload</el-button>
    </div>
    <div class="canvas-container">
      <vue-cropper
        :container-style="{ height: height + 'px' }"
        ref="cropper"
        :guides="false"
        :view-mode="0"
        drag-mode="crop"
        :auto-crop="false"
        :auto-crop-area="0.5"
        :background="true"
        :restore="false"
        :rotatable="false"
        :zoomable="true"
        src="imgSrc"
        :ready="onCropperReady"
        alt="Source Image" />
      </vue-cropper>
    </div>
  </div>
</div>
</template>

<script>
import VueCropper from 'vue-cropperjs'
import Darkroom from '@/utils/image/darkroom'
import { uploadPhoto, loadImageFromURL } from '@/api'

export default {
  name: 'PhotoUploader',
  components: {
    'vue-cropper': VueCropper
  },
  props: {
    height: {
      type: Number,
      default: '400'
    }
  },
  data () {
    return {
      uploadUrl: '/api/upload',
      imgSrc: '',
      imgType: '',
      // urlToLoad: 'https://www.google.com.tw/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png',
      urlToLoad: '',
      darkroom: null,
      fileList: [],
      mode: 'WAIT_FILE'
    }
  },
  computed: {
    cropper () {
      return this.$refs.cropper
    }
  },
  methods: {
    onCropperReady () {
      console.log('ready')
      this.darkroom = new Darkroom(this.cropper.getCroppedCanvas())
    },
    setImage (file) {
      this.readImageFile(file.raw)
    },
    darkroomToCropper () {
      const url = this.darkroom.canvas.toDataURL(this.imgType)
      this.cropper.replace(url)
    },
    cropImage () {
      const newImgSrc = this.cropper.getCroppedCanvas().toDataURL(this.imgType)
      this.imgSrc = newImgSrc
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
      this.mode = 'EDIT'
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

<style scoped>
  .step {
    max-width: 100%;
    height: 100%;
  }

  .canvas-container {
    max-width: 100%;
  }

  .toolbox {
    margin-bottom: 10px
  }

  .dropzone__content {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .dropzone >>> .el-upload {
    width: 100%;
    height: 100%;
  }

  .dropzone >>> .el-upload-dragger  {
    width: 100%;
    height: 100%;
  }

  .dropzone__icon {
    font-size: 67px;
    color: #b4bccc;
  }

</style>
