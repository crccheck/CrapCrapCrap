const { amazon } = require('./amazon')
const { bigbadtoystore } = require('./bbts')

async function main () {
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
      try {
        data = bigbadtoystore()
      } catch (err) {
        console.error(err)
        data = []
      }
      break
  }
  const response = await browser.runtime.sendMessage({ // eslint-disable-line no-unused-vars
    payload: data,
    referrer: window.location.href,
  })
}
setTimeout(main, 200 + Math.random() * 2000)
