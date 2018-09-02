console.log('background')
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

browser.runtime.onInstalled.addListener(handleInstalled)
browser.pageAction.onClicked.addListener((tab) => {
  console.log('pageAction.onClicked')
  // browser.pageAction.setIcon({
  //   tabId: tab.id, path: "icons/icon-48.png"
  // });
})
// browser.tabs.getCurrent()

browser.runtime.onMessage.addListener((msg) => {
  console.log('onMessge', msg)
  browser.tabs.query({currentWindow: true, active: true}).then((x) => console.log('query', x))
})
