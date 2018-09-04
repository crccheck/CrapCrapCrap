const DEBUG = process.env.NODE_ENV !== 'production' // eslint-disable-line no-unused-vars

exports.debug = function debug (arg0, ...args) {
  // Debug, even in prod for now
  // if (!DEBUG) { return }

  console.log(`CRAPCRAPCRAP ${arg0}`, ...args)
}
