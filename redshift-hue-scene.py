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
log = logging.getLogger('redshift-hue-scene')

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

log.debug(
    'Location: %.2f %s, %.2f %s',
    abs(LAT), 'SN'[LAT >= 0.], abs(LON), 'WE'[LON >= 0.])


log.debug(
    'Temperatures: %dK at day, %dK at night',
    TEMP_DAY, TEMP_NIGHT)

transition_low = -6.0
transition_high = 3.0
log.debug(
    'Solar elevations: day above %.1f, night below %.1f',
    transition_high, transition_low)


# TODO poll capibilities of lights from the hub
#dimmable_lights = map(int, config.get('hue', 'dimmable-lights').split(','))
#color_lights = map(int, config.get('hue', 'color-lights').split(','))

bridge = Bridge(BRIDGE_ADDRESS)
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


def interpolate_temperatue(elevation, temperature_night, temperature_day):
    alpha = get_alpha(elevation)
    temperature = (1.0 - alpha) * temperature_night + alpha * temperature_day
    return temperature

def interpolate_brightness(elevation, brightness_night, brightness_day):
    alpha = get_alpha(elevation)
    brightness = (1.0 - alpha) * brightness_night + alpha * brightness_day
    return brightness

shift_skew_map = { l.light_id : l.name.split("ct")[1] for l in bridge.lights if ("ct+" or "ct-")  in l.name.split("ct") }

last_period = None

while True:

    now = datetime.datetime.now()
    elevation = get_altitude(LAT, LON, now)
    log.debug('Solar elevation: %f', elevation)

    temperature        = interpolate_temperatue(elevation, TEMP_NIGHT, TEMP_DAY)
    brightness         = interpolate_brightness(elevation, BRIGHTNESS_NIGHT, BRIGHTNESS_DAY )
    evening_brightness   = interpolate_brightness(elevation, BRIGHTNESS_EVENING, BRIGHTNESS_DAY )

    transition = get_transition_progress(elevation)
    period = get_period(elevation)
    log_period(get_period(elevation), transition)
    log.info('Color temperature: %dK', temperature)
    log.info('Dimmed Brightness: %.2f', evening_brightness)
    log.info('Nightlight Brightness: %.2f', brightness)

    mired = int(1000000. / temperature)


    #bridge.set_light(color_lights, 'ct', mired)
    #bridge.set_light(dimmable_lights, 'bri', int(brightness * 255))

    # Only change if transitioning or just changed to/from transitioning.
    if period != last_period or period == 'Transition':

        # Update dimshift scenes
        dayshift_scenes =   { scene.name : scene for scene in bridge.scenes if 'dayshift' in scene.name.lower()}

        for scene_object in dayshift_scenes.values():
            log.info('updating daylight scene: %s' % scene_object.name)
            bridge.set_scene_lights(scene_object,{'ct':mired,
                                                  'on':True,
                                                  'transitiontime':TRANSITION_TIME,
                                                  'bri':int(evening_brightness * 255)})


        # Update nightlight shift dimming scenes

        nightshift_scenes =   { scene.name : scene for scene in bridge.scenes if 'nightshift' in scene.name.lower()}

        for scene_object in nightshift_scenes.values():
            log.info('updating lightlight scenes: %s' % scene_object.name)
            bridge.set_scene_lights(scene_object,{'ct':mired,
                                                  'on':True,
                                                  'transitiontime':TRANSITION_TIME,
                                                  'bri':int(brightness * 255)})


        # Update just the temperature of lights that are on
        if SHIFT_ALL_LIGHTS:
            active_lights = { light.light_id : light for light in bridge.lights if light.on }
            bridge.set_light(active_lights.keys(), {'ct':mired} , transitiontime=TRANSITION_TIME)

        if TWEAK_MOTION_DIM:
            motion_dim = [ r for r in  bridge.rules if (".dim" in r.name and "MotionSensor" in r.name)]
            for m in motion_dim:
                dim_actions = [ k for k,a in enumerate(m.actions) if  'bri_inc' in a['body'].keys() ]
                for k in dim_actions:
                    m.actions[k]['body']['transitiontime'] = TRANSITION_TIME
                bridge.set_rule(m.rule_id, {'actions':m.actions})

        last_period = period

    sleep(SLEEP_TIME)
