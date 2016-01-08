from system.core.router import routes

routes['default_controller'] = 'Uwheres'
routes['/loginpage'] = 'Uwheres#login_page'
routes['/registerpage'] = 'Uwheres#register_page'
routes['POST']['/register'] = 'Uwheres#register'
routes['POST']['/login'] = 'Uwheres#logging'
routes['/uwhere/<id>'] = 'Uwheres#profile'
routes['/logout'] = 'Uwheres#logout'
routes['POST']['/send/<id>'] = 'Uwheres#sendMessage'
routes['/add/<phone>'] = 'Uwheres#add'