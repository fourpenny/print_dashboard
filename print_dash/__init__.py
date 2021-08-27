# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import sqlite3
import flask

class printStatsDB:
    def __init__(self, plugin):
        self.name = plugins._settings.settings.getBaseFolder("logs") + "stats.db"

    #TODO: Implement function below within OctoPrint instead of the OS?
    #Using OS library causes plugin to not work for some reason...
    #Use DROP TABLE to clear table data instead :)
    def delete_database(self):
        return "Database deleted :)"

    #def connect(self):
    #    conn = None
    #    try:
    #        conn = sqlite3.connect(self.name)
    #        return conn
    #    except Error as e:
    #        print(e)
    #    return conn

class Print_dashPlugin(
                        octoprint.plugin.TemplatePlugin,
                        octoprint.plugin.AssetPlugin,
                        octoprint.plugin.StartupPlugin,
                        octoprint.plugin.SettingsPlugin,
                        octoprint.plugin.EventHandlerPlugin,
                        octoprint.plugin.SimpleApiPlugin):

        def get_assets(self):
            return dict(
                js=["js/print_dash.js"],
                css=["css/print_dash.css"]
            )

        def on_after_startup(self):
            self.database = printStatsDB(self)

#------------------------------------------------------------------------------#
# Event Handling                                                               #
#------------------------------------------------------------------------------#

        def on_event(self, event, payload):
            self._logger.info(event)
            self._logger.info(payload)
            #list of events to use: PrintStarted, PrintFailed, PrintDone, PrintCancelled,
            #FileAdded, FileSelected
            if event == "PrintStarted":
                self._logger.info("Success!")
            return

#------------------------------------------------------------------------------#
# SimpleApiPlugin implementation                                               #
#------------------------------------------------------------------------------#

        def get_api_commands(self):
            return dict(
                clear_db=[]
            )

        def on_api_command(self, command, data):
            if command == "clear_db":
                #Need to implement function below
                self._logger.info(self.database.delete_database())

        def on_api_get(self,request):
            data = request.args.get('data')
            if (data == "successful_prints"):
                return flask.jsonify(dict(message='hello'))
            else:
                return flask.jsonify(dict(message='goodbye'))

        def is_api_adminonly(self):
            return False

# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "print_dash"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
#__plugin_pythoncompat__ = ">=3,<4" # only python 3
#__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

__plugin_name__ = "Print Dashboard"
__plugin_version__ = "0.0.1"
__plugin_description__ = "A quick \"Hello World\" example plugin for OctoPrint"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = Print_dashPlugin()
