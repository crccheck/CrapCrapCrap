const pkg = require('../../package.json')
const manifest = require('./manifest.json')

manifest.version = pkg.version
if (process.env.NODE_ENV === 'production') {
  manifest.permissions = ['https://tracker.craptobuy.com/*', 'activeTab']
} else {
  manifest.permissions = ['http://localhost/*', 'activeTab']
}
manifest.page_action.show_matches = manifest.content_scripts[0].matches

console.log(JSON.stringify(manifest, null, 2))
