<template>
  <div class="hello">
    <div v-if="!showDownloadSection">
      <photo-uploader :height="300"
        :on-upload-success="onUploadSuccess" />
    </div>
    <div v-else>
      <el-form :inline="true" :model="cropConfig">
        <el-form-item label="Width">
          <el-input v-model="cropConfig.w" type="number"></el-input>
        </el-form-item>
        <el-form-item label="Height">
          <el-input v-model="cropConfig.h" type="number"></el-input>
        </el-form-item>
      </el-form>

      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <span>Download Link</span>
        </div>
        <p>
          <a :href="croppedDownloadLink" target="_blank">{{croppedDownloadLink}}</a>
        </p>
      </el-card>
    </div>
  </div>
</template>

<script>
import PhotoUploader from '@/components/PhotoUploader'

export default {
  name: 'HelloWorld',
  components: {PhotoUploader},
  data () {
    return {
      showDownloadSection: false,
      downloadLink: '',
      cropConfig: {
        w: null,
        h: null
      }
    }
  },
  computed: {
    croppedDownloadLink () {
      if (this.cropConfig.w && this.cropConfig.h) {
        return `${this.downloadLink}?w=${this.cropConfig.w}&h=${this.cropConfig.h}`
      }
      return this.downloadLink
    }
  },
  methods: {
    onUploadSuccess (data) {
      this.$message.success('Photo uploaded')
      this.downloadLink = data.downloadLink
      this.showDownloadSection = true
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

a,
a:link,
a:visited,
a:hover,
a:active {
  color: #409EFF
}
</style>
