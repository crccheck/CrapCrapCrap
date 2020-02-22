global.window = {
  location: {
    host: {},
  },
}

const crap = require('./crap')


describe('extension js', () => {
  it('loads with unknown host', async () => {
    await crap.main()
  })
})
