# Automated Posting Setup Guide

This guide explains how to set up the automated Sudoku posting workflow using GitHub Actions. By following these steps, your repository will be configured to post Sudoku puzzles to your social media accounts automatically, twice a day.

## How It Works

The repository includes a GitHub Actions workflow file (`.github/workflows/social_post.yml`) that is triggered on a schedule. When the workflow runs, it does the following:

1.  **Checks out your code:** It gets the latest version of your code from the `main` branch.
2.  **Sets up Python:** It installs the correct version of Python.
3.  **Installs dependencies:** It installs all the Python libraries needed to run the application.
4.  **Runs the scheduler:** It runs the `main.py` script in scheduler mode with the `--post-now` flag, which tells the application to generate and post a puzzle immediately.

## Configuring API Credentials

To post to your social media accounts, the workflow needs access to your API credentials. For security reasons, these credentials are not stored in the code. Instead, they are stored as **secrets** in your GitHub repository.

### Step 1: Get Your API Credentials

Before you can configure the secrets, you need to get the API credentials for each social media platform you want to use. You can find instructions on how to do this in the `README.md` file.

### Step 2: Add the Secrets to Your GitHub Repository

1.  Go to your repository on GitHub.
2.  Click on the **Settings** tab.
3.  In the left sidebar, click on **Secrets and variables**, then **Actions**.
4.  Click the **New repository secret** button.
5.  Enter the name of the secret (e.g., `INSTAGRAM_USERNAME`) and its value.
6.  Click **Add secret**.

You will need to repeat this process for each of the following secrets:

*   `INSTAGRAM_USERNAME`
*   `INSTAGRAM_PASSWORD`
*   `TWITTER_API_KEY`
*   `TWITTER_API_SECRET`
*   `TWITTER_ACCESS_TOKEN`
*   `TWITTER_ACCESS_TOKEN_SECRET`
*   `REDDIT_CLIENT_ID`
*   `REDDIT_CLIENT_SECRET`
*   `REDDIT_USERNAME`
*   `REDDIT_PASSWORD`
*   `FACEBOOK_PAGE_ID`
*   `FACEBOOK_ACCESS_TOKEN`

**Important:** The names of the secrets must be an exact match for the names listed above.

## Step 3: Enable the Platforms

Once you've added the secrets, you need to enable the platforms you want to post to in the `config.yaml` file.

1.  Open the `config.yaml` file in your repository.
2.  For each platform you want to use, set the `enabled` property to `true`. For example:

```yaml
platforms:
  instagram:
    enabled: true
  twitter:
    enabled: true
  facebook:
    enabled: false
  reddit:
    enabled: false
```

3.  Commit and push your changes to the `main` branch.

## Step 4: Verify the Workflow

The workflow is scheduled to run twice a day, but you can also trigger it manually to make sure it's working correctly.

1.  Go to the **Actions** tab in your repository.
2.  In the left sidebar, click on the **Post Daily Sudoku** workflow.
3.  Click the **Run workflow** dropdown, and then click the **Run workflow** button.

The workflow will now run. You can watch its progress in real-time. If everything is configured correctly, a new Sudoku puzzle will be posted to the social media accounts you enabled.
