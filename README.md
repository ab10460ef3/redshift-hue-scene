# redshift-hue-scene
Script to dim and adjust color temperature of Phillips Hue scenes based on sun elevation.

Based on [deuxpi's redshift-hue](https://github.com/deuxpi/redshift-hue) and 
utilizing a fork of [studioimaginaire's phue](https://github.com/studioimaginaire/phue), 
the script reads a current hue configuration from a hub, and applies a color shifted and or 
dimmed scene configuration based on the altitude of the sun.

# Important

- This software is in active development.
- USE AT YOUR OWN RISK! 
- It has been tested on 2nd and 3rd gen white ambiance and color bulbs.
- It has been NOT been tested on non-dimmible or white only bulbs, or a first gen hub.

# Known Issues

- Scenes activated by a motion sensor may flicker one time when activated. 
I presume this is caused by lights getting their initial state from
 memory instead of receiving it from the hub. Attempting to resolve with delays or ddx in 1.13.

# Requirements & Dependancies

A Hue Bridge running version **1.11+** is **required**

Targeted for python 3.4, not tested in 2.7

Depends on pysolar==0.7 and custom phue (included) 

# Configuration

Location and hub address, as well as color temperatures and dimness is configured by global variables.

```python
TEMP_DAY           = 3500
TEMP_NIGHT         = 2300
BRIGHTNESS         = 1.0
BRIGHTNESS_DAY     = 1.0
BRIGHTNESS_EVENING = 0.8
BRIGHTNESS_NIGHT   = 0.15
TRANSITION_TIME    = 100  # deciseconds
SLEEP_TIME         = 120  # seconds
LAT                =  40.7128  # North of the Equaitor is positive 
LON                = -74.0059  # East of Greenwich is positive 
BRIDGE_ADDRESS     = '192.168.1.102'

SHIFT_ALL_LIGHTS   = True
TWEAK_MOTION_DIM   = True
```

# Scene Configuration

Configuration of scenes and bulb temperature is done with
naming conventions using the scene or bulb names in the hub. This is most easily done with the app
 or your preferred method of configuration. 

- Scenes with "nightshift" or "dayshift" in the name (case-insensitive) will be updated by the script
- "nightshift" applies `BRIGHTNESS_NIGHT` settings, "dayshift" applies the `BRIGHTNESS_EVENING`.
 They are intended as replacements for 'Nightlight' and 'Dimmed' scenes respectively,
  but with temperature shifting.
- Scenes are actually room specific, so if you have 4 sensors in 4 rooms, you'll need 8 scenes.
 
<img src="https://github.com/ab10460ef3/redshift-hue-scene/blob/master/doc/scene_creation.png?raw=true" width="200">

This approach allows you to configure your lights in the 
  way you do now, instead of logging into a raspberry pi and using vi on a config file when you 
  want to add a light or adjust times.
  
# Unimplemented features 

- Bulbs named "ct<+/-number>" i.e. ct+50 will be shifted on the mired scale (+/-) by given number
- ~~Add condition comparing previous iteration to reduce chattyness~~
- ~~default transistiontime delay.~~
- debian service files

