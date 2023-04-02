from flask import Flask, make_response, abort, render_template, url_for

api = Flask(__name__, template_folder = "templates")

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
    return url_for(books, genre = "romance")



if __name__ == "__main__":
    api.run()



