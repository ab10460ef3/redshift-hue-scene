'''

https://github.com/deuxpi/redshift-hue/blob/master/LICENSE

The MIT License (MIT)

Copyright (c) 2015 Philippe Gauthier

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import datetime
import logging
import time
from time import sleep

from phue import Bridge
from pysolar.solar import *

log_format = '%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
logging.basicConfig(format=log_format, level=logging.INFO)
log = logging.getLogger('redshift-hue')

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

lat = config_defaults['lat']
lon = config_defaults['lon']

log.debug(
    'Location: %.2f %s, %.2f %s',
    abs(lat), 'SN'[lat >= 0.], abs(lon), 'WE'[lon >= 0.])

temperature_day = config_defaults['temp-day']
temperature_night = config_defaults['temp-night']
log.debug(
    'Temperatures: %dK at day, %dK at night',
    temperature_day, temperature_night)

transition_low = -6.0
transition_high = 3.0
log.debug(
    'Solar elevations: day above %.1f, night below %.1f',
    transition_high, transition_low)

brightness = config_defaults['brightness']
try:
    brightness_day = config_defaults['brightness-day']
except KeyError:
    brightness_day = brightness
try:
    brightness_night = config_defaults['brightness-night']
except KeyError:
    brightness_night = brightness

bridge_address = config_defaults['hue-address']

# TODO poll capibilities of lights from the hub
#dimmable_lights = map(int, config.get('hue', 'dimmable-lights').split(','))
#color_lights = map(int, config.get('hue', 'color-lights').split(','))

bridge = Bridge(bridge_address)
bridge.connect()


def get_alpha(elevation):
    alpha = (transition_low - elevation) / (transition_low - transition_high)
    return min(max(0.0, alpha), 1.0)


def get_period(elevation):
    if elevation < transition_low:
        return 'Night'
    elif elevation < transition_high:
        return 'Transition'
    else:
        return 'Daytime'


def log_period(period, transition):
    if period == 'Transition':
        log.info('Period: %s (%.2f%% day)', period, transition * 100)
    else:
        log.info('Period: %s', period)


def get_transition_progress(elevation):
    period = get_period(elevation)
    return {
        'Night': 0.0,
        'Transition': get_alpha(elevation),
        'Daytime': 1.0,
    }[period]


def interpolate(elevation):
    alpha = get_alpha(elevation)
    temperature = (1.0 - alpha) * temperature_night + alpha * temperature_day
    brightness = (1.0 - alpha) * brightness_night + alpha * brightness_day
    return temperature, brightness


while True:
    now = datetime.datetime.now()
    elevation = get_altitude(lat, lon, now)
    log.debug('Solar elevation: %f', elevation)

    temperature, brightness = interpolate(elevation)
    transition = get_transition_progress(elevation)
    log_period(get_period(elevation), transition)
    log.info('Color temperature: %dK', temperature)
    log.info('Brightness: %.2f', brightness)

    mired = int(1000000. / temperature)


    #bridge.set_light(color_lights, 'ct', mired)

    #bridge.set_light(dimmable_lights, 'bri', int(brightness * 255))

    redshift_scenes =   { scene.name:scene for scene in bridge.scenes if 'redshift' in scene.name.lower()}
    for scene_object in redshift_scenes.values():
        print('updating scene: ' + scene_object.name)
        bridge.set_scene_lights(scene_object,{'ct':mired,'on':True,'bri':int(brightness * 255)})

    brightshift_scenes =   { scene.name:scene for scene in bridge.scenes if 'brightshift' in scene.name.lower()}
    for scene_object in brightshift_scenes.values():
        print('updating scene: ' + scene_object.name)
        bridge.set_scene_lights(scene_object,{'ct':mired,'on':True,'bri':int(1 * 255)})

    sleep(60.0)