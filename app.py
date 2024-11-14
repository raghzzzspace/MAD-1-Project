
from flask import Flask, render_template, request, redirect, url_for, flash, session
from model import db, Customer, Professional, Admin
from model import Closed_Services, Services_status,Services,Service_Req, Service_History, Today_Services
import secrets
from sqlalchemy.sql import text
from datetime import datetime
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__, instance_relative_config=True)
app.secret_key = secrets.token_hex(16)

# Configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = r"sqlite:///C:\Users\hp\Desktop\household_services_database.db"  # Absolute path for SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)

# Create the tables (Only needed on the first run)
# with app.app_context():
#     db.create_all()

# for index.html
@app.route("/")
def index():
    return render_template("index.html")

# customer registration
@app.route('/user/customer_register', methods=['GET', 'POST'])
def customer_register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['fullname']
        address = request.form['address']
        pincode = request.form['pincode']

        existing_customer = Customer.query.filter_by(email=email).first()
        if existing_customer:
            flash('Already Registered with this email. Please login.', 'danger')
            return render_template('user/customer_register.html')


        existing_professional = Professional.query.filter_by(email=email).first()
        if existing_professional:
            flash('Already Registered with this email. Please login.', 'danger')
            return render_template('user/customer_register.html')

        new_customer = Customer(
            email=email,
            password=password,
            full_name=full_name,
            address=address,
            pincode=pincode,
            role='customer'
        )

        db.session.add(new_customer)
        db.session.commit()

        flash('Registered Successfully! Please login to continue.', 'success')
        return render_template('user/customer_register.html')

    return render_template('user/customer_register.html')

# professional registration
@app.route('/user/professional_signup', methods=['GET','POST'])
def professional_signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['fullname']
        service_name = request.form['service_name']
        experience = request.form['experience']
        document = request.files['documents']
        address = request.form['address']
        pincode = request.form['pincode']

        existing_customer = Customer.query.filter_by(email=email).first()
        if existing_customer:
            flash('Already Registered with this email. Please login.', 'danger')
            return render_template('user/professional_signup.html')

        
        existing_professional = Professional.query.filter_by(email=email).first()
        if existing_professional:
            flash('Already Registered with this email. Please login.', 'danger')
            return render_template('user/professional_signup.html')

        document_data = document.read() if document else None

        new_professional = Professional(
            email=email,
            password=password,
            full_name=full_name,
            service_name=service_name,
            experience=experience,
            document=document_data,  # PDF as binary data
            address=address,
            pincode=pincode,
            role='professional'
        )

        db.session.add(new_professional)
        db.session.commit()

        flash('Registered Successfully! Please login to continue.', 'success')
        return render_template('user/professional_signup.html')

    return render_template('user/professional_signup.html')



@app.route('/professional/login', methods=['GET'])
def service_professional_login():
    return render_template('user/login.html')

@app.route('/admin/login', methods=['GET'])
def admin_login():
    return render_template('user/login.html')

@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        customer =  Customer.query.filter_by(email=email, password=password).first()
        if customer:
            session['customer_id'] = customer.customer_id
            flash(f'Welcome back, {customer.full_name}!', 'success')
            return redirect(url_for('customer_dashboard'))

        professional = Professional.query.filter_by(email=email, password=password).first()
        if professional:
            session['professional_id'] = professional.professional_id
            flash(f'Welcome back, {professional.full_name}!', 'success')
            return redirect(url_for('professional_dashboard')) 

        admin = Admin.query.filter_by(email=email, password=password).first()
        if admin:
            flash(f'Welcome back, {admin.email}!', 'success')
            return redirect(url_for('admin_dashboard'))  

        flash('Invalid credentials. Please try again.', 'danger')
        return redirect(url_for('user_login'))  

    return render_template('user/login.html')

@app.route('/logout')
def logout():
    session.clear()  
    resp = redirect(url_for('user_login'))
    resp.set_cookie('session', '', expires=0) 
    flash('You have been logged out successfully.', 'info')
    return resp

#CUSTOMER SIDE
@app.route('/user/customer_dashboard', methods=['GET'])
def customer_dashboard():
    customer_id = session['customer_id']
    service_history = Service_History.query.filter_by(id=customer_id).all()
    services = Services.query.all()
    return render_template('user/customer_dashboard.html', services=services,service_history=service_history)

@app.route('/user/customer_profile', methods=['GET'])
def customer_profile():
    customer_id = session['customer_id']
    customer = Customer.query.filter_by(customer_id=customer_id).one()
    return render_template('user/customer_profile.html', customer=customer)

@app.route('/user/customer_remarks', methods=['GET'])
def customer_remarks():
    return render_template('user/customer_remarks.html')

@app.route('/user/submit_service_remarks', methods=['POST'])
def submit_service_remarks():
    customer_id = session['customer_id']
    customer = Customer.query.filter_by(customer_id=customer_id).one()
    service_id = request.form.get('service_id')
    professional = Professional.query.join(Service_History, Professional.full_name == Service_History.professional_name).filter(Service_History.service_id == service_id).filter(Professional.full_name == Service_History.professional_name).one()
    date_string = datetime.today().strftime('%Y-%m-%d')
    
    closed_booking = Closed_Services(
        customer_name=customer.full_name,
        email=customer.email,
        location=customer.address,
        date=datetime.strptime(date_string, "%Y-%m-%d").date(),
        cid=customer.customer_id,
        pid=professional.professional_id,
        rating = request.form.get('rating')
    )
    db.session.add(closed_booking)
    db.session.commit()
    return redirect(url_for('customer_dashboard'))

@app.route('/user/customer_search', methods=['GET', 'POST'])
def customer_search():
    search_results = []
    search_by = None  

    if request.method == 'POST':
        search_by = request.form.get('searchBy')
        search_text = request.form.get('searchInput')

        if not search_text:
            flash('Please enter search text.', 'warning')
            return redirect(url_for('customer_search'))

        if search_by == 'service_name':
            search_results = Professional.query.filter(Professional.service_name.ilike(f"%{search_text}%"),Professional.status == "Approved").all()
        elif search_by == 'pin_code':
            search_results = Professional.query.filter(Professional.pincode.ilike(f"%{search_text}%"),Professional.status == "Approved").all()
        elif search_by == 'location':
            search_results = Professional.query.filter(Professional.address.ilike(f"%{search_text}%"),Professional.status == "Approved").all()
        else:
            flash('Invalid search criteria.', 'danger')

    return render_template('user/customer_search.html', search_results=search_results, search_by=search_by)

@app.route('/book_service', methods=['POST'])
def book_service():
    customer_id = session['customer_id']
    customer = Customer.query.filter_by(customer_id=customer_id).one()

    new_booking = Today_Services(
        customer_name=customer.full_name,
        email=customer.email,
        location=customer.address,
        customer_id=customer.customer_id,
        professional_id=request.form.get('id')
    )
    
    new_booking_cust = Service_History(
        id = customer.customer_id,
        service_name = request.form.get('service_name'),
        professional_name=request.form.get('professional_name'),
        email=request.form.get('email'),
        status = "Requested"
    )

    db.session.add(new_booking)
    db.session.add(new_booking_cust)
    db.session.commit()

    flash('Booking successful!', 'success')
    return redirect(url_for('customer_dashboard'))

@app.route('/close_service', methods=['POST'])
def close_service():
    service_id = request.form.get('service_id')
    service = Service_History.query.filter_by(service_id = service_id).one()
    if service:
        service.status = "Closed"
        db.session.commit()

    professional = Professional.query.join(Service_History, Professional.full_name == Service_History.professional_name).filter(Service_History.service_id == service_id).filter(Professional.full_name == Service_History.professional_name).one()
    customer_id = session['customer_id']
    
    db.session.query(Today_Services).filter_by(professional_id = professional.professional_id, customer_id = customer_id ).delete()
    db.session.commit()

    return render_template('user/customer_remarks.html', service = service)

@app.route('/user/customer_summary', methods=['GET'])
def customer_summary():
    customer_id = session['customer_id']
    total_requested = db.session.query(func.count(Service_History.id)).filter(Service_History.id == customer_id).scalar()

    total_closed = db.session.query(func.count(Service_History.id)).filter(Service_History.id == customer_id, Service_History.status == 'Closed').scalar()

    total_assigned = total_requested - total_closed

    service_history_data = {
        'Requested': total_requested,
        'Closed': total_closed,
        'Assigned': total_assigned
    }

    return render_template('user/customer_summary.html', service_history_data=service_history_data)
    


#PROFESSIONAL SIDE
@app.route('/user/professional_viewprofile/<int:professional_id>', methods=['GET'])
def professional_viewprofile(professional_id):
    professional = Professional.query.get_or_404(professional_id)

    return render_template('user/professional_viewprofile.html', professional=professional)


@app.route('/user/professional_editprofile/<int:professional_id>', methods=['GET', 'POST'])
def professional_editprofile(professional_id):
    professional = Professional.query.get_or_404(professional_id)

    if request.method == 'POST':
        
        email = request.form.get('email', professional.email)  
        password = request.form.get('password')  
        fullname = request.form.get('fullname')
        service_name = request.form.get('service_name')
        experience = request.form.get('experience')
        document = request.files.get('document')  
        address = request.form.get('address')
        pincode = request.form.get('pincode')

        if not fullname or not service_name or not experience or not address or not pincode:
            flash('Please fill in all required fields.', 'danger')
            return render_template('user/professional_editprofile.html', professional=professional)

        if password:
            professional.password = password

        professional.email = email  
        professional.full_name = fullname
        professional.service_name = service_name
        professional.experience = int(experience) if experience else 0
        if document:
            professional.document = document.read()
        professional.address = address
        professional.pincode = pincode

        
        try:
            db.session.commit()
            flash('Your profile has been updated successfully!', 'success')
            return redirect(url_for('professional_viewprofile', professional_id=professional.professional_id))
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {e}", 'danger')
            return render_template('user/professional_editprofile.html', professional=professional)

    return render_template('user/professional_editprofile.html', professional=professional)



def get_logged_in_professional():
    professional_id = session.get('professional_id')
    if professional_id:
        return Professional.query.get(professional_id)
    return None

@app.route('/user/professional_summary', methods=['GET'])
def professional_summary():
    logged_in_professional = get_logged_in_professional()

    if not logged_in_professional:
        return redirect(url_for('user_login'))

    ratings_query = text("""
        SELECT rating, COUNT(*) 
        FROM closed__services 
        WHERE pid = :professional_id
        GROUP BY rating
    """)
    ratings_result = db.session.execute(ratings_query, {'professional_id': logged_in_professional.professional_id}).fetchall()

    ratings_data = {str(row[0]): row[1] for row in ratings_result}

    requests_query = text("""
        SELECT status, COUNT(*) 
        FROM service__history 
        WHERE professional_name = :professional_name
        GROUP BY status
    """)
    requests_result = db.session.execute(requests_query, {'professional_name': logged_in_professional.full_name}).fetchall()

    service_requests_data = {
        'Received': sum(row[1] for row in requests_result),
        'Closed': sum(row[1] for row in requests_result if row[0] == 'C'),
        'Rejected': sum(row[1] for row in requests_result if row[0] == 'R')
    }

    return render_template(
        'user/professional_summary.html',
        ratings_data=ratings_data,
        service_requests_data=service_requests_data
    )



@app.route('/user/professional_dashboard', methods=['GET'])
def professional_dashboard():
    professional = get_logged_in_professional()
    professional_id = session.get('professional_id') 

    today_services = Today_Services.query.filter_by(professional_id=professional_id).all()
    closed_services = Closed_Services.query.filter_by(pid=professional_id).all()

    return render_template('user/professional_dashboard.html', 
                           professional=professional, 
                           today_services=today_services, 
                           closed_services=closed_services)
@app.route('/accept_service/<int:service_id>', methods=['POST'])
def accept_service(service_id):
    service = Today_Services.query.get(service_id)
    if service:
        new_service = Services_status(
            customer_name=service.customer_name,
            email=service.email,
            location=service.location,
            status='A'
        )
        db.session.add(new_service)
        db.session.delete(service)
        db.session.commit()
    return redirect(url_for('professional_dashboard'))

@app.route('/reject_service/<int:service_id>', methods=['POST'])
def reject_service(service_id):

    service = Today_Services.query.get(service_id)
    if service:
        new_service = Services_status(
            customer_name=service.customer_name,
            email=service.email,
            location=service.location,
            status='R'
        )
        db.session.add(new_service)
        db.session.delete(service)
        db.session.commit()
    return redirect(url_for('professional_dashboard'))

@app.route('/user/professional_search', methods=['GET', 'POST'])
def professional_search():
    search_results = []

    if request.method == 'POST':
        search_by = request.form.get('searchBy')
        search_text = request.form.get('searchText')

        if not search_text:
            flash('Please enter search text.', 'warning')
            return redirect(url_for('professional_search'))

        if search_by == 'date':
            search_results = Closed_Services.query.filter(Closed_Services.date == search_text,Closed_Services.pid == session['professional_id']  ).all()
        elif search_by == 'location':
            search_results = Closed_Services.query.filter(Closed_Services.location.ilike(f"%{search_text}%"),Closed_Services.pid == session['professional_id'] ).all()
        elif search_by == 'pincode':
            search_results = Closed_Services.query.filter(Closed_Services.location.contains(search_text),Closed_Services.pid == session['professional_id'] ).all()
        elif search_by == 'customer':
            search_results = Closed_Services.query.filter(Closed_Services.customer_name.ilike(f"%{search_text}%"),Closed_Services.pid == session['professional_id'] ).all()
        else:
            flash('Invalid search criteria.', 'danger')

    return render_template('user/professional_search.html', search_results=search_results)



@app.route('/user/approve_professional/<int:professional_id>', methods=['POST'])
def approve_professional(professional_id):
    professional = Professional.query.get_or_404(professional_id)
    professional.status = 'Approved'
    db.session.commit()
    return redirect(url_for('admin_dashboard'))


@app.route('/user/reject_professional/<int:professional_id>', methods=['POST'])
def reject_professional(professional_id):
    professional = Professional.query.get_or_404(professional_id)
    professional.status = 'Rejected'  
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/user/delete_professional/<int:professional_id>', methods=['POST'])
def delete_professional(professional_id):
    professional = Professional.query.get_or_404(professional_id)
    db.session.delete(professional)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))


#ADMIN SIDE
@app.route('/user/admin_dashboard', methods=['GET'])
def admin_dashboard():
    services=Services.query.all()
    today_services_query = db.session.execute(
        text("""
            SELECT ts.id, ts.professional_id, p.full_name as professional_name
            FROM today__services ts
            LEFT JOIN professional p ON ts.professional_id = p.professional_id
        """)
    ).mappings()

    closed_services_query = db.session.execute(
        text("""
            SELECT cs.id, cs.pid AS professional_id, cs.date, p.full_name as professional_name
            FROM closed__services cs
            LEFT JOIN professional p ON cs.pid = p.professional_id
        """)
    ).mappings()

    service_history_query = db.session.execute(
        text("""
            SELECT sh.service_id AS id, sh.service_name, sh.professional_name, sh.status
            FROM service__history sh
        """)
    ).mappings()

    professionals_query = db.session.execute(
        text("""
            SELECT * FROM professional
        """)
    ).mappings()
    professionals = list(professionals_query)

    today_services = list(today_services_query)
    closed_services = list(closed_services_query)
    service_history = list(service_history_query)

    service_requests = []

    for history in service_history:
        status = 'R' if history['status'] == 'Requested'  else 'C'
        
        service_requests.append({
            'id': history['id'],
            'professional': history['professional_name'],
            'service_name': history['service_name'], 
            'status': status
        })

    return render_template(
        'user/admin_dashboard.html',
        services=services,
        professionals=professionals,
        service_requests=service_requests
    )


@app.route('/user/admin_editservice/<int:service_id>', methods=['GET', 'POST'])
def admin_editservice(service_id):
    service = Services.query.get_or_404(service_id)
    
    if request.method == 'POST':
        service.service_name = request.form['service_name']
        service.base_price = request.form['base_price']
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    
    return render_template('user/admin_editservice.html', service=service)


@app.route('/user/admin_deleteservice/<int:service_id>', methods=['POST'])
def admin_deleteservice(service_id):
    service = Services.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))



@app.route('/user/admin_search', methods=['GET', 'POST'])
def admin_search():
    search_results = []
    search_by = None 

    if request.method == 'POST': 
        search_by = request.form.get('searchBy')
        search_text = request.form.get('searchText')

        if not search_text:
            flash('Please enter search text.', 'warning')
            return redirect(url_for('admin_search'))

        if search_by == 'services':
            search_results = Services.query.filter(Services.service_name.ilike(f"%{search_text}%")).all()
        elif search_by == 'service requests':
            search_results = Service_Req.query.filter(Service_Req.service_name.ilike(f"%{search_text}%")).all()
        elif search_by == 'customers':
            search_results = Customer.query.filter(Customer.full_name.ilike(f"%{search_text}%")).all()
        elif search_by == 'professionals':
            search_results = Professional.query.filter(Professional.full_name.ilike(f"%{search_text}%")).all()
        else:
            flash('Invalid search criteria.', 'danger')

    return render_template('user/admin_search.html', search_results=search_results, search_by=search_by)


@app.route('/user/admin_addservice', methods=['GET', 'POST'])
def admin_addservice():
    if request.method == 'POST':
        service_id = request.form['service_id']
        service_name = request.form['service_name']
        base_price = request.form['base_price']

        new_service = Services(id=service_id,service_name=service_name, base_price=base_price)
        db.session.add(new_service)
        db.session.commit()

        flash('New service added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('user/admin_addservice.html')


@app.route('/user/admin_summary', methods=['GET'])
def admin_summary():
    ratings_query = text("SELECT rating, COUNT(*) FROM closed__services GROUP BY rating")
    ratings_result = db.session.execute(ratings_query).fetchall()

    ratings_data = {str(row[0]): row[1] for row in ratings_result}

    requests_query = text("SELECT COUNT(*) FROM service__history")
    requests_query2 = text("SELECT COUNT(*) FROM closed__services")
    requests_query3 = text("SELECT status,COUNT(*) FROM services_status group by status")
    requests_result2 = db.session.execute(requests_query2).fetchall()
    requests_result = db.session.execute(requests_query).fetchall()
    requests_result3 = db.session.execute(requests_query3).fetchall()
  
    service_requests_data = {
        'Received': (requests_result[0][0]),
        'Closed': sum(row[0] for row in requests_result2),
        'Rejected': sum(row[1] for row in requests_result3 if row[0] == 'R')
    }

    return render_template('user/admin_summary.html', ratings_data=ratings_data, service_requests_data=service_requests_data)


@app.route('/user/admin_profile', methods=['GET'])
def admin_profile():
    return render_template('/user/admin_profile.html')

@app.route('/search_services', methods=['POST'])
def search_services():
    
    
    search_results = []
    search_by = None  

    if request.method == 'POST':  
        search_by = request.form.get('service_type')
        search_results = Professional.query.filter(Professional.service_name.ilike(f"%{search_by}%"),Professional.status == "Approved").all()

    customer_id = session['customer_id']
    service_history = Service_History.query.filter_by(id=customer_id).all()
    services = Services.query.all()

    return render_template('user/customer_dashboard.html', services=services,service_history=service_history,search_results=search_results, search_by=search_by)
    
    







if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
