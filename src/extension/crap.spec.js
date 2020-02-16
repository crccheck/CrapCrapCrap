global.window = {
  location: {
    host: {},
  },
}

describe('extension js', () => {
  it('loads with unknown host', () => {
    require('./crap')
  })
})
