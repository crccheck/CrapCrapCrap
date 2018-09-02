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
console.log('browser.pageAction', browser.pageAction)
console.log('browser.runtime', browser.runtime)
function handleInstalled (details) {
  console.log('handleInstalled', details)
  // browser.tabs.create({
  //   url: "http://chilloutandwatchsomecatgifs.com/"
  // });
}

browser.runtime.onInstalled.addListener(handleInstalled);
browser.pageAction.onClicked.addListener((tab) => {
  console.log('pageAction.onClicked')
  // browser.pageAction.setIcon({
  //   tabId: tab.id, path: "icons/icon-48.png"
  // });
});
// browser.tabs.getCurrent()
