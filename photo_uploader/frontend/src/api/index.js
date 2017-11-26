import axios from 'axios'

function requestBlob (method, url, data) {
  return new Promise((resolve, reject) => {
    function rejectXhr () {
      const err = new Error('Cannot fetch file')
      let data = {}
      try {
        data = JSON.parse(this.response)
      } catch (e) {}

      err.response = {
        status: this.status,
        data: data
      }
      reject(err)
    }

    function onload () {
      if (this.status >= 200 && this.status < 300) {
        resolve({
          data: xhr.response
        })
      } else {
        rejectXhr.apply(this)
      }
    }

    function onreadystatechange () {
      if (this.readyState === 2) {
        if (this.status >= 200 && this.status < 300) {
          this.responseType = 'blob'
        } else {
          this.responseType = 'text'
        }
      }
    }

    // Use XMLHttpRequest rather than axios to change
    // `responseType` dynamically base on status
    const xhr = new XMLHttpRequest()
    xhr.onreadystatechange = onreadystatechange
    xhr.onload = onload
    xhr.onerror = rejectXhr

    xhr.open(method, url)
    xhr.setRequestHeader('Content-Type', 'application/json;charset=utf-8')
    xhr.send(JSON.stringify(data))
  })
}

export function uploadPhoto (blob) {
  const formData = new FormData()
  const fileName = 'photo.png'
  formData.append('file', blob, fileName)
  return axios.post('/api/upload', formData)
}

export function loadImageFromURL (url) {
  return requestBlob('POST', '/api/load', {url})
}
