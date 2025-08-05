from flask import render_template, request, redirect, url_for, flash, session
from datetime import datetime, date, timedelta
from app import app
from data import APARTMENTS, FLAT_TYPES, FLATS, get_apartment_by_id, get_flat_type_by_id, get_flat_by_id, get_flats_by_apartment
from models import booking_manager

# Make date, datetime, and timedelta available in all templates
@app.context_processor
def inject_date():
    return dict(date=date, datetime=datetime, timedelta=timedelta)

@app.route('/')
def index():
    return render_template('index.html', 
                         apartments=APARTMENTS, 
                         flat_types=FLAT_TYPES)

@app.route('/apartments')
def apartments():
    return render_template('apartments.html', apartments=APARTMENTS)

@app.route('/apartment/<int:apartment_id>')
def apartment_details(apartment_id):
    apartment = get_apartment_by_id(apartment_id)
    if not apartment:
        flash('Apartment not found.', 'error')
        return redirect(url_for('apartments'))
    
    flats = get_flats_by_apartment(apartment_id)
    
    # Group flats by type for display
    flats_by_type = {}
    for flat in flats:
        flat_type = get_flat_type_by_id(flat.flat_type_id)
        if flat_type.id not in flats_by_type:
            flats_by_type[flat_type.id] = {
                'type': flat_type,
                'flats': []
            }
        flats_by_type[flat_type.id]['flats'].append(flat)
    
    return render_template('flat_details.html', 
                         apartment=apartment, 
                         flats_by_type=flats_by_type)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        check_in_str = request.form.get('check_in')
        check_out_str = request.form.get('check_out')
        guests = int(request.form.get('guests', 1))
        apartment_id = request.form.get('apartment_id')
        flat_type_id = request.form.get('flat_type_id')
        
        # Validate dates
        try:
            check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
            
            if check_in < date.today():
                flash('Check-in date cannot be in the past.', 'error')
                return redirect(url_for('index'))
            
            if check_out <= check_in:
                flash('Check-out date must be after check-in date.', 'error')
                return redirect(url_for('index'))
                
        except ValueError:
            flash('Invalid date format.', 'error')
            return redirect(url_for('index'))
        
        # Filter available flats
        available_flats = []
        for flat in FLATS:
            # Filter by apartment if specified
            if apartment_id and flat.apartment_id != int(apartment_id):
                continue
            
            # Filter by flat type if specified
            if flat_type_id and flat.flat_type_id != int(flat_type_id):
                continue
            
            # Check guest capacity
            flat_type = get_flat_type_by_id(flat.flat_type_id)
            if flat_type.max_guests < guests:
                continue
            
            # Check availability
            if booking_manager.is_flat_available(flat.id, check_in, check_out):
                available_flats.append({
                    'flat': flat,
                    'apartment': get_apartment_by_id(flat.apartment_id),
                    'flat_type': flat_type
                })
        
        # Store search parameters in session
        session['search_params'] = {
            'check_in': check_in_str,
            'check_out': check_out_str,
            'guests': guests
        }
        
        return render_template('apartments.html', 
                             apartments=APARTMENTS,
                             available_flats=available_flats,
                             search_params=session['search_params'])
    
    return redirect(url_for('index'))

@app.route('/book/<int:flat_id>')
def book_flat(flat_id):
    flat = get_flat_by_id(flat_id)
    if not flat:
        flash('Flat not found.', 'error')
        return redirect(url_for('index'))
    
    apartment = get_apartment_by_id(flat.apartment_id)
    flat_type = get_flat_type_by_id(flat.flat_type_id)
    
    # Get search parameters from session
    search_params = session.get('search_params', {})
    
    return render_template('booking.html', 
                         flat=flat, 
                         apartment=apartment, 
                         flat_type=flat_type,
                         search_params=search_params)

@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    flat_id = int(request.form.get('flat_id'))
    guest_name = request.form.get('guest_name')
    guest_email = request.form.get('guest_email')
    guest_phone = request.form.get('guest_phone')
    check_in_str = request.form.get('check_in')
    check_out_str = request.form.get('check_out')
    total_guests = int(request.form.get('total_guests'))
    special_requests = request.form.get('special_requests', '')
    
    # Validate required fields
    if not all([flat_id, guest_name, guest_email, guest_phone, check_in_str, check_out_str]):
        flash('All required fields must be filled.', 'error')
        return redirect(url_for('book_flat', flat_id=flat_id))
    
    try:
        check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
        check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
    except ValueError:
        flash('Invalid date format.', 'error')
        return redirect(url_for('book_flat', flat_id=flat_id))
    
    # Check if flat is still available
    if not booking_manager.is_flat_available(flat_id, check_in, check_out):
        flash('Sorry, this flat is no longer available for the selected dates.', 'error')
        return redirect(url_for('book_flat', flat_id=flat_id))
    
    # Calculate total price
    flat = get_flat_by_id(flat_id)
    flat_type = get_flat_type_by_id(flat.flat_type_id)
    nights = (check_out - check_in).days
    total_price = flat_type.base_price * nights
    
    # Create booking
    booking = booking_manager.create_booking(
        flat_id=flat_id,
        guest_name=guest_name,
        guest_email=guest_email,
        guest_phone=guest_phone,
        check_in=check_in,
        check_out=check_out,
        total_guests=total_guests,
        total_price=total_price,
        special_requests=special_requests
    )
    
    return redirect(url_for('booking_confirmation', booking_id=booking.id))

@app.route('/confirmation/<int:booking_id>')
def booking_confirmation(booking_id):
    booking = booking_manager.get_booking(booking_id)
    if not booking:
        flash('Booking not found.', 'error')
        return redirect(url_for('index'))
    
    flat = get_flat_by_id(booking.flat_id)
    apartment = get_apartment_by_id(flat.apartment_id)
    flat_type = get_flat_type_by_id(flat.flat_type_id)
    
    return render_template('confirmation.html', 
                         booking=booking, 
                         flat=flat, 
                         apartment=apartment, 
                         flat_type=flat_type)

@app.route('/my_bookings', methods=['GET', 'POST'])
def my_bookings():
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            bookings = booking_manager.get_bookings_by_email(email)
            booking_details = []
            for booking in bookings:
                flat = get_flat_by_id(booking.flat_id)
                apartment = get_apartment_by_id(flat.apartment_id)
                flat_type = get_flat_type_by_id(flat.flat_type_id)
                booking_details.append({
                    'booking': booking,
                    'flat': flat,
                    'apartment': apartment,
                    'flat_type': flat_type
                })
            return render_template('my_bookings.html', booking_details=booking_details, email=email)
        else:
            flash('Please enter your email address.', 'error')
    
    return render_template('my_bookings.html')

@app.route('/cancel_booking/<int:booking_id>')
def cancel_booking(booking_id):
    if booking_manager.cancel_booking(booking_id):
        flash('Booking cancelled successfully.', 'success')
    else:
        flash('Booking not found or could not be cancelled.', 'error')
    
    return redirect(url_for('my_bookings'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html'), 500
