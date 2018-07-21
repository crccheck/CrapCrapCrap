const { debug } = require('./utils')
const { bigbadtoystore } = require('./bbts')

function main () {
  debug('started')
  switch (window.location.host) {
    case 'www.bigbadtoystore.com':
      bigbadtoystore()
      break
  }
}

setTimeout(main, 200 + Math.random() * 2000)
