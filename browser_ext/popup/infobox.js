browser.runtime.getBackgroundPage().then((bgWindow) => {
  const { state } = bgWindow
  console.log('popup state:', state)
  const $productCount = document.getElementById('placeholder--product-count')
  const plural = state.payload.length === 1 ? '' : 's'
  $productCount.innerHTML = `${state.payload.length} product${plural} found!`

  const $wish = document.getElementById('placeholder--wish')
  if (state.shareUrl) {
    $wish.href = state.shareUrl
  }
})
