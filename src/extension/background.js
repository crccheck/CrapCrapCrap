console.log('background script running --------------------------------------')
browser.pageAction.onClicked.addListener((tab) => {
  console.log('pageAction.onClicked TODO')
})

browser.runtime.onMessage.addListener(async (msg) => {
  // FIXME if another tab loads, it will use the current tab
  const [tab] = await browser.tabs.query({currentWindow: true, active: true})
  const { type, payload } = msg
  switch (type) {
    case 'data':
      const path = payload.length ? 'icons/ccc_loaded.svg' : 'icons/ccc_error.svg'
      browser.pageAction.setIcon({ tabId: tab.id, path })
      break
    default:
      console.log('Unknown message type: %s', type)
  }
})
