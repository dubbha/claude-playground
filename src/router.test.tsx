import { describe, expect, it } from 'vitest'
import { getRouter } from './router'

describe('getRouter', () => {
  it('creates a router with the generated route tree', () => {
    const router = getRouter()
    expect(router.routesByPath['/']).toBeDefined()
  })
})
