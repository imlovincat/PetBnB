from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def display_homepage():
    return render_template(
        "index.html",
        the_title="Project - PetBnB",
        the_opening_title="Main Screen",
    )


@app.route("/login")
def petbnb_login():
    return render_template(
        "login.html",
        the_title="Project - PetBnB",
        the_opening_title="Login Screen",
    )

@app.route("/signup")
def petbnb_signup():
    return render_template(
        "signup.html",
        the_title="Project - PetBnB",
        the_opening_title="Sign Up Screen",
    )

@app.route("/bepetsitter")
def petbnb_bepetsitter():
    return render_template(
        "bepetsitter.html",
        the_title="Project - PetBnB",
        the_opening_title="Sign up pet sitter Screen",
    )

@app.route("/processform", methods=["POST"])
def process_from_data():
    data = request.form

    with open("comments.txt", "a") as df:
        print(data["thename"], ",", sep="", end="", file=df)
        print(data["theemail"], ",", sep="", end="", file=df)
        print(data["thesubject"], ",", sep="", end="", file=df)
        print(data["themessage"], file=df)

        return (
            "Hi "
            + data["thename"]
            + ", thank you for visit and leave me your comment! see you :)"
        )
