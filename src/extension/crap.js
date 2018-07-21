const { debug, sendUpdate } = require('./utils')
const { bigbadtoystore } = require('./bbts')

function main () {
  debug('started')
  switch (window.location.host) {
    case 'www.bigbadtoystore.com':
      const data = bigbadtoystore()
      if (data) {
        sendUpdate(data)
      }
      break
  }
}

setTimeout(main, 200 + Math.random() * 2000)
