"""
main file, for running various commands
start by creating a project
after creating project, define scope
the scope should more or less be the assets being scanned

"""
from datetime import datetime

from Project import Project
from Scan import Scan
from Asset import Asset
from Subdomain import Subdomain
from Link import Link
from Form import Form
from db_connection import *


def main(project_name_param_, assets_param, assets_out_of_scope):
    project_name = project_name_param_
    project = Project(project_name)
    assets = assets_param
    project.set_assets(assets)
    project.save_project()
    scan_instance = Scan(project)
    scan_instance.save_scan()
    for asset in assets:
        asset_instance = Asset(scan_instance, asset)
        asset_subdomains = asset_instance.get_subdomains()
        asset_id = asset_instance.save_asset()
        for subdomain in asset_subdomains:
            subdomain_instance = Subdomain(asset_id, subdomain, assets_out_of_scope)
            subdomain_links = subdomain_instance.parse_links()
            subdomain_id = subdomain_instance.save_subdomain()
            for link in subdomain_links:
                if link in assets_out_of_scope: continue
                link_instance = Link(subdomain_id, link)
                link_instance.process_link()
                link_id = link_instance.save_link()
                forms = link_instance.forms
                for form_index in range(len(forms)):
                    form = forms[form_index]
                    form_instance = Form(link_id, form, form_index)
                    form_instance.save_form()


if __name__ == '__main__':
    project_name_param = "testrun_{}".format(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
    assets_in_scope = []
    assets_out_of_scope_param = []
    main(project_name_param, assets_in_scope, assets_out_of_scope_param)
