const DEBUG = process.env.NODE_ENV !== 'production'
const TRACK_URL = DEBUG ? 'http://localhost:35272/receive/' : 'https://tracker.craptobuy.com/receive/'

console.log('background script running --------------------------------------')

window.state = {
  payload: [],
  shareUrl: null,
}

browser.runtime.onMessage.addListener(async (msg) => {
  // FIXME if another tab loads, it will use the current tab
  const [tab] = await browser.tabs.query({ currentWindow: true, active: true })
  const { referrer, payload } = msg
  window.state.payload = payload
  const path = payload.length ? 'icons/ccc_loaded.svg' : 'icons/ccc_error.svg'
  browser.pageAction.setIcon({ tabId: tab.id, path })
  const body = {
    referrer,
    data: payload,
    v: 1,
  }
  try {
    const resp = await fetch(TRACK_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
      },
      body: JSON.stringify(body),
    })
    const respData = await resp.json()
    window.state.shareUrl = respData.search_url
  } catch (err) {
    console.error(err)
  }

  // This doesn't work because the popup isn't open yet
  // browser.extension.getViews({type: 'popup'})
})
