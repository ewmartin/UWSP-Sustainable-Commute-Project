def index(): 
#check session and foward properly
#session.survey_status (1=completed index(on address),2=completed address(on route)
 
    #uwsp form
    form=FORM(DIV(H3('UWSP ID:',_class='hlabel'),
    INPUT(_name='uwspid',_class='styledinput surveyinput',requires=IS_NOT_EMPTY()),_class='surveyrow'),
    DIV(LABEL('UWSP Status:',_class='hlabel',_for='uwstatus'),SELECT('Student','Faculty','Staff',_name='uwstatus',_value='Student',_class='surveyinput',_id='uwstatus'),_class='surveyrow'),
    DIV(LABEL('Years at UWSP:',_class='hlabel',_for='uwyears'),INPUT(_name='uwyears',_class='styledinput surveyinput',_id='uwyears',requires=IS_NOT_EMPTY()),_class='surveyrow'),
    DIV(INPUT(_type='submit',_value='start',_class='surveyinput',requires=IS_NOT_EMPTY()),_class='surveyrow'),_formname='form1')
    
    #non uwsp form
    form2 = FORM(
    DIV(H3('First Name:',_class='hlabel'),INPUT(_name='fname',_class='styledinput surveyinput',requires=IS_NOT_EMPTY()),_class='surveyrow'),
    DIV(H3('Last Name:',_class='hlabel'),INPUT(_name='lname',_class='styledinput surveyinput',_requires=IS_NOT_EMPTY()),_class='surveyrow'),
    DIV(H3('Email:',_class='hlabel'),INPUT(_name='email',_class='styledinput surveyinput',_requires=IS_EMAIL()),_class='surveyrow'),
    INPUT(_type='submit',_value='start',requires=IS_NOT_EMPTY(),_class='surveyinput'),_formname='form2')
    
    #if uwsp form validates
    if form.accepts(request,session,formname='form1'):
        session.uwspid = form.vars.uwspid
        session.uwstatus = form.vars.uwstatus
        session.uwyears = form.vars.uwyears
        session.isUwspUser = 1
        redirect(URL('address'))
    elif form.errors:
        response.flash = 'Please fix the form errors'
        
    #if other form validates
    if form2.accepts(request,session,formname='form2'):
        session.fname = form2.vars.fname
        session.lname = form2.vars.lname
        session.email = form2.vars.email
        session.isUwspUser = 0
    elif form.errors:
        response.flash = 'Please fix the form errors'
        
    return dict(form=form,form2=form2)
def address():

    #create address form
    form=FORM(
    DIV(H3('Address:',_class='hlabel'),INPUT(_name='addr',_class='styledinput surveyinput',requires=IS_NOT_EMPTY()),_class='surveyrow'),
    DIV(H3('City:',_class='hlabel'),INPUT(_name='city',_class='styledinput surveyinput',requires=IS_NOT_EMPTY()),_class='surveyrow'),
    DIV(H3('State:',_class='hlabel'),INPUT(_name='state',_class='styledinput surveyinput',requires=IS_NOT_EMPTY()),_class='surveyrow'),
    DIV(H3('Zip Code:',_class='hlabel'),INPUT(_name='zip',_maxlength='5',_class='styledinput surveyinput',requires=IS_NOT_EMPTY()),_class='surveyrow'),
    DIV(INPUT(_type='submit',_value='next',_class='surveyinput'),_class='surveyrow'),_formname='address_form')
    
    #jquery slider control form for transportation frequency
    slider_form=FORM(
    H2('How do you get to school?'),
    P('Bike:',INPUT(_type='hidden',_name='bike'),
    DIV(_class='tran_slider')),
    P('Bus:',INPUT(_type='hidden',_name='bus'),
    DIV(_class='tran_slider')),
    P('Car:',INPUT(_type='hidden',_name='car'),
    DIV(_class='tran_slider')),
    P('Walk:',INPUT(_type='hidden',_name='walk'),
    DIV(_class='tran_slider')),_formname='slider_form')  
    
    #initilize form2
    form2 = FORM()

    #query for result
    if session.uwspid:
        emailQuery = session.uwspid +'@uwsp.edu'
        result = db(db.response_user.email == emailQuery).select().first()
        #if uwsp user in our response data
        if result:
            #populate form
            response.flash = 'UWSP ID: ' + session.uwspid + ' found!'
            form.vars.addr = result.address
            form.vars.city = result.city
            form.vars.state = result.state
            form.vars.zip = result.zip
        else:
            #query raw data
            result = db(db.user_data_raw.email==emailQuery).select() 
            #if user in raw data
            if(len(result) > 0):
                #populate form
                response.flash = 'UWSP ID: ' + session.uwspid + ' found!'
                form.vars.addr = result[0].ladd
                form.vars.city = result[0].lcity
                form.vars.state = result[0].lstate
                form.vars.zip = result[0].lzip.split(".")[0]  
                #save their name
                session.fname = result[0].first_
                session.lname = result[0].last_
                session.email = result[0].email   
            else:
                #uwsp user not in data
                #add additional information form
                response.flash = 'UWSP ID: ' + session.uwspid + ' not found! Fill out additional information.'
                form2 = FORM(
                DIV(H3('First Name:',_class='hlabel'),INPUT(_name='fname',_class='styledinput surveyinput',requires=IS_NOT_EMPTY()),_class='surveyrow'),
                DIV(H3('Last Name:',_class='hlabel'),INPUT(_name='lname',_class='styledinput surveyinput',_requires=IS_NOT_EMPTY()),_class='surveyrow'),
                DIV(H3('Email:',_class='hlabel'),INPUT(_name='email',_class='styledinput surveyinput',_requires=IS_EMAIL()),_class='surveyrow'),_formname='form2')
                session.isUwspUser = 0

    if slider_form.accepts(request,session,formname='slider_form'):
        session.bikeDay = slider_form.vars.bike
        session.busDay = slider_form.vars.bus
        session.walkDay = slider_form.vars.walk
        session.carDay = slider_form.vars.car
        #Save data to databse
        
    #if additional information form validates
    if form2.accepts(request,session,formname='form2'):
        #save name
        session.fname = form2.vars.fname
        session.lname = form2.vars.lname
        session.email = form2.vars.email
        session.isUwspUser = 0
    elif form.errors:
        response.flash = 'Please fix the form errors'
            
    #if address form validates
    if form.accepts(request,session,formname='address_form'):
        session.addr = form.vars.addr
        session.city = form.vars.city
        session.state = form.vars.state
        session.zip = form.vars.zip
        
        #query for existing user
        result = db(db.response_user.email == session.email).select().first()
        #if found
        if result:
            #update
            result.address = session.addr
            result.city = session.city
            result.zip = session.zip
            result.first_name = session.fname
            result.last_name = session.lname
            result.state = session.state
            result.update_record()
                    
        else:
            #insert new record
            db.response_user.insert(address = session.addr, city = session.city,
                zip = session.zip, first_name = session.fname, last_name = session.lname, email = session.email,state=session.state)
            db.commit()
        #if user entered uwspid
        if session.uwspid:
            result = db(db.response_user.email == session.email).select().first()
            uwspresult = db(db.uwsp_user.user == result.id).select().first()
            #if uwsp user already exists
            if uwspresult:
                #update record
                uwspresult.uwsp_id = session.uwspid
                uwspresult.uwsp_status = session.uwstatus
                uwspresult.uwsp_years = session.uwyears
                uwspresult.update_record()
            else:
                #insert new record
                db.uwsp_user.insert(uwsp_id = session.uwspid,uwsp_status = session.uwstatus, uwsp_years = session.uwyears, user = result.id)        
        redirect(URL('route'))
     
    return dict(form=form,slider_form=slider_form,form2=form2)
   
def route():
#route based on session data
#query for user route
#return route path
    #if user is a uwspuser
    if session.isUwspUser == 1:
        #set url for KML
        static_route = 'kml/2010/' + session.uwspid +'.kmz'
        kml_route = URL('static',static_route)
        session.viewRoute = 1
        session.setRoute = 0
    else:
        #set varibles for generated route
        kml_route = '1'
        session.viewRoute = 0
        session.setRoute = 0

    #create confirmation form
    form = FORM(
    H1('Is this your route to school?'),
    INPUT(_type='submit',_value='Yes',_name='map_accurate',_class='styledinput'),
    INPUT(_type='submit',_value='No',_name='map_accurate',_class='styledinput'))
    
    #if confirmation form validates
    if form.accepts(request):
        #if the user confirmmed the route
        if request.vars.map_accurate == 'Yes':
            #delete uneeded session vars
            del session.setRoute
            del session.viewRoute
            #insert route into response table
            question = db(db.question.question_text == 'route to school').select().first()
            response_user = db(db.response_user.email == session.email).select().first()
            db.response.insert(response_to=question.id,user=response_user.id,answer='true')
            redirect('parking')
        else:
            #set session vars to create new route
            response.flash = 'Please edit and confirm your route'
            del session.viewRoute
            session.setRoute = 1

    #create drag route form
    form2 = FORM(
           H2('Please drag the route to reflect the route you take to school'),
           INPUT(_type='submit',_value='Confirm',_name='map_confirm',_class='styledinput '),
           INPUT(_type='hidden',_name='route',_id='route', requires=IS_NOT_EMPTY()))
       
    #if the user confirmed their 'new' route
    if form2.accepts(request,session):
        if form2.vars.map_confirm == 'Confirm':
            #delete unneeded session vars
            del session.setRoute
            #insert new route into response table
            question = db(db.question.question_text == 'route to school').select().first()
            response_user = db(db.response_user.email == session.email).select().first()
            db.response.insert(response_to=question.id,user=response_user.id,answer=form2.vars.route)
            redirect('parking')
   
       
    return dict(kmlroute=kml_route,form=form,form2=form2)

def parking():
    return dict(form=FORM())
