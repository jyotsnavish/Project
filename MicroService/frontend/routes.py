from flask import Blueprint, render_template, session, redirect, request, flash, url_for
from flask_login import current_user, logout_user
from api.user_api import UserClient
from api.order_client import OrderClient
from api.book_client import BookClient
import forms

blueprint = Blueprint('frontend',__name__)

@blueprint.context_processor
def cart_count():
    count = 0
    order = session.get('order')
    if order:
        for item in order.get('order_items'):
            count += item['quantity']

    return {'items_in_cart': count}

@blueprint.route('/',methods=['GET'])
def index():
    
    if current_user.is_authenticated:
        session['order'] = OrderClient.get_order_session()
    try:
        books = BookClient.get_books()
    except: 
        books = {'result': []}

    return render_template('index.html',books=books)

@blueprint.route('/register',methods=['GET','POST'])
def register():
    form = forms.RegistrationForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data

            if UserClient.user_exists(username):
                flash("Please try another user name")
                return render_template('register.html', form=form)
            else:
                user = UserClient.create_user(form)
                if user:
                    flash("Registered. Please Login")
                    return redirect(url_for('frontend.index'))
        else:
            flash("Error")
    return render_template('register.html', form=form)
                                       
@blueprint.route('/login',methods=['GET','POST'])
def login():
    form = forms.LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            api_key = UserClient.login(form)
            if api_key:
                session['user_api_key'] = api_key
                user = UserClient.get_user()
                session['user'] = user['result']

                order = OrderClient.get_order()
                if order.get('result'):
                    session['order'] = order['result']

                flash("Welcome")
                return redirect(url_for('frontend.index'))
            else:
                flash("Cannot login")
        else:
            flash("Cannot login")
    return render_template('login.html', form=form)

@blueprint.route('/logout',methods=['GET'])
def logout():
    session.clear()
    logout_user()
    flash("Logged Out")
    return redirect(url_for('frontend.index'))

@blueprint.route('/book/<slug>',methods=['GET','POST'])
def book_details(slug):
    response = BookClient.get_book(slug)
    book = response['result']

    form = forms.ItemForm(book_id=book['id'])

    if request.method == 'POST':
        if 'user' not in session:
            flash("Please login")
            return redirect(url_for("frontend.login"))
        
        order = OrderClient.add_to_cart(book_id=book['id'],quantity=1)
        session['order'] = order['result']
        flash("Book added to the cart")
    return render_template('book_info.html',book=book, form=form)

@blueprint.route('/checkout',methods=['GET'])
def checkout():
    if 'user' not in session:
        flash("Please login")
        return redirect(url_for('frontend.login'))
    
    if 'order' not in session:
        flash("Please add some items in the cart")
        return redirect(url_for('frontend.index'))
    
    order = OrderClient.get_order()

    if len(order['result']['order_items']) == 0:
        flash("Please add some items in the cart")
        return redirect(url_for('frontend.index'))
    
    OrderClient.checkout()
    return redirect(url_for('frontend.thank_you'))

@blueprint.route('/thank-you', methods=['GET'])
def thank_you():
    if 'user' not in session:
        flash("Please login")
        return redirect(url_for('frontend.login'))
    
    if 'order' not in session:
        flash("Please add some items in the cart")
        return redirect(url_for('frontend.index'))
    
    session.pop('order',None)
    flash("Thank you for placing the Order")

    return render_template('thankyou.html')

