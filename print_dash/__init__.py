# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import sqlite3
import flask

class printStatsDB:
    def __init__(self, folder):
        self.name = folder + "stats.db"
        #note, in the future should move connection object to individual functions
        #rather than DB object
        self.connection= self.connect()
        self.cursor = self.connection.cursor()
        self.tables = ['filaments','models','prints']

    def delete_database(self):
        cursor.executemany('''DROP TABLE (?)''', self.tables)

    def connect(self):

        conn = None
        try:
            conn = sqlite3.connect(self.name, check_same_thread=False)
            return conn
        except Error as e:
            print(e)
        return conn

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS filaments (
                        filament_id INTEGER PRIMARY KEY,
                        material TEXT,
                        brand TEXT,
                        purchase_date TEXT,
                        color TEXT
                        )'''
        )

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS models (
                        model_id INTEGER PRIMARY KEY,
                        file_name TEXT,
                        volume REAL,
                        base_area REAL,
                        skirt INTEGER,
                        raft INTEGER
                        )'''
        )
        cursor.execute('''CREATE TABLE IF NOT EXISTS prints (
                        print_id INTEGER PRIMARY KEY,
                        success INTEGER,
                        filament_id INTEGER,
                        model_id INTEGER,
                        nozzle_temp REAL,
                        bed_temp REAL,
                        print_date TEXT,
                        nozzle_size REAL,
                        FOREIGN KEY (filament_id)
                            REFERENCES filaments (filament_id),
                        FOREIGN KEY (model_id)
                            REFERENCES models (model_id)
                        )'''
        )

    def update_prints(self, payload):
        self.print_fp = payload['path']
        #check if a file with the same path is already in the database
        self.cursor.execute('''SELECT * FROM models WHERE file_name LIKE (?)''', (self.print_fp,))
        #if not, add it to the database
        if self.cursor.fetchone() == None:
            self.cursor.execute('''INSERT INTO models (file_name)
                                    VALUES (?)''', (self.print_fp,))
            self.connection.commit()

class Print_dashPlugin(
                        octoprint.plugin.TemplatePlugin,
                        octoprint.plugin.AssetPlugin,
                        octoprint.plugin.StartupPlugin,
                        octoprint.plugin.SettingsPlugin,
                        octoprint.plugin.EventHandlerPlugin,
                        octoprint.plugin.SimpleApiPlugin):

        def get_assets(self):
            return dict(
                js=["js/print_dash.js", "js/d3.min.js"],
                css=["css/print_dash.css"]
            )

        def on_after_startup(self):
            self.database = printStatsDB(self.get_plugin_data_folder())
            self.database.create_tables()

#------------------------------------------------------------------------------#
# Event Handling                                                               #
#------------------------------------------------------------------------------#

        def on_event(self, event, payload):
            #self._logger.info(event)
            #self._logger.info(payload)
            #list of events to use: PrintStarted, PrintFailed, PrintDone, PrintCancelled,
            #FileAdded, FileSelected
            if event == "PrintStarted":
                self._logger.info("Success")
                self.database.update_prints(payload)
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
