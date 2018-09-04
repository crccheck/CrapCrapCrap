const DEBUG = process.env.NODE_ENV !== 'production'
const TRACK_URL = DEBUG ? 'http://localhost:35272/receive/' : 'https://tracker.craptobuy.com/receive/'

console.log('background script running --------------------------------------')

window.store = {
  test: 'test',
}

browser.runtime.onMessage.addListener(async (msg) => {
  // FIXME if another tab loads, it will use the current tab
  const [tab] = await browser.tabs.query({currentWindow: true, active: true})
  const { type, payload } = msg
  window.store.payload = payload
  switch (type) {
    case 'data':
      const path = payload.length ? 'icons/ccc_loaded.svg' : 'icons/ccc_error.svg'
      browser.pageAction.setIcon({ tabId: tab.id, path })
      const body = {
        referrer: msg.referrer,
        data: payload,
        v: 1,
      }
      console.log('body', body, TRACK_URL)
      try {
        const resp = await fetch(TRACK_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json; charset=utf-8',
          },
          body: JSON.stringify(body),
        })
        console.log('resp', await resp.json())
      } catch (err) {
        console.error(err)
      }
      break
    default:
      console.log('Unknown message type: %s', type)
  }

  // This doesn't work because the popup isn't open yet
  // browser.extension.getViews({type: 'popup'})
})
