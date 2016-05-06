from uwaterlooapi import UWaterlooAPI
import pprint
uw = UWaterlooAPI(api_key="8ab9363c27cf84a3fdf526a89269e81a")

pprint.pprint(uw.course_schedule("CS", "136")[0]['classes'], width=20)