from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from .auth import login_required
from .db import get_db
import openai

bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    """Show all the posts, most recent first."""
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("blog/index.html", posts=posts)


def get_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/<int:id>/update", methods=("POST", "GET"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)
    author_id = g.user["id"]


    # DB
    db = get_db()

    # Insert new message into table
    if request.method == "POST":
        body = request.form["body"]

        print("writing row", "id=%s" % (id), "author_id=%d" % (author_id), "body=%s" % (body))
        db.execute(
            "INSERT INTO conversation (topic_id, body, author_id) VALUES (?, ?, ?)", (id, body, author_id)
        )

        # Load history
        db = get_db()
        res = db.execute(
            "SELECT author_id, body FROM conversation WHERE topic_id = ?", (id, )
        )
        rows = res.fetchall()

        # Now get response
        response = get_response_from_ai(rows)
        system_id = 0
        print("writing row", "id=%s" % (id), "author_id=%d" % (system_id), "body=%s" % (response))
        db.execute(
            "INSERT INTO conversation (topic_id, body, author_id) VALUES (?, ?, ?)", (id, response, system_id)
        )

        db.commit()

    # For GET and POST (after insert)
    # Load again
    res = db.execute(
        "SELECT author_id, body FROM conversation WHERE topic_id = ?", (id, )
    )
    rows = res.fetchall()

    history = ''
    for row in rows:
        #print("reading row", "id=%s" % (id), row['author_id'], row['body'])
        history = history + "\n" + row['body']

    post = dict(post)
    post['body'] = history
    #print("History=[%s]" % history)

    # form pretty output
    post['body'] = decorate_history(rows)

    # Show conversation
    return render_template("blog/update.html", post=post)

@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))

def get_response_from_ai(rows):
    # Init client
    if "openai_client" not in g:
        g.openai_client = openai.OpenAI()

    # Exit if there is no client
    if "openai_client" not in g or g.openai_client is None:
        return "Failed to create OpenAI client"

    # Get client from global context
    openai_client = g.openai_client

    messages = []
    message = {
        "role": "system",
        "content": "You are a helpful assistant."
    }
    messages.append(message)
    for row in rows:
        message = {
            "role": "user" if row['author_id'] != 0 else "assistant",
            "content": row['body']
        }
        messages.append(message)

    # Get response from backend AI engine
    print("sending chat completions request", messages)
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages
    )
    print("received response of chat completions request", response)
    return response.choices[0].message.content


# decorate conversation history with html tags
def decorate_history(rows):
    response = ""
    for row in rows:
        entry = "%s: %s\n\n" % ("user" if row['author_id'] != 0 else "assistant", row['body'])
        response = response + entry

    return response