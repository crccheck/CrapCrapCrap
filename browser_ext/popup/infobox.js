console.log('popup hi -------------')

browser.runtime.getBackgroundPage().then((bgWindow) => {
  console.log('popup', bgWindow.store)
  const productCount = document.getElementById('placeholder--product-count')
  console.log(productCount, bgWindow.store.payload)
  productCount.innerHTML = bgWindow.store.payload.length
})
