const { debug } = require('../utils')

exports.hosts = ['www.wayfair.com']

exports.scrape = function () {
  debug('Analyzing Wayfair page...')
  const product = [...document.querySelectorAll('script[type="application/ld+json"]')]
    .map((x) => JSON.parse(x.innerHTML))
    .find((x) => {
      return x['@type'] === 'Product'
    })
  if (!product) {
    throw new Error('No product found')
  }

  const priceData = {
    name: product.name,
    identifier: product.sku,
    url: document.querySelector('link[rel=canonical]').href,
    price: document.querySelector('.StandardPriceBlock .notranslate').innerHTML.replace(/[$,]/g, ''),
  }
  return [priceData]
}
