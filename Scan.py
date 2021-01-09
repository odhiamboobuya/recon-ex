from datetime import datetime
from db_connection import create_connection, select_project_id, create_scan_result


def get_project_id(project_name):
    conn = create_connection()
    with conn:
        project_id = select_project_id(conn, project_name)
    return project_id


class Scan:

    def __init__(self, project_object):
        self.date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        self.project_id = get_project_id(project_object.name)
        self.assets = project_object.assets
        self.scan_id = None

    def save_scan(self):
        conn = create_connection()
        scan = (self.project_id, self.date, self.assets)
        with conn:
            self.scan_id = create_scan_result(conn, scan)
