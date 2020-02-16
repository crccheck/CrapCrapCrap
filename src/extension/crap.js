const { debug } = require('./utils')

/*::
PriceData: { name: string, identifier: string, url: string, price: string }
*/

const allScrapers = [
  require('./stores/amazon'),
  require('./stores/bbts'),
  require('./stores/wayfair'),
]

async function main () {
  const scraper = allScrapers.find((x) => x.hosts.includes(window.location.host))
  if (!scraper) {
    debug('unknown host: %s', window.location.host)
    return
  }

  let data/*: PriceData[] */ = []
  try {
    data = scraper.scrape()
  } catch (err) {
    debug(err)
  }
  const response = await browser.runtime.sendMessage({ // eslint-disable-line no-unused-vars
    payload: data,
    referrer: window.location.href,
  })
}

setTimeout(main, 200 + Math.random() * 2000)
