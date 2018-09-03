console.log('popup hi -------------')

browser.runtime.getBackgroundPage().then((bgWindow) => console.log(bgWindow.store))
