from flask import Flask, render_template, request, url_for, redirect
import os
import sys
from datetime import datetime

app = Flask(__name__)

DATA = os.path.join(os.getcwd(), "data")
ADMIN_PASTES = os.path.join(os.getcwd(), "data", "admin")
ANON_PASTES = os.path.join(os.getcwd(), "data", "other")

with open(os.path.join(DATA, "template"), "r", encoding="utf-8") as temp_file:
    _DEFAULT_POST_TEMPLATE = temp_file.read()

admin_posts_list = []
anon_posts_list = []


def refreshAdminPosts():
    global admin_posts_list
    admin_posts_file_list = os.listdir(ADMIN_PASTES)
    if not(len(admin_posts_list) == len(admin_posts_file_list)):
        for admin_post_file_name in admin_posts_file_list:
            admin_post_file_name_path = os.path.join(
                ADMIN_PASTES, admin_post_file_name)
            admin_post_file_name_stats = os.stat(admin_post_file_name_path)
            admin_posts_list.append(
                {
                    "name": admin_post_file_name,
                    "size": bytes2KB(admin_post_file_name_stats.st_size),
                    "creation_date": datetime.utcfromtimestamp(int(admin_post_file_name_stats.st_mtime)).strftime('%d-%m-%Y'),
                    "creation_time": datetime.utcfromtimestamp(int(admin_post_file_name_stats.st_mtime)).strftime('%H:%M:%S')
                }
            )


def refreshAnonPosts():
    global anon_posts_list
    anon_posts_file_list = os.listdir(ANON_PASTES)
    if not(len(anon_posts_list) == len(anon_posts_file_list)):
        for anon_post_file_name in anon_posts_file_list:
            anon_post_file_name_path = os.path.join(
                ANON_PASTES, anon_post_file_name)
            anon_post_file_name_stats = os.stat(anon_post_file_name_path)
            anon_posts_list.append(
                {
                    "name": anon_post_file_name,
                    "size": bytes2KB(anon_post_file_name_stats.st_size),
                    "creation_date": datetime.utcfromtimestamp(int(anon_post_file_name_stats.st_mtime)).strftime('%d-%m-%Y'),
                    "creation_time": datetime.utcfromtimestamp(int(anon_post_file_name_stats.st_mtime)).strftime('%H:%M:%S')
                }
            )


def bytes2KB(value):
    return value / 1000


@app.route("/")
def index():
    global admin_posts_list, anon_posts_list

    refreshAdminPosts()
    refreshAnonPosts()

    return render_template("index.html", admin_posts_list=admin_posts_list, anon_posts_list=anon_posts_list)


@app.route("/pages")
def all_links():
    return "All Links"


@app.route("/new")
def new_paste():
    return render_template("new.html", paste_template_text=_DEFAULT_POST_TEMPLATE)


@app.route("/new_paste", methods=['POST'])
def new_paste_form_post():
    global _DEFAULT_POST_TEMPLATE
    try:
        # Sample request.values -->
        #       CombinedMultiDict(
        #       [ImmutableMultiDict([]),
        #        ImmutableMultiDict(
        #           [('pasteTitle', 'sfgds'), ('pasteContent', 'Puk Gula\r\n gfhbfgngf')]
        #       )])

        args = request.values
        pasteTitle = args.get('pasteTitle')
        pasteContent = args.get('pasteContent')
    except Exception as e:
        return f"Error: {e}"

    with open(os.path.join(ANON_PASTES, pasteTitle), "w", encoding="utf-8") as file:
        file.write(pasteContent)
    return redirect(url_for('index'))


@app.route("/post")
def post():
    return render_template("post.html")


if __name__ == "__main__":
    app.run("0.0.0.0", port=8080, debug=False)
