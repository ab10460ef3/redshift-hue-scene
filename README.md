# redshift-hue-scene
Script to dim and adjust color temperature of Phillips Hue scenes based on sun elevation.

Based on [deuxpi's redshift-hue](https://github.com/deuxpi/redshift-hue) and 
utilizing a fork of [studioimaginaire's phue](https://github.com/studioimaginaire/phue), 
the script reads a current hue configuration from a hub, and applies a color shifted and or 
dimmed scene configuration based on the altitude of the sun.

## This software is in active development. USE AT YOUR OWN RISK! 

## Lights must have a brightness appled to turn on a light.

# Requirements & Dependancies

Targeted for python 3.4, not tested in 2.7

Depends on pysolar and custom phue libraries

# Configuration

Color temperatures and dimness is configured by variables in default config.

Configuration of scenes and bulb temperature is done with
naming conventions using the scene or bulb names in the hub.

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

- Configure two scenes for each group you want to be color shifted as follows:

1. A scene for dimmed evening/morning mode with "dayshift" in the name i.e. "Kitchen dayshift"
2. A scene for nightlight mode with "nightshift" i.e. "Bathroom nighshift"

 
<img src="https://github.com/ab10460ef3/redshift-hue-scene/blob/master/doc/scene_creation.png?raw=true" width="200">


- Scenes with "nightshift" or "dayshift" in the name (case-insensitive) will be updated by the script
- "nightshift" applies full nightlight like settings, "dayshift" applies the evening brightness.
 They are indended as replacemenst for 'Nightlight' and 'Dimmed' scenes respectively, but with temperature shifting.

# Unimplemented features 

- Bulbs named "ct<+/-number>" i.e. ct+1000 will be shifted on the mired scale (+/-) by given number
