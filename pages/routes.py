from market import app
from flask import render_template, redirect, url_for, flash
from market.models import Sahip, Hekim , Randevu
from market.forms import RegisterForm, LoginForm, AnimalForm, AppointmentForm, HekimForm
from market import db
from flask_login import login_user, logout_user, login_required
from flask_login import current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/randevu')
@login_required
def market_page():
    return render_template('randevu.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        tc=form.tc.data
        isim=form.fname.data
        soyisim=form.lname.data
        email_address=form.email_address.data
        password_hash=form.password1.data
        new_user = Sahip(tc,isim,soyisim,email_address,password_hash)
        insert = 'insert into sahip values(\'{tc}\',\'{isim}\',\'{soyisim}\',\'{email_address}\',\'{password_hash}\')'.format(
                                                                                                    tc=tc,
                                                                                                    isim=isim,
                                                                                                    soyisim=soyisim,
                                                                                                    email_address=email_address,
                                                                                                    password_hash=password_hash)
        db.engine.execute(insert)
        db.session.commit()
        login_user(new_user,force = True)
        flash(f"Account created successfully! You are now logged in as {new_user.isim}", category='success')
        render_template('base.html')
        return redirect(url_for('market_page'))

    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        select = "select password_hash from sahip where email_address = \'{email_address}\'".format(email_address=form.email_address.data)
        pswd1 = str(db.engine.execute(select).fetchone())
        pswd = pswd1[2:-3]
        attempted_user = Sahip.query.filter_by(
            email_address=form.email_address.data).first()
            
        if attempted_user and pswd == form.password.data and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user, remember = True, force = True)
            flash(  
                f'Success! You are logged in as: {attempted_user.isim}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not match! Please try again',
                  category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route('/randevu/hayvan', methods=['GET', 'POST'])
@login_required
def animal_page():
    form = AnimalForm()
    if form.validate_on_submit():
        query = "select h1.hnum + 1 as start from hayvan as h1 left outer join hayvan as h2 on h1.hnum + 1 = h2.hnum where h2.hnum is null"
        hnum = str(db.engine.execute(query).fetchone())
        hnum = hnum[1:-2]
        if isinstance(form.yas.data, int):
            insert = 'insert into hayvan values(\'{hnum}\',\'{owner}\',\'{name}\',\'{tur}\',{yas})'.format(
                                                                    hnum=hnum,
                                                                    owner = current_user.tc,
                                                                    name=form.name.data,
                                                                    tur=form.tur.data,
                                                                    yas=form.yas.data)
            db.engine.execute(insert)
            db.session.commit()
            return redirect(url_for("market_page"))
        else:
            flash('Ekleme sirasinda bir hata olustu. Lutfen tekrar dene',
                  category='danger')
            return render_template('hayvan.html', form=form)
    else:
        flash('Ekleme sirasinda bir hata olustu. Lutfen tekrar dene',
                  category='danger')
    return render_template('hayvan.html', form=form)    

@app.route('/randevu/al', methods=['GET', 'POST'])
@login_required
def randevu_page():
    form = AppointmentForm()    
    if form.validate_on_submit():    
        insert = 'insert into randevu values(\'{date}\',\'{saat}\',\'{hayvanlar}\',\'{hekimler}\')'.format(
                                                                    date = form.tarih.data,
                                                                    saat=form.saat.data,
                                                                    hayvanlar=form.hayvanlar.data,
                                                                    hekimler=form.hekimler.data)
        
        db.engine.execute(insert)
        db.session.commit()
        return redirect(url_for("market_page"))
    else:
        return render_template('al.html', form=form)   

@app.route('/randevu/eski')
@login_required
def eski_page():
    randevular = Randevu.query.filter_by()
    return render_template('eski.html',randevular = randevular) 

@app.route('/admin')
@login_required
def admin_page():
    hekimler = Hekim.query.all()
    return render_template('admin.html', hekimler=hekimler)

@app.route('/admin/hekim', methods=['GET', 'POST'])
@login_required
def hekim_page():
    form = HekimForm()
    if 1:     
        query = "select h1.num + 1 as start from hekim as h1 left outer join hekim as h2 on h1.num + 1 = h2.num where h2.num is null"
        hnum = str(db.engine.execute(query).fetchone())
        hnum = int(hnum[1:-2])   
        
        if form.soyisim.data != None:
            insert = 'insert into hekim values(\'{isim}\',\'{soyisim}\',\'{email}\',\'{sifre}\',{num})'.format(
                                                                    soyisim = form.soyisim.data,
                                                                    isim=form.isim.data,
                                                                    sifre=form.sifre.data,
                                                                    email=form.email.data,
                                                                    num=hnum)
        
            db.engine.execute(insert)
            db.session.commit()
            return redirect(url_for("admin_page"))
        else:
            flash('Ekleme sirasinda bir hata olustu. Lutfen tekrar dene',
                  category='danger')
            return render_template('hekim.html', form=form)
    else:
        flash('Ekleme sirasinda bir hata olustu. Lutfen tekrar dene',
                  category='danger')
        return render_template('hekim.html', form=form)