const DEBUG = process.env.NODE_ENV !== 'production'
const TRACK_URL = DEBUG ? 'http://localhost:35272/receive/' : 'https://tracker.craptobuy.com/receive/'

console.log('background script running --------------------------------------')

window.state = {
  payload: [],
  shareUrl: null,
}

// TODO Chrome doesn't like the default svg icon and supports show/hide

browser.runtime.onMessage.addListener(async (msg, sender) => {
  // const [tab] = await browser.tabs.query({ currentWindow: true, active: true })
  const { tab } = sender
  // Chrome doesn't support `show_matches` from the `manifest.json`
  browser.pageAction.show(tab.id)
  const { referrer, payload } = msg
  window.state.payload = payload
  const path = payload.length ? 'icons/ccc_loaded.svg' : 'icons/ccc_error.svg'
  browser.pageAction.setIcon({ tabId: tab.id, path })
  const body = {
    referrer,
    data: payload,
    v: 1,
  }
  const ret = {}
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
    ret.status = 200
  } catch (err) {
    console.error(err)
    ret.error = err
  }

  return ret
})
