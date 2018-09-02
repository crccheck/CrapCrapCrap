const pkg = require('../../package.json')
const manifest = require('./manifest.json')

manifest.version = pkg.version
if (process.env.NODE_ENV === 'production') {
  manifest.permissions = ['https://tracker.craptobuy.com/*', 'activeTab']
} else {
  manifest.permissions = ['http://localhost/*', 'activeTab']
}

console.log(JSON.stringify(manifest, null, 2))
