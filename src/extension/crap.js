const { amazon } = require('./stores/amazon')
const { bigbadtoystore } = require('./stores/bbts')
const { debug } = require('./utils')

/*::
PriceData: { name: string, identifier: string, url: string, price: string }
*/

async function main () {
  let data/*: PriceData[] */ = []
  switch (window.location.host) {
    case 'www.amazon.com':
      try {
        data = amazon()
      } catch (err) {
        console.error(err)
      }
      break
    case 'www.bigbadtoystore.com':
      try {
        data = bigbadtoystore()
      } catch (err) {
        console.error(err)
      }
      break
    case 'www.wayfair.com':
      try {
        data = require('./stores/wayfair')()
      } catch (err) {
        console.error(err)
      }
      break
    default:
      debug('unknown host: %s', window.location.host)
  }
  const response = await browser.runtime.sendMessage({ // eslint-disable-line no-unused-vars
    payload: data,
    referrer: window.location.href,
  })
}
setTimeout(main, 200 + Math.random() * 2000)
