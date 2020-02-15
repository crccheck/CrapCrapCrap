IMPORTANT: This directory is the source template for the web extension.
[`manifest.json`] won't be valid in this directory.


Usage
=====

### Firefox

From the project root, run the watcher:

    make ext/dev

And in another terminal, run "web-ext":

    make web-ext

"web-ext" needs to be separate so you can control reloads.

### Chrome

https://developer.chrome.com/extensions/getstarted

1. Enable "Developer mode"
2. Install Extensions Reloader
   https://chrome.google.com/webstore/detail/extensions-reloader/fimgfedafeadlieiabdeeaodndnlbhid
3. Run `make ext/dev` to make sure `browser_ext` is built
4. "Load unpacked" the [`browser_ext`] directory


Firefox/Chrome cross-compatibility weirdness
============================================

`browser` vs `chrome` global
----------------------------

The easiest thing to do is stick with `browser` and use the
[webextension-polyfill] for Chrome compatibility.


Chrome doesn't support svg
--------------------------

Any icons listed in [`manifest.json`] have to be PNG. Any icons
programmatically set (e.g. `browser.pageAction.setIcon`) will take SVG fine.


Displaying popups
-----------------

Firefox uses `show_matches` in [`manifest.json`], but in Chrome, it's set
programmatically.


  [webextension-polyfill]: https://github.com/mozilla/webextension-polyfill
  [`browser_ext`]: ../browser_ext
  [`manifest.json`]: ./manifest.json
