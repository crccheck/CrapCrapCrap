const { amazon } = require('./amazon')
const { bigbadtoystore } = require('./bbts')
const { debug, sendUpdate } = require('./utils')

function main () {
  debug('started')
  let data
  switch (window.location.host) {
    case 'www.amazon.com':
      data = amazon()
      break
    case 'www.bigbadtoystore.com':
      data = bigbadtoystore()
      break
  }
  if (data && data.length) {
    sendUpdate(data)
  }
}
// setTimeout(main, 200 + Math.random() * 2000)
console.log('browser', browser)
console.log('browser.tabs', browser.tabs)
browser.tabs.query({active: true, currentWindow: true})
  .then(console.log)
