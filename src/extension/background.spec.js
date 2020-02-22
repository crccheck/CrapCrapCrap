const assert = require('assert')

global.browser = {
  runtime: {
    onMessage: {
      addListener: () => {},
    },
  },
}

describe('background', () => {
  it('sets window.state', () => {
    require('./background')
    assert.ok(window.state)
    assert.ok(window.state.payload)
  })
})
