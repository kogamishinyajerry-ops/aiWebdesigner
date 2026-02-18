/**
 * Home Page E2E Tests
 */

import { test, expect } from '@playwright/test'

test.describe('Home Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('has correct title', async ({ page }) => {
    await expect(page).toHaveTitle(/AI Designer/)
  })

  test('shows hero section', async ({ page }) => {
    const hero = page.locator('h1')
    await expect(hero).toContainText('AI Designer')
  })

  test('has start button', async ({ page }) => {
    const button = page.getByRole('button', { name: /start creating/i })
    await expect(button).toBeVisible()
  })

  test('navigates to dashboard on start button click', async ({ page }) => {
    const button = page.getByRole('button', { name: /start creating/i })
    await button.click()
    await expect(page).toHaveURL(/\/dashboard/)
  })

  test('shows feature cards', async ({ page }) => {
    const cards = page.locator('[class*="card"]')
    await expect(cards).toHaveCount(3)
  })
})
