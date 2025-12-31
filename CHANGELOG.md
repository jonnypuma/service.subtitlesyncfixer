# Changelog

## Version 1.1.1
- Fixed: removed provides line in addon.xml to prevent addon from appearing in Program addons and Services addons categories

##Version 1.1.0
- Fixed: Only applies subtitle fix to video playback, not audio/music
- Added: Icon and fanart support for addon display
- Improved: Better detection of video vs audio playback using isPlayingVideo()

##Version 1.0.0
- Initial release
- Waits 5 seconds after playback starts, then seeks back 1 second to fix subtitles
- Only triggers when playback starts near the beginning (first 2 seconds)
- Minimal interruption - only 1 second rewind instead of 5 seconds
- Silent background operation with logging support

