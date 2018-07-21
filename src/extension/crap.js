const { debug, sendUpdate } = require('./utils')
const { bigbadtoystore } = require('./bbts')
const { amazon } = require('./amazon')

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

setTimeout(main, 200 + Math.random() * 2000)
