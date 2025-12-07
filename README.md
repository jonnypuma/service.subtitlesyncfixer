# Subtitle Sync Fixer - Kodi Service Add-on

## Description

This service add-on automatically fixes subtitle display issues in Kodi by waiting 5 seconds after playback starts, then seeking back 1 second to trigger subtitle re-synchronization. This resolves the common problem where embedded subtitles don't appear until manually seeking backward.

## Problem

When playing movies in Kodi, subtitles (especially embedded ones in MKV files) sometimes don't display at the start of playback. The workaround is to manually skip backward 5 seconds, which forces Kodi to re-sync the subtitle stream. This add-on automates that process.

## Solution

The add-on runs silently in the background and listens for playback start events. When a video begins playing, it automatically:
1. Detects when playback starts near the beginning (first 2 seconds)
2. Waits for playback to reach 5 seconds
3. Seeks back 1 second to trigger subtitle re-sync (minimal interruption)
4. Only activates once per playback session to avoid interfering with normal seeking

## Installation

### Method 1: Install from ZIP (Recommended)

1. Create a ZIP file of the entire `service.subtitlesyncfixer` folder
3. In Kodi, go to **Settings** → **Add-ons** → **Install from zip file**
4. Navigate to and select the ZIP file
5. The add-on will be installed and start automatically

### Method 2: Manual Installation

1. Copy the `service.subtitlesyncfixer` folder to your Kodi add-ons directory:
   - **Windows**: `%APPDATA%\Kodi\addons\`
   - **Linux**: `~/.kodi/addons/`
   - **macOS**: `~/Library/Application Support/Kodi/addons/`
   - **Android**: `/sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons/`
2. Restart Kodi or enable the add-on from **Settings** → **Add-ons** → **My add-ons** → **Services**

## Usage

Once installed, the add-on runs automatically in the background. If you chose to copy folder directly into the addons folder instead of installing as a zip, you may have to enable the addon first inside the addon settings in Kodi. 

By default, it is enabled. You can enable or disable it by:

1. Go to **Settings** → **Add-ons** → **My add-ons** → **Services**
2. Select **Subtitle Sync Fixer**
3. Click **Configure** to open settings
4. Toggle **Enable subtitle sync fix** on or off

When enabled, the add-on will:
- Activate whenever video playback starts
- Only trigger when playback begins near the start (first 2 seconds)
- Work silently without any user interaction

## Requirements

- Kodi 19 (Matrix) or later (Python 3.x)
- No additional dependencies required

## How It Works

The add-on uses Kodi's `xbmc.Player()` class to listen for playback events. When `onPlayBackStarted()` is triggered:
1. It checks if playback is near the beginning (first 2 seconds)
2. Monitors playback time in the background
3. When playback reaches 5 seconds, it seeks back 1 second using `seekTime()`
4. This minimal seek forces Kodi to re-synchronize all streams, including subtitles, without significant interruption

## Troubleshooting

- **Subtitles still not appearing**: Make sure subtitles are enabled in Kodi's player settings
- **Add-on not working**: Check Kodi's log file for error messages (usually in `kodi.log`)
- **Too aggressive**: The add-on only triggers in the first 2 seconds of playback to avoid interfering with normal use

## Logging

The add-on logs its activity to Kodi's log file. To view logs:
- Enable debug logging in Kodi: **Settings** → **System Settings** → **Logging** → Enable debug logging
- Look for entries prefixed with `Subtitle Sync Fixer`

## License

MIT License - Feel free to modify and distribute

## Credits

Created to solve the common Kodi subtitle display issue where embedded subtitles don't appear at playback start.

