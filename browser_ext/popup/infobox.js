browser.runtime.getBackgroundPage().then((bgWindow) => {
  const { state } = bgWindow
  console.log('popup state:', state)
  const $productCount = document.getElementById('placeholder--product-count')
  $productCount.innerHTML = state.payload.length

  const $share = document.getElementById('placeholder--share')
  if (state.shareUrl) {
    $share.href = state.shareUrl
  }
})
