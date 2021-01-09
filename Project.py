"""
this class has the project's nameT
"""
from db_connection import create_connection, create_project


class Project:

    def __init__(self, name=""):
        self.name = name
        self.assets = []

    def set_assets(self, assets):
        self.assets = assets

    def save_project(self):
        conn = create_connection()
        project = (self.name, self.assets)
        with conn:
            create_project(conn, project)



