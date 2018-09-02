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
    browser.runtime.sendMessage({
      type: 'data',
      payload: data,
    })
    sendUpdate(data)
  }
}
setTimeout(main, 200 + Math.random() * 2000)
