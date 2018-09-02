const { amazon } = require('./amazon')
const { bigbadtoystore } = require('./bbts')
const { debug, sendUpdate } = require('./utils')

async function main () {
  debug('started')
  let data
  switch (window.location.host) {
    case 'www.amazon.com':
      try {
        data = amazon()
      } catch (err) {
        console.error(err)
        data = []
      }
      break
    case 'www.bigbadtoystore.com':
      data = bigbadtoystore()
      break
  }
  try {
    if (data && data.length) {
      await sendUpdate(data)
    }
  } catch (err) {
    debug(err)
  } finally {
    browser.runtime.sendMessage({
      type: 'data',
      payload: data,
    })
  }
}
setTimeout(main, 200 + Math.random() * 2000)
