const { debug } = require('./utils')

exports.amazon = function amazon () {
  const aState = {}
  document.querySelectorAll('script[type=a-state]').forEach((x) => {
    const { key } = JSON.parse(x.dataset.aState)
    aState[key] = JSON.parse(x.innerHTML)
  })
  // console.log('hi', )
  debug('aState', aState)
  const $price = document.querySelector('#_mediaPrice .value')
  const price = $price.textContent.trim().replace(/[$,]/g, '')
  const name = document.getElementById('productTitle').textContent.trim()
  const identifier = aState['URL-Refresh-State'].landingAsin
  const url = document.querySelector('link[rel=canonical]').href
  return [{name, identifier, url, price}]
}
