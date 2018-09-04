console.log('popup hi -------------')

browser.runtime.getBackgroundPage().then((bgWindow) => {
  console.log('popup', bgWindow.state)
  const productCount = document.getElementById('placeholder--product-count')
  console.log(productCount, bgWindow.state.payload)
  productCount.innerHTML = bgWindow.state.payload.length
})
