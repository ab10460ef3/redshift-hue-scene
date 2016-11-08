# redshift-hue-scene
Script to dim and adjust color temperature of Phillips Hue scenes based on sun elevation.

Based on [deuxpi's redshift-hue](https://github.com/deuxpi/redshift-hue) and 
utilizing a fork of [studioimaginaire's phue](https://github.com/studioimaginaire/phue), 
the script reads a current hue configuration from a hub, and applies a color shifted and or 
dimmed scene configuration based on the altitude of the sun.


# Requirements & Dependancies

Targeted for python 3.4, not tested in 2.7

Depends on pysolar and custom phue libraries

# Configuration

Color temperatures and dimness is configured with variables.

Configuration of scenes and bulb temperature is done with
naming conventions using the scene or bulb names in the hub.

- Scenes with "redshift" in the name (case-insensitive) will be updated by the script
- Bulbs with "ct+<number>" i.e. ct+1000 will be skewed in the direction sign (+/-) by given number
