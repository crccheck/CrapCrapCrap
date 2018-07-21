const { debug } = require('./utils')

exports.amazon = function amazon () {
  const url = document.querySelector('link[rel=canonical]').href
  const identifier = url.match(/\/dp\/(\w+)/)[1]
  debug('identifier', identifier)
  const name = document.getElementById('productTitle').textContent.trim()
  debug('name', name)
  const $price = document.querySelector('#_mediaPrice .value, #priceblock_ourprice')
  const price = $price.textContent.replace(/[$,]/g, '').trim().replace(/\s+/, '.')
  debug('price', price)
  return [{name, identifier, url, price}]
}
