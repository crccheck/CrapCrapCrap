const DEBUG = process.env.NODE_ENV !== 'production'
const TRACK_URL = DEBUG ? 'http://localhost:35272/receive/' : 'https://tracker.craptobuy.com/receive/'

exports.debug = function debug (arg0, ...args) {
  // Debug, even in prod for now
  // if (!DEBUG) { return }

  console.log(`CRAPCRAPCRAP ${arg0}`, ...args)
}

exports.sendUpdate = async function (data) {
  const payload = {
    referrer: window.location.href,
    data,
    v: 1,
  }
  // debug(JSON.stringify(payload, null, 2))
  exports.debug('sendUpdate %d items', data.length, TRACK_URL)
  return fetch(TRACK_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
    },
    body: JSON.stringify(payload),
  })
}
