const $ = (id) => document.getElementById(id)
const $wish = $('placeholder--wish')

document.body.addEventListener('click', (e) => {
  if (e.target.href) {
    e.preventDefault() // Keep Firefox from opening link
    browser.tabs.create({ active: true, url: e.target.href })
  }
})

browser.runtime.getBackgroundPage().then((bgWindow) => {
  const { state } = bgWindow
  console.log('popup state:', state)
  const $productCount = $('placeholder--product-count')
  const plural = state.payload.length === 1 ? '' : 's'
  $productCount.textContent = `${state.payload.length} product${plural} found!`

  if (state.shareUrl) {
    $wish.parentElement.classList.remove('hide')
    $wish.href = state.shareUrl
  }
})
