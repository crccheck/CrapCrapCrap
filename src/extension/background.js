console.log('background script running --------------------------------------')
browser.pageAction.onClicked.addListener((tab) => {
  console.log('pageAction.onClicked TODO')
})

browser.runtime.onMessage.addListener(async (msg) => {
  const [tab] = await browser.tabs.query({currentWindow: true, active: true})
  browser.pageAction.setIcon({
    tabId: tab.id, path: 'icons/ccc_loaded.svg',
  })
  console.log('onMessge', msg)
})
