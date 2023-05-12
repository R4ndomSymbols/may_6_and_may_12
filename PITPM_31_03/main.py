from flask import Flask, make_response, abort, render_template, url_for, request, redirect, session

api = Flask(__name__, template_folder = "templates")
api.secret_key = "ultra_secret"
@api.route('/')
def index():
    return 'Hello World'

@api.route('/books/<genre>')
def books(genre):
    response = make_response("All Books in {} category".format(genre))
    response.headers['Content-Type'] = 'text/plain'
    response.headers['Server'] = 'Foobar'
    return response
    
@api.route('/error404')
def return_404():
    abort(404)
    return make_response("404 Error", 404)

@api.route('/error500')
def http_500_handler():
    return ("500 Error", 500)

@api.route('/rendermarkdown')
def render_markdown():
    response = make_response("## Heading **some_bold_text**", 200)
    response.headers['Content-Type'] = 'text/markdown'
    return response

# @api.route('/redirect')
# def transfer():
#    return redirect("https://localhost:5000/rendermarkdown", code=301)

@api.before_first_request
def initial_handler():
    print("initial_handler called")

@api.before_request
def first_handler():
    print("first_handler called")

@api.after_request
def second_handler(response):
    print("second_handler called")
    return(response)

@api.route("/index")
def index_route():
    print("index route called")
    return 'Index Route Called'

@api.errorhandler(404)
def http_404_handler(error):
    return "пацаны, ашибка", 404

@api.route("/template") 
def show_template():
    name, age, message_to_you = "oleg", 18, "пацаны, не используйте фласк, вы матерям еще нужны"
    template_context = dict(name=name, age=age, message_to_you=message_to_you)
    return render_template('index.html', **template_context)


@api.route("/geturl")
def url_get():
    return redirect(url_for('books', genre = 'romance'))

# lesson 12, cookie

@api.route("/set_name_cookie")
def cookie():
    res = make_response("Set name cookie")
    res.set_cookie('name', 'oleg', max_age=60*60*24)
    return res

@api.route("/set_font", methods = ['GET', 'POST'])
def font_cookie():
     response = make_response(render_template('cookies.html'))
     if (request.method == 'POST'):
        font = request.form.get('font_type_selection')
        response.set_cookie('font_type', font)
        
     return response
#lesson 13 sessions
visit = 'visitcount'
@api.route("/view_count")
def count_views():
    if visit in session:
        session[visit] = session[visit] + 1
    else:
        session[visit] = 1
    return "Число промотров этой страницы: {}".format(session[visit])
@api.route('/clear_session')
def clear_session():
    session.pop(visit, None)
    return 'Session data cleared'

@api.route('/update_session')
def update_session():
    offset = 0
    if visit in session:
        offset = session[visit]
    items_key = 'items'
    items = {'яблоко' : 0, 'манго': 0, 'киви': 0} 
    if items_key in session:
        items_stored = session[items_key]
        for key in items_stored:
            items_stored[key]+=offset
        session[items_key] = items_stored
    else:
        session[items_key] = items
    return str(session[items_key])
    
     
if __name__ == "__main__":
    api.run()

