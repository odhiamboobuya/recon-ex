import sqlite3
from sqlite3 import Error

database_path = 'recon_ex.db'


def get_database_path():
    return database_path


def create_connection(database=get_database_path()):
    conn = None
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_all_tables():
    database = get_database_path()

    sqlite_create_project_table = """
    CREATE TABLE IF NOT EXISTS projects (
    id integer primary key,
    name text,
    assets text,
    UNIQUE(name));
    """

    sqlite_create_scans_table = """
    CREATE TABLE IF NOT EXISTS scans (
    id integer primary key,
    project_id integer not null,
    date text,
    assets text,
    FOREIGN KEY (project_id) REFERENCES projects (id) );
    """

    sqlite_create_assets_table = """
    CREATE  TABLE IF NOT EXISTS assets(
    id integer primary key,
    name text,
    subdomains text,
    scan_id text,
    FOREIGN KEY (scan_id) REFERENCES scans (id) );"""

    sqlite_create_subdomain_table = """
    CREATE TABLE IF NOT EXISTS subdomains (
    id integer primary key,
    url text,
    google_dorks text,
    webserver_id text,
    links text,
    asset_id text,
    FOREIGN KEY (asset_id) REFERENCES assets (id));"""

    sqlite_create_links_table = """
        CREATE TABLE IF NOT EXISTS links(
        id integer primary key,
        page_url text,
        tech_stack text,
        header text, 
        forms text,
        http_parameters text,
        hardcoded_strings text,
        screenshots text,
        backup_files text,
        outdated_js text,
        subdomain_id text,
        FOREIGN KEY (subdomain_id) REFERENCES subdomains (id));"""

    sqlite_create_form_table = """
        CREATE TABLE IF NOT EXISTS forms (
        id integer primary key,
        action text,
        parameters text,
        method text,
        link_id text,
        FOREIGN KEY (link_id) REFERENCES links (id) );
        """

    sqlite_create_webserver_table = """
        CREATE TABLE IF NOT EXISTS webservers (
        id integer primary key,
        name text,
        version text,
        operating_system text,
        subdomain_id text,
        FOREIGN KEY (subdomain_id) REFERENCES subdomains (id) );
        """

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sqlite_create_project_table)

        create_table(conn, sqlite_create_scans_table)

        create_table(conn, sqlite_create_assets_table)

        create_table(conn, sqlite_create_subdomain_table)
        create_table(conn, sqlite_create_links_table)
        create_table(conn, sqlite_create_form_table)
        create_table(conn, sqlite_create_webserver_table)
    else:
        print("Error! cannot create the database connection")


def create_project(conn, project):
    sql = '''INSERT INTO projects(name, assets) VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid


def create_scan_result(conn, scan):
    sql = '''INSERT INTO scans(project_id, date,  assets)
    VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, scan)
    conn.commit()
    return cur.lastrowid


def create_asset(conn, asset):
    sql = '''INSERT INTO assets(name, subdomains, scan_id) VALUES(?,?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, asset)
    conn.commit()
    return cur.lastrowid


def create_subdomain(conn, subdomain):
    sql = '''INSERT INTO subdomains(url, google_dorks, webserver, links, asset_id) VALUES(?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, subdomain)
    conn.commit()
    return cur.lastrowid


def create_link(conn, link):
    sql = '''INSERT INTO links(response_code, page_url, tech_stack, header, forms, http_params, hardcoded_strings, 
    screenshots, backup_files, outdated_js, subdomain_id) VALUES(?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, link)
    conn.commit()
    return cur.lastrowid


def create_form(conn, form):
    sql = '''INSERT INTO forms(action, method, parameters, link_id) VALUES(?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, form)
    conn.commit()
    return cur.lastrowid


def create_webserver(conn, webserver):
    sql = '''INSERT INTO webservers(name, version, operating_system, subdomain_id) VALUES(?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, webserver)
    conn.commit()
    return cur.lastrowid


def select_project_id(conn, project_name):
    cur = conn.cursor()
    cur.execute("SELECT id FROM projects WHERE name=?", (project_name,))
    rows = cur.fetchall()
    return rows


class DbConnect:

    def __init__(self):
        pass


if __name__ == '__main__':
    conn = create_connection()
    with conn:
        create_all_tables()

