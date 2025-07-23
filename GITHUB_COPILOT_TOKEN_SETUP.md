# GitHub Copilot Token Setup Guide

This guide provides updated instructions for obtaining and configuring authentication tokens for GitHub Copilot development and usage.

## Table of Contents

1. [Overview](#overview)
2. [Development Setup (for Extension Development)](#development-setup-for-extension-development)
3. [Production Usage (for End Users)](#production-usage-for-end-users)
4. [Authentication Methods](#authentication-methods)
5. [Troubleshooting](#troubleshooting)
6. [Security Best Practices](#security-best-practices)

## Overview

GitHub Copilot supports multiple authentication methods depending on your use case:

- **OAuth Device Flow** - For development and testing (recommended for contributors)
- **Personal Access Tokens (PAT)** - For programmatic access and specific integrations
- **OAuth Apps** - For third-party integrations
- **GitHub Apps** - For enterprise and organizational use

## Development Setup (for Extension Development)

### Method 1: Automated Setup Script (Recommended)

For GitHub Copilot extension development, use the built-in setup script:

```bash
# Install dependencies
npm install

# Run the automated token setup
npm run get_token
```

This script will:

1. **Request device authorization** from GitHub
2. **Display a user code** for you to copy
3. **Open your browser** to GitHub's authorization page
4. **Wait for authorization** and automatically retrieve the token
5. **Save the token** to your `.env` file

#### Step-by-step process:

1. Run `npm run get_token`
2. Copy the displayed user code (e.g., `ABCD-1234`)
3. Press any key to open GitHub in your browser
4. Paste the code when prompted
5. Click "Continue" and then "Authorize"
6. Wait for the script to confirm successful token generation

### Method 2: Manual OAuth Device Flow

If you need to manually implement the OAuth flow:

```bash
# Start the setup script
npm run get_token

# Or run directly with tsx
npx tsx script/setup/getToken.mts
```

### Method 3: Environment Setup Only

If you already have a token, you can set it manually:

```bash
# Create or update .env file
echo "GITHUB_OAUTH_TOKEN=ghp_your_token_here" >> .env
```

## Production Usage (for End Users)

### Visual Studio Code

1. **Install the GitHub Copilot extension** from the VS Code marketplace
2. **Sign in to GitHub** when prompted
3. **Choose your authentication method**:
   - **OAuth (Recommended)**: One-click sign-in via browser
   - **Device Code**: Manual code entry process
   - **PAT**: Manual token configuration

#### OAuth Setup in VS Code:
1. Open VS Code Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
2. Type "GitHub Copilot: Sign In"
3. Choose "Sign in with GitHub"
4. Complete authorization in your browser

#### Manual PAT Setup in VS Code:
1. Create a Personal Access Token on GitHub with `repo` scope
2. Open VS Code Command Palette
3. Type "GitHub Copilot: Sign In with GitHub Token"
4. Paste your token when prompted

### JetBrains IDEs

1. **Install GitHub Copilot plugin** from JetBrains Marketplace
2. **Sign in via Settings**:
   - Go to `File` → `Settings` → `Tools` → `GitHub Copilot`
   - Click "Sign in to GitHub"
   - Complete OAuth flow in browser

### Other Editors

For editors supporting MCP (Model Context Protocol):

#### Remote GitHub MCP Server with OAuth:
```json
{
  "servers": {
    "github": {
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```

#### Remote GitHub MCP Server with PAT:
```json
{
  "servers": {
    "github": {
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer YOUR_GITHUB_PAT"
      }
    }
  }
}
```

## Authentication Methods

### OAuth 2.0 Device Flow (Recommended for Development)

**Advantages:**
- Secure and user-friendly
- No need to handle secrets in code
- Automatic token refresh
- Follows GitHub's recommended practices

**Use cases:**
- Extension development
- Local development environments
- Interactive applications

**Implementation:**
```typescript
// Device authorization request
const deviceResponse = await fetch('https://github.com/login/device/code', {
  method: 'POST',
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    client_id: 'your_client_id',
    scope: 'repo'
  })
});
```

### Personal Access Tokens (PAT)

**Types of PATs:**
- **Classic PATs**: Traditional tokens with broad scopes
- **Fine-grained PATs**: More granular permissions (recommended)

**Required Scopes:**
- `repo` - Full repository access (required for private repos)
- `read:packages` - For package registry access
- `user:email` - For user identification

**Creating a PAT:**
1. Go to [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token"
3. Select scopes based on your needs
4. Set appropriate expiration date
5. Generate and copy the token

### GitHub Apps (Enterprise)

For organizational use, consider creating a GitHub App:

1. **Create GitHub App** in your organization settings
2. **Configure permissions** (repository access, API permissions)
3. **Install the app** in target repositories
4. **Generate installation tokens** programmatically

## Troubleshooting

### Common Issues

#### "Authentication failed" error
```bash
# Check if token is correctly set
grep GITHUB_OAUTH_TOKEN .env

# Verify token has correct scopes
curl -H "Authorization: Bearer $GITHUB_OAUTH_TOKEN" https://api.github.com/user
```

#### "Token expired" error
```bash
# Regenerate token
npm run get_token

# Or update existing token manually
```

#### "Rate limit exceeded" error
- Check your token's rate limits
- Consider using a GitHub App for higher limits
- Implement proper rate limiting in your application

#### "Insufficient permissions" error
- Ensure your token has the `repo` scope
- For organization repositories, check organization policies
- Verify repository access permissions

### Debug Commands

```bash
# Test token validity
curl -H "Authorization: Bearer $GITHUB_OAUTH_TOKEN" \
     -H "Accept: application/vnd.github.v3+json" \
     https://api.github.com/user

# Check token scopes
curl -I -H "Authorization: Bearer $GITHUB_OAUTH_TOKEN" \
        https://api.github.com/user

# Test Copilot API access
curl -H "Authorization: Bearer $GITHUB_OAUTH_TOKEN" \
     https://api.github.com/copilot_internal/user
```

### Environment Issues

#### TTY Environment Error
If you see "Not running in a TTY environment":
- Run the script in an interactive terminal
- For CI/CD, use pre-generated tokens or GitHub Apps
- Consider using GitHub Actions secrets for automated workflows

#### Network/Firewall Issues
- Ensure access to `github.com` and `api.github.com`
- Check corporate firewall settings
- Verify proxy configuration if applicable

## Security Best Practices

### Token Storage

**✅ Do:**
- Store tokens in `.env` files (excluded from version control)
- Use environment variables in production
- Set appropriate token expiration dates
- Use fine-grained PATs when possible

**❌ Don't:**
- Commit tokens to version control
- Share tokens via insecure channels
- Use overly broad token scopes
- Store tokens in plain text files

### Token Scopes

**Minimum required scopes for Copilot development:**
- `repo` - Repository access (required for private repos and codesearch)

**Additional scopes for extended functionality:**
- `read:packages` - Package registry access
- `user:email` - User identification
- `read:org` - Organization access (if needed)

### Token Rotation

- **Regular rotation**: Update tokens every 90 days
- **Immediate rotation**: If token is compromised
- **Automated rotation**: Use GitHub Apps for automatic token refresh

### Environment Security

```bash
# Ensure .env is in .gitignore
echo ".env" >> .gitignore

# Set proper file permissions
chmod 600 .env

# Use environment variables in production
export GITHUB_OAUTH_TOKEN="your_token_here"
```

## Recent Updates (2025)

### New Features
- **Model Context Protocol (MCP)** support in VS Code
- **Agent mode** for autonomous coding assistance
- **Fine-grained PATs** for better security
- **OAuth improvements** for smoother authentication

### Deprecated Features
- Some older OAuth endpoints (use current endpoints shown above)
- Legacy authentication methods (migrate to OAuth 2.0)

### API Changes
- Enhanced Copilot API endpoints
- Improved rate limiting
- Better error responses

## Additional Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [GitHub OAuth Documentation](https://docs.github.com/en/developers/apps/building-oauth-apps)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [VS Code Copilot Extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
- [Contributing Guidelines](./CONTRIBUTING.md)

## Getting Help

If you encounter issues:

1. **Check this guide** for common solutions
2. **Review logs** in your development console
3. **Test your token** using the debug commands above
4. **Check GitHub Status** at [githubstatus.com](https://www.githubstatus.com/)
5. **Open an issue** in this repository with detailed error information

---

*Last updated: January 2025*
*For the most current information, always refer to the official GitHub documentation.*