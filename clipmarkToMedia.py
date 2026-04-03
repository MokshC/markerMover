#!/usr/bin/env python

# Created by: Moksh Chitkara
# Last Update: April 3rd 2026
# v1.0.0
# Copyright (C) 2026  Moksh Chitkara
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import datetime

# Global Variables
projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()
################################################################################################
# Window creation #
###################
def main_ui():
	# vertical group
	window = [ui.VGroup({"Spacing": 10,},[
				# Track Select
				ui.HGroup({ 'Weight': 0 }, [
					ui.Label({ 'Text': "Move markers on track: " }),
					ui.LineEdit({ 'ID': "track_edit", "PlaceholderText": "Leave empty for all tracks"}),
				]),
				# Move button
				ui.HGap(),
				ui.Button({"ID": "Button", "Text": "Move Markers!!", "Weight": 1, 'AlignHCenter': True}),
				]), 
			]
	return window

ui = fu.UIManager # get UI utility from fusion
disp = bmd.UIDispatcher(ui) # gets display settings?

# window definition
window = disp.AddWindow({"WindowTitle": "Clip Markers to Mediapool",
			"ID": "CMTMPWin", 
			'WindowFlags': {'Window': True,'WindowStaysOnTopHint': True},
			"Geometry": [1500,500,330,120], # x-position, y-position, width, height
			}, 
			main_ui())

itm = window.GetItems() # Grabs all UI elements to be manipulated
################################################################################################
# Functions #
#############

def log(info, level = 1):

	if level == 1:
		level = "INFO"
	elif level == 2:
		level = "WARN"
	else:
		level = "EROR"
	
	time = datetime.datetime.now()
	
	fullLog = [str(time), level, info]
	print(" | ".join(fullLog))	


# Applies markers from clip to media
# input: item [timeline clip item]
# output: None
def moveMarker(item):
	
	markers = item.GetMarkers()
	media = item.GetMediaPoolItem()
	
	if markers and media.GetName():
		for key in markers:
			frameId = key
			color = markers[key]["color"]
			name = markers[key]["name"]
			note = markers[key]["note"]
			duration = markers[key]["duration"]
			
			if media.AddMarker(frameId, color, name, note, duration):
				log(str(frameId) + " added to " + str(media.GetName()))
			else:
				log(str(frameId) + " failed to add on " + str(media.GetName()), 3)

def _main(ev):

	itm['Button'].Enabled = False
	itm['Button'].Text = "Starting..."
	
	timeline = project.GetCurrentTimeline()

	# do a single track or all tracks
	try:
		dest_track = int(itm["track_edit"].Text)
		track_range = range(dest_track, dest_track + 1)
	except:
		log("Running on all tracks", 2)
		track_range = reversed(range(1, timeline.GetTrackCount("video")+1))
	
	for track in track_range:
		if timeline.GetIsTrackEnabled("video",track):
			log("Starting track " + str(track), 1)
			track_items = timeline.GetItemListInTrack("video",track)
			prog = 0
			total = len(track_items)
			
			for item in track_items:
				prog += 1
				loading = "{:.2%}".format(float(prog)/float(total))
				itm['Button'].Text = "Moving on Track {}: {}".format(track, loading)
				
				moveMarker(item)
				
		
	itm['Button'].Text = "Disable!!"
	itm['Button'].Enabled = True
# needed to close window
def _close(ev):
	disp.ExitLoop()

################################################################################################
# GUI Elements #
# manipulations

# button presses
window.On.Button.Clicked = _main
window.On.CMTMPWin.Close = _close
window.Show()
disp.RunLoop()
window.Hide()
#################################################################################################
