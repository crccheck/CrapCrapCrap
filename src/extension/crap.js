const { debug } = require('./utils')

/*::
PriceData: { name: string, identifier: string, url: string, price: string }
*/

const scrapers = new Map([
  ['www.amazon.com', require('./stores/amazon').scrape],
  ['www.bigbadtoystore.com', require('./stores/bbts').scrape],
  ['www.wayfair.com', require('./stores/wayfair').scrape],
])
async function main () {
  if (!scrapers.has(window.location.host)) {
    debug('unknown host: %s', window.location.host)
    return
  }

  const scraper = scrapers.get(window.location.host)
  let data/*: PriceData[] */ = []
  try {
    data = scraper()
  } catch (err) {
    debug(err)
  }
  const response = await browser.runtime.sendMessage({ // eslint-disable-line no-unused-vars
    payload: data,
    referrer: window.location.href,
  })
}

setTimeout(main, 200 + Math.random() * 2000)
