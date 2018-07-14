const HOST = 'http://localhost:8000'
const DEBUG = 1

function debug(arg0, ...args) {
  if (!DEBUG) { return }

  console.log(`CrapCrapCrap ${arg0}`, ...args)
}

function sendUpdate(data) {
  const payload = {
    referrer: window.location.href,
    data,
    v: 1,
  }
  // debug(JSON.stringify(payload, null, 2))
  debug('sendUpdate %d items', data.length)
  fetch(`${HOST}/receive`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      body: JSON.stringify(payload),
    }
  })
    .then(console.log)
    .catch(console.error)
}

function bigbadtoystore() {
  const [,pageType] = window.location.pathname.split('/')
  switch (pageType) {
    case 'Search': {
      debug('analyzing', pageType)
      const $prices = document.querySelectorAll('.product-price')
      const data = []
      $prices.forEach(($elem) => {
        const price = $elem.textContent.trim().replace(/\s+/, '.').replace('$', '')
        let $parent = $elem.parentElement
        while (!$parent.querySelector('.product-name')) {
          $parent = $parent.parentElement
        }
        const $name = $parent.querySelector('.product-name')
        const name = $name.textContent.trim()
        const url = $name.parentElement.href
        const [,identifier] = url.match(/VariationDetails\/(\d+)/)
        data.push({ name, identifier, url, price })
      })
      sendUpdate(data)
    }
    break
    case 'Product': {
      debug('analyzing', pageType)
      const $price = document.querySelector('.price')
      const price = $price.textContent.trim().replace('$', '')
      const name = document.querySelector('.product-header h3').textContent.trim()
      const identifier = document.getElementById('ProductVariationId').value
      const url = window.location.href
      sendUpdate([{ name, identifier, url, price}])
    }
    break
  }
}

function main() {
  debug('started')
  switch (window.location.host) {
    case 'www.bigbadtoystore.com':
      bigbadtoystore()
    break
  }
}

setTimeout(main, 200 + Math.random() * 2000)
