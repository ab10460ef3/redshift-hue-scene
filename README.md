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

Location and hub address, as well as color temperatures and dimness is configured by variables in `config_defaults`.

```python
config_defaults = {
    'temp-day': 3500,
    'temp-night': 2000,
    'brightness': 1.0,
    'brightness-day': 1.0,
    'brightness-evening': 0.8,
    'brightness-night': 0.35,
    'lat':40.7128,
    'lon':-74.0059,
    'hue-address': '192.168.1.102'
}
```

# Scene Configuration

Configuration of scenes and bulb temperature is done with
naming conventions using the scene or bulb names in the hub. Probably done using the hue app or something similar.

- Scenes with "nightshift" or "dayshift" in the name (case-insensitive) will be updated by the script
- "nightshift" applies `brightness-night` settings, "dayshift" applies the `brightness-evening`.
 They are intended as replacements for 'Nightlight' and 'Dimmed' scenes respectively,
  but with temperature shifting.

- Configure two scenes for each group you want to be color shifted as follows:

1. A scene for dimmed evening/morning mode with "dayshift" in the name i.e. "Kitchen dayshift"
2. A scene for nightlight mode with "nightshift" i.e. "Bathroom nighshift"

 
<img src="https://github.com/ab10460ef3/redshift-hue-scene/blob/master/doc/scene_creation.png?raw=true" width="200">

# Unimplemented features 

- Bulbs named "ct<+/-number>" i.e. ct+1000 will be shifted on the mired scale (+/-) by given number
- Add condition comparing previous iteration to reduce chattyness.
- default transistiontime delay.
- debian service files

# Limitations

- Utilizing `/api/.../scene/x/lights` as treated in version 1.11 of the hue API was not included in phue lib at the time of 
writing. The function `set_scene_lights()` fills was added, but in such away as to be general enough 
for inclusion in the main phue project. Although it would be a lot easier to include logic specific to this 
side project in the function, it would no longer be a general function. 