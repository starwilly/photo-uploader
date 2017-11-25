
function disableSmoothRendering (ctx) {
  ctx.mozImageSmoothingEnabled = false
  ctx.webkitImageSmoothingEnabled = false
  ctx.msImageSmoothingEnabled = false
  ctx.imageSmoothingEnabled = false
  return ctx
}

export default class Darkroom {
  constructor (canvas) {
    this.canvas = canvas
    this.origWidth = canvas.width
    this.origHeight = canvas.height
  }

  pixelate ({ x = 0,
              y = 0,
              width = this.origWidth,
              height = this.origHeight } = {}) {
    const scaleWidth = Math.round(width * 0.1)
    const scaleHeight = Math.round(height * 0.1)
    const ctx = this.canvas.getContext('2d')
    disableSmoothRendering(ctx)
    ctx.drawImage(this.canvas, x, y, width, height, x, y, scaleWidth, scaleHeight)
    ctx.drawImage(this.canvas, x, y, scaleWidth, scaleHeight, x, y, width, height)
    return this.canvas
  }
}
