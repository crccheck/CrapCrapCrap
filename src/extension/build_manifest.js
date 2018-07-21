const fs = require('fs')
const path = require('path')

const pkg = require('../../package.json')
const manifest = require('./manifest.json')

const OUT_FILE = path.join(__dirname, '..', '..', 'browser_ext', 'manifest.json')

manifest.version = pkg.version
if (process.env.NODE_ENV === 'production') {
  manifest.permissions = ['https://tracker.craptobuy.com/*']
} else {
  manifest.permissions = ['http://localhost/*']
}

fs.writeFileSync(OUT_FILE, JSON.stringify(manifest, null, 2))
