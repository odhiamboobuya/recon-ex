"""
this class is for analyzing the properties of each of the assets.
each asset has a name, id and subdomains
"""
from Sublist3r import  sublist3r
from db_connection import create_connection, create_asset


class Asset:

    def __init__(self, scan_object, asset):
        self.name = self.get_asset_name(asset)
        self.scan_object = scan_object
        self.subdomains = []
        self.scan_id = scan_object.scan_id
        self.asset_path = asset
        self.asset_id = None

    def get_asset_name(self, asset):
        return asset.replace('.','_').replace('://','').replace('https','').replace('http','').replace(':','').replace('/','__')

    def get_subdomains(self):
        subdomains = sublist3r.main(self.asset_path,40,'/tmp/sublister_{}'.format(self.scan_object.date),ports=None,silent=True,verbose=True,enable_bruteforce=False, engines=None)
        self.subdomains = subdomains
        return subdomains

    def save_asset(self):
        conn = create_connection()
        with conn:
            asset = (self.name, self.subdomains, self.scan_id)
            self.asset_id = create_asset(conn, asset)
        return self.asset_id
