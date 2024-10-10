{
    'name': 'project_testing',
    'author': 'none',
    'category': '',
    'version': "17.0.0.1.0",
    'depends': ['base','account','board',
                ],
    'data': [
        'security/ir.model.access.csv',
        'views/test.xml',
        'views/data_test.xml',
        'views/partner.xml',
        'views/account_move.xml',
        'views/stambach_test_dashboard.xml',

    ],
    'assets':{
        'web.assets_backend':[
            'testing_app/static/src/components/**/*.js',
            'testing_app/static/src/components/**/*.xml',
            'testing_app/static/src/components/**/*.scss',


        ]
    },


    'application': True,
}
