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
├── staging.json              # Staging environment configuration
├── production.json           # Production environment configuration
└── asset/
    ├── staging/              # Staging environment assets
    │   ├── appicon/
    │   │   ├── android/
    │   │   │   ├── mipmap-hdpi/     # ic_launcher.png
    │   │   │   ├── mipmap-mdpi/
    │   │   │   ├── mipmap-xhdpi/
    │   │   │   ├── mipmap-xxhdpi/
    │   │   │   └── mipmap-xxxhdpi/
    │   │   ├── Assets.xcassets/
    │   │   │   └── AppIcon.appiconset/   # iOS app icons
    │   │   ├── appstore.png              # App Store icon (1024×1024)
    │   │   └── playstore.png             # Play Store icon (512×512)
    │   ├── fonts/
    │   └── splashscreen/
    │       └── splashscreen.png
    └── production/           # Production environment assets
        ├── appicon/
        │   ├── android/
        │   │   ├── mipmap-hdpi/
        │   │   ├── mipmap-mdpi/
        │   │   ├── mipmap-xhdpi/
        │   │   ├── mipmap-xxhdpi/
        │   │   └── mipmap-xxxhdpi/
        │   ├── Assets.xcassets/
        │   │   └── AppIcon.appiconset/
        │   ├── appstore.png
        │   └── playstore.png
        ├── fonts/
        └── splashscreen/
            └── splashscreen.png
```

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

1. **Edit or create JSON configuration files** to use company-specific values:
   - Use or modify `staging.json` and `production.json` with details unique to the company.

2. **Update the JSON content** with company-specific values:
   - Bundle IDs
   - App names and company names
   - Brand colors
   - API endpoints
   - Signing key credentials
   - App store identifiers

### Step 3: Add Company Assets

Place company-specific assets in the appropriate directories under `asset/<environment>/`:

- **App Icons** (`asset/<environment>/appicon/`):
  - **iOS**: `Assets.xcassets/AppIcon.appiconset/` — include all required sizes (29, 40, 57, 58, 60, 80, 87, 1024, etc.)
  - **Android**: `android/mipmap-*/` — `ic_launcher.png` in each density folder (mdpi, hdpi, xhdpi, xxhdpi, xxxhdpi)
  - **Store icons**: `appstore.png` (1024×1024), `playstore.png` (512×512)

- **Fonts**: `asset/<environment>/fonts/` — TTF/OTF font files

- **Splash Screens**: `asset/<environment>/splashscreen/splashscreen.png`


## Jenkins Integration

The Jenkins build pipeline uses this repository to build client-specific applications:

1. **Branch Selection**: Jenkins checks out the branch corresponding to the company/client
2. **Configuration Loading**: The build process reads the JSON configuration files from the branch
3. **Asset Integration**: Assets from the `asset/` directory are integrated into the app build
4. **App Building**: The app is built with the company-specific configuration and branding

### Jenkins Build Process

When Jenkins builds a new app:

1. Checks out the repository branch matching the company name
2. Reads the JSON configuration file (staging.json or production.json)
3. Copies assets from `asset/<environment>/` to the app project
4. Applies configuration values (bundle IDs, colors, API endpoints, etc.)
5. Uses signing keys referenced in the configuration
6. Builds and packages the app with the company's branding



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
