import odoo.http as http

class HomePage(http.Controller):
     @http.route('/new_home_page', type='http', auth='user', website=True)
     def show_custom_homepage(self, **kw):
          return http.request.render('website_template.new_home_page', {})