# -*- coding: utf-8 -*-
"""
Subtitle Sync Fixer Service Add-on for Kodi
Automatically seeks back 1 second after 5 seconds of playback to fix subtitle display issues
"""

import xbmc
import xbmcaddon

# Get addon info
ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_NAME = ADDON.getAddonInfo('name')

# Configuration
WAIT_TIME = 5.0  # Wait 5 seconds before seeking back
SEEK_BACK = 1.0  # Seek back 1 second (enough to trigger resync)


class SubtitleFixPlayer(xbmc.Player):
    """Player class that listens for playback events and fixes subtitle sync"""
    
    def __init__(self):
        xbmc.Player.__init__(self)
        self._fix_applied = False
        self._playback_started = False
        xbmc.log(f"{ADDON_NAME}: Service initialized", xbmc.LOGINFO)
    
    def onPlayBackStarted(self):
        """Called when playback begins"""
        try:
            # Check if add-on is enabled
            if not ADDON.getSettingBool('enabled'):
                return
            
            current_time = self.getTime()
            
            # Only apply fix if we're at the very beginning (first 2 seconds)
            # This prevents the fix from triggering on every seek/resume
            if current_time < 2.0:
                self._fix_applied = False
                self._playback_started = True
                xbmc.log(f"{ADDON_NAME}: Playback started at {current_time:.2f}s, will apply subtitle fix after {WAIT_TIME}s", xbmc.LOGINFO)
            else:
                # If playback started mid-way, don't apply fix
                self._playback_started = False
                self._fix_applied = True
        except Exception as e:
            xbmc.log(f"{ADDON_NAME}: Error in onPlayBackStarted: {str(e)}", xbmc.LOGERROR)
    
    def onPlayBackStopped(self):
        """Called when playback stops"""
        self._playback_started = False
        self._fix_applied = False
        xbmc.log(f"{ADDON_NAME}: Playback stopped", xbmc.LOGDEBUG)
    
    def onPlayBackEnded(self):
        """Called when playback ends"""
        self._playback_started = False
        self._fix_applied = False
        xbmc.log(f"{ADDON_NAME}: Playback ended", xbmc.LOGDEBUG)
    
    def check_and_apply_fix(self):
        """Check if we need to apply the subtitle fix"""
        # Check if add-on is enabled
        if not ADDON.getSettingBool('enabled'):
            return
        
        if not self._playback_started or self._fix_applied:
            return
        
        try:
            if self.isPlaying():
                current_time = self.getTime()
                
                # If we've reached the wait time, apply the fix
                if current_time >= WAIT_TIME:
                    xbmc.log(f"{ADDON_NAME}: Playback reached {current_time:.2f}s, seeking back {SEEK_BACK}s to trigger subtitle re-sync", xbmc.LOGINFO)
                    
                    # Get current time and seek back 1 second
                    seek_to = current_time - SEEK_BACK
                    if seek_to >= 0:
                        self.seekTime(seek_to)
                        self._fix_applied = True
                        xbmc.log(f"{ADDON_NAME}: Successfully sought back to {seek_to:.2f}s", xbmc.LOGINFO)
                    else:
                        # If we can't seek back enough, just use StepBack
                        xbmc.executebuiltin('PlayerControl(StepBack)')
                        self._fix_applied = True
                        xbmc.log(f"{ADDON_NAME}: Used StepBack to trigger subtitle re-sync", xbmc.LOGINFO)
        except Exception as e:
            xbmc.log(f"{ADDON_NAME}: Error in check_and_apply_fix: {str(e)}", xbmc.LOGERROR)


def main():
    """Main service loop"""
    xbmc.log(f"{ADDON_NAME}: Service starting...", xbmc.LOGINFO)
    
    # Initialize the player event listener
    player = SubtitleFixPlayer()
    
    # Keep the service running in the background
    monitor = xbmc.Monitor()
    
    try:
        while not monitor.abortRequested():
            # Check if we need to apply the subtitle fix
            player.check_and_apply_fix()
            
            # Sleep for 100ms and check if we should exit
            if monitor.waitForAbort(0.1):
                break
    except KeyboardInterrupt:
        pass
    finally:
        xbmc.log(f"{ADDON_NAME}: Service stopped", xbmc.LOGINFO)


if __name__ == '__main__':
    main()

