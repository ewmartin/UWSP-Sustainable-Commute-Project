import datetime

db.define_table('articles',
                    Field('author', db.auth_user),
                    Field('title','text'),                
                    Field('published','date',default=datetime.datetime.now()),
                    Field('bodytext','text'))

db.articles.author.requires = IS_IN_DB(db, 'auth_user.id', 'auth_user.first_name')
db.articles.bodytext.requires = IS_NOT_EMPTY()
db.articles.title.requires = IS_NOT_EMPTY()

#define email table
db.define_table('email_list',Field('emailID','string'))

db.define_table('user_data_debug',
                    Field('first_name'),
                    Field('last_name'),
                    Field('email'),
                    Field('uwsp_id'),
                    Field('home_address'),
                    Field('home_city'),
                    Field('home_state'),
                    Field('home_zip'),
                    Field('home_phone'),
                    Field('local_address'),
                    Field('local_city'),
                    Field('local_state'),
                    Field('local_zip'),
                    Field('local_phone'))
                    
db.define_table('user_data_raw',
                    Field('first_'),
                    Field('last_'),
                    Field('email'),
                    Field('hadd'),
                    Field('hcity'),
                    Field('hstate'),
                    Field('hzip'),
                    Field('hphone'),
                    Field('ladd'),
                    Field('lcity'),
                    Field('lstate'),
                    Field('lzip'),
                    Field('lphone'),
                    Field('miles'))

db.define_table('response_user',
                    Field('first_name'),
                    Field('last_name'),
                    Field('email'),
                    Field('address'),
                    Field('city'),
                    Field('zip'),
                    Field('ustate'))
db.response_user.email.requires = IS_NOT_IN_DB(db, 'response_user.email', error_message='Email already used!')
db.define_table('uwsp_user',
                Field('ruser', db.response_user),
                Field('uwsp_id'),
                Field('uwsp_status'),
                Field('uwsp_years'),
                Field('uwsp_dept'))

db.define_table('category',
                Field('category_name'))


#inialize questions table
db.define_table('question',
                Field('question_text'),
                Field('type_id'),
                Field('answers'),
                Field('category',db.category),
                Field('question_order'))
#, 'datetime', default = datetime.datetime.now()))
#inialize response table
db.define_table('response',
                Field('response_to',db.question),
                Field('ruser', db.response_user),
                Field('answer','text'),
                Field('res_time', 'datetime', default = datetime.datetime.now()))

