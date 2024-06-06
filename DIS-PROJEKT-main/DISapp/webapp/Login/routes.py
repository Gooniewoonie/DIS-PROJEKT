from flask import render_template, redirect, url_for, flash, request, Blueprint
from webapp import app,conn,bcrypt,roles,mysession
from flask_login import login_user, current_user, logout_user, login_required
from webapp.forms import UserLoginForm, RegistrationForm, SearchForm
from webapp.models import User, select_user, insert_user, search_users
import psycopg2


roles = ["admin","free-user", "bronze-user", "silver-user","gold-user"]
Login = Blueprint('Login', __name__)

@Login.route("/")
@Login.route("/home")
def home():
    mysession["state"] = "home or /"
    role = mysession.get("role", None)
    return render_template('home.html', role=role)

@Login.route("/about")
def about():
    mysession["state"] = "about"
    return render_template('about.html', title='About')

@Login.route("/login", methods=['GET', 'POST'])
def login():
    mysession["state"] = "login"
    if current_user.is_authenticated:
        return redirect(url_for('Login.home'))

    form = UserLoginForm()
    if form.validate_on_submit():
        user = select_user(form.username.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            mysession["role"] = user.role
            mysession["id"] = user.id
            flash('Login successful.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Login.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', form=form, role=mysession.get("role"))


@Login.route("/logout")
def logout():
    mysession["state"] = "logout"
    logout_user()
    return redirect(url_for('Login.home'))

@Login.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('Login.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        insert_user(form.username.data, hashed_password, form.role.data)
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('Login.login'))
    
    return render_template('register.html', form=form)

@Login.route("/account")
@login_required
def account():
    mysession["state"] = "account"
    role = mysession.get("role", None)
    user = current_user
    return render_template('account.html', title='Account', user=user, role=role)



# @Login.route("/leaderboard", methods=['GET', 'POST'])
# def leaderboard():
#     query = request.args.get('query', '')
#     if query:
#         users = search_users(query)
#     else:
#         users = get_top_users()
#     return render_template('leaderboard.html', users=users, query=query)

@Login.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    users = []
    if form.validate_on_submit():
        pattern = form.query.data
        users = search_users(pattern)
    return render_template('search.html', form=form, users=users)


@Login.route("/recommender", methods=['GET'])
@login_required
def recommender():
    return render_template('recommender.html')

@Login.route("/recommend_songs/<mood>")
@login_required
def recommend_songs(mood):
    print(f"Selected mood: {mood}")  # debug statem
    songs = get_songs_by_mood(mood)
    print(f"Fetched songs: {songs}")  # also here
    return render_template('recommender.html', songs=songs, mood=mood)

def get_songs_by_mood(mood):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT track_name, Artist.artists, album_name
            FROM Track
            JOIN Artist ON Track.artistID = Artist.artistID
            JOIN Album ON Track.albumID = Album.albumID
            JOIN Mood ON Track.moodID = Mood.moodID
            WHERE LOWER(Mood.MoodName) = LOWER(%s)
            ORDER BY RANDOM()
            LIMIT 100
            """, (mood,))
        songs = cur.fetchall()
        cur.close()
        print(f"Database response: {songs}")  #only for debug but its fixed now
        return [{'track_name': row[0], 'artist_name': row[1], 'album_name': row[2]} for row in songs]
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error fetching songs: {e}")
        return []