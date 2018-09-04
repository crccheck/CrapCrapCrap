browser.runtime.getBackgroundPage().then((bgWindow) => {
  const { state } = bgWindow
  console.log('popup state:', state)
  const $productCount = document.getElementById('placeholder--product-count')
  $productCount.innerHTML = state.payload.length

  const $wish = document.getElementById('placeholder--wish')
  if (state.shareUrl) {
    $wish.href = state.shareUrl
  }
})
