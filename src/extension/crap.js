const { debug, sendUpdate } = require('./utils')
const { bigbadtoystore } = require('./bbts')
const { amazon } = require('./amazon')

function main () {
  console.log('HHHHHHHHHHHHHHHHH')
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
  if (data) {
    sendUpdate(data)
  }
}

setTimeout(main, 200 + Math.random() * 2000)
