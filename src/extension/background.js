const DEBUG = process.env.NODE_ENV !== 'production'
const TRACK_URL = DEBUG ? 'http://localhost:35272/receive/' : 'https://tracker.craptobuy.com/receive/'

console.log('background script running --------------------------------------')

window.state = {
  payload: [],
  shareUrl: null,
}

browser.runtime.onMessage.addListener(async (msg, sender) => {
  // const [tab] = await browser.tabs.query({ currentWindow: true, active: true })
  const { tab } = sender
  // Chrome ignores `show_matches` in `manifest.json`, so this enables the popup instead
  browser.pageAction.show(tab.id)
  const { referrer, payload } = msg
  window.state.payload = payload
  if (!payload.length) {
    browser.pageAction.setIcon({ tabId: tab.id, path: 'icons/ccc_error.png' })
    return
  }

  browser.pageAction.setIcon({ tabId: tab.id, path: 'icons/ccc_loaded.png' })
  const body = {
    referrer,
    data: payload,
    v: 1,
  }
  const ret = {}
  const url = new URL(TRACK_URL)
  // Add referrer so access logs make more sense
  url.searchParams.append('referrer', referrer)

  try {
    const resp = await fetch(url.toString(), {
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
