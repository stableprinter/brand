# Branding Repository

This repository stores corporate identity and configuration files for multi-client application builds. It provides a centralized location for managing branding assets, app configurations, and build settings across different company clients.

## Purpose

This repository serves as the single source of truth for:
- **Corporate Identity**: Logos, colors, fonts, and visual branding elements
- **App Configuration**: Bundle IDs, API endpoints, app store information
- **Build Configuration**: Signing keys, certificates, and build settings

## Repository Structure

```
brand/
├── README.md
├── staging.json          # Staging environment configuration
├── production.json       # Production environment configuration
└── asset/
    ├── staging/          # Staging environment assets
    │   ├── appicon/      # App icons (iOS & Android)
    │   ├── fonts/        # Custom fonts
    │   └── splashscreen/ # Splash screen assets
    └── production/       # Production environment assets
        ├── appicon/      # App icons (iOS & Android)
        ├── fonts/        # Custom fonts
        └── splashscreen/ # Splash screen assets
```

## Configuration Files

### JSON Configuration Structure

Each JSON file (`staging.json`, `production.json`) contains:

- **identifiers**: Bundle IDs, domains, and deep link schemes
- **api**: API endpoints, WebSocket URLs, CDN configurations
- **branding**: App name, company name, colors, logos, support information
- **stores**: App Store and Play Store identifiers
- **signingKeys**: iOS and Android signing credentials and certificates

## Adding a New Company/Client App

To add a new company client application, follow this strategy:

### Step 1: Create a New Branch

Create a new branch named after the company/client:

```bash
git checkout -b <company-name>
```

Example:
```bash
git checkout -b acme-corp
```

### Step 2: Update Configuration Files

1. **Rename or create JSON files** to match the company's naming convention:
   - `staging.json` → `<company-name>-staging.json` (or keep as `staging.json` if branch-specific)
   - `production.json` → `<company-name>-production.json` (or keep as `production.json` if branch-specific)

2. **Update the JSON content** with company-specific values:
   - Bundle IDs
   - App names and company names
   - Brand colors
   - API endpoints
   - Signing key credentials
   - App store identifiers

### Step 3: Add Company Assets

Place company-specific assets in the appropriate directories:

- **App Icons**: `asset/<environment>/appicon/`
  - iOS: `Assets.xcassets/AppIcon.appiconset/`
  - Android: `android/mipmap-*/`
  - Store icons: `appstore.png`, `playstore.png`

- **Fonts**: `asset/<environment>/fonts/`

- **Splash Screens**: `asset/<environment>/splashscreen/`

### Step 4: Commit and Push

```bash
git add .
git commit -m "Add branding configuration for <company-name>"
git push origin <company-name>
```

## Jenkins Integration

The Jenkins build pipeline uses this repository to build client-specific applications:

1. **Branch Selection**: Jenkins checks out the branch corresponding to the company/client
2. **Configuration Loading**: The build process reads the JSON configuration files from the branch
3. **Asset Integration**: Assets from the `asset/` directory are integrated into the app build
4. **App Building**: The app is built with the company-specific configuration and branding

### Jenkins Build Process

When Jenkins builds a new app:

1. Checks out the repository branch matching the company name
2. **Performs health checks**: Validates all required fields in JSON files and verifies all asset files exist
3. Reads the JSON configuration file (staging.json or production.json)
4. Copies assets from `asset/<environment>/` to the app project
5. Applies configuration values (bundle IDs, colors, API endpoints, etc.)
6. Uses signing keys referenced in the configuration
7. Builds and packages the app with the company's branding

**Note**: If health checks fail (missing fields or files), Jenkins will automatically ping the repository owner and halt the build process.

## Best Practices

- **Branch Naming**: Use clear, consistent naming (e.g., `acme-corp`, `tech-solutions-inc`)
- **Asset Organization**: Keep assets organized by environment (staging/production)
- **Complete Configuration**: All fields in JSON files must be populated - there are no optional fields
- **Complete Assets**: Ensure all required asset files are present in the appropriate directories
- **Version Control**: Commit all assets and configurations to the repository
- **Documentation**: Update this README if adding new configuration fields or changing the structure

## Health Checks & Validation

Jenkins automatically performs health checks on the repository:

- **Configuration Validation**: Jenkins validates that all required fields are present in JSON configuration files
- **File Existence Checks**: Jenkins verifies that all referenced asset files exist in the expected locations
- **Automatic Notifications**: If any field is missing or any file is missing, Jenkins will:
  - Automatically detect the issue during the health check
  - Ping/notify the repository owner or branch maintainer
  - Prevent the build from proceeding until issues are resolved

**Important**: All configuration fields and asset files are required. Missing fields or files will cause build failures and trigger owner notifications.

## Notes

- Each branch represents a separate company/client configuration
- Assets and JSON files are environment-specific (staging/production)
- Jenkins handles the actual app building process using these configurations
- Signing keys are referenced by credential IDs (managed in Jenkins)
- Jenkins performs automatic health checks and will notify owners of any missing fields or files
