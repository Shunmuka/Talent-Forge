import { test, expect } from '@playwright/test';

test.describe('Analyze Happy Path', () => {
  test('should complete full analyze flow', async ({ page }) => {
    // Navigate to home page
    await page.goto('http://localhost:3000');

    // Fill in resume text
    await page.fill('textarea[placeholder*="resume"]', 'Software Engineer with 5 years of experience in Python and JavaScript. Led multiple projects and improved performance by 30%.');

    // Fill in job description
    await page.fill('textarea[placeholder*="job description"]', 'We are looking for a Senior Software Engineer with experience in Python, JavaScript, and React. Must have leadership experience.');

    // Click analyze button
    await page.click('button:has-text("Analyze Resume")');

    // Wait for navigation to results page
    await page.waitForURL('**/results**', { timeout: 10000 });

    // Check that results page loaded
    await expect(page.locator('h1:has-text("Analysis Results")')).toBeVisible();

    // Check that score is displayed
    await expect(page.locator('text=/\\d+/')).toBeVisible();

    // Check that gaps section exists
    await expect(page.locator('h2:has-text("Skill Gaps")')).toBeVisible();

    // Check that bullets section exists
    await expect(page.locator('h2:has-text("Resume Bullets")')).toBeVisible();
  });
});
