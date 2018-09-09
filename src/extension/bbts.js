const { debug } = require('./utils')

exports.bigbadtoystore = function bigbadtoystore () {
  const [, pageType] = window.location.pathname.split('/')
  switch (pageType) {
    case 'Search': {
      debug('analyzing', pageType)
      const $prices = document.querySelectorAll('.product-price')
      const data = []
      $prices.forEach(($elem) => {
        const price = $elem.textContent.trim().replace(/\s+/, '.').replace(/[$,]/g, '')
        let $parent = $elem.parentElement
        while (!$parent.querySelector('.product-name')) {
          $parent = $parent.parentElement
        }
        const $name = $parent.querySelector('.product-name')
        const name = $name.textContent.trim()
        const url = $name.parentElement.href
        const [, identifier] = url.match(/VariationDetails\/(\d+)/)
        data.push({ name, identifier, url, price })
      })
      return data
    }
    case 'Product': {
      debug('analyzing', pageType)
      const $price = document.querySelector('.price')
      const price = $price.textContent.trim().replace(/[$,]/g, '')
      const name = document.querySelector('.product-header h3').textContent.trim()
      const identifier = document.getElementById('ProductVariationId').value
      const url = window.location.href
      return ([{ name, identifier, url, price }])
    }
  }
}
