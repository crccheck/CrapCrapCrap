IMPORTANT: This directory is the source template for the web extension.
[`manifest.json`] won't be valid in this directory.


Usage
=====

### Firefox


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
  [`manifest.json`]: ./manifest.json
