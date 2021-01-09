from db_connection import create_connection, create_form


class Form():

    def __init__(self, link_id, form_object, form_index):
        self.action = form_object[str(form_index)]['action']
        self.parameters = form_object[str(form_index)]['inputs']
        self.method = form_object[str(form_index)]['method']
        self.link_id = link_id
        self.form_id = None

    def save_form(self):
        conn = create_connection()
        with conn:
            form = (self.action, self.method, self.parameters, self.link_id)
            self.form_id = create_form(conn, form)
        return self.form_id