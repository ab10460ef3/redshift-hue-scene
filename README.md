# redshift-hue-scene
Script to dim and adjust color temperature of Phillips Hue scenes based on sun elevation.

Based on [deuxpi's redshift-hue](https://github.com/deuxpi/redshift-hue) and 
utilizing a fork of [studioimaginaire's phue](https://github.com/studioimaginaire/phue), 
the script reads a current hue configuration from a hub, and applies a color shifted and or 
dimmed scene configuration based on the altitude of the sun.

## This software is in active development. USE AT YOUR OWN RISK! 

## Lights must have a brightness appled to turn on.

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
    'brightness-night': 0.35,
    'lat':40.7128,
    'lon':-74.0059,
    'hue-address': '192.168.1.102'
}
```

- Scenes with "redshift" or "brightshift" in the name (case-insensitive) will be updated by the script
- "Redshift" dims, brightshift does not.

# Unimplemented features 

- Bulbs named "ct<+/-><number>" i.e. ct+1000 will be shifted on the mired scale (+/-) by given number
