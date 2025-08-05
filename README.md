# Service Apartments Booking System

A Flask-based web application for booking service apartments with multiple flat types. The system manages three luxury service apartments with a total of 60 flats, offering different accommodation types from studios to 2-bedroom apartments.

## Features

- **3 Service Apartments**: Royal Heights, Garden View Residences, and Metropolitan Suites
- **60 Total Flats**: Studio, 1-Bedroom, 2-Bedroom, and Penthouse units
- **Advanced Search**: Filter by dates, guest count, apartment, and flat type
- **Booking Management**: Complete booking workflow with confirmation
- **Guest Portal**: Email-based booking lookup and cancellation
- **Responsive Design**: Mobile-friendly interface with Bootstrap dark theme

## Requirements

- Python 3.11 or higher
- Modern web browser

## Installation

1. **Clone or download the project files**

2. **Install dependencies:**
   ```bash
   pip install -r deployment_requirements.txt
   ```

3. **Set environment variable (optional):**
   ```bash
   export SESSION_SECRET="your-secret-key-here"
   ```
   On Windows:
   ```cmd
   set SESSION_SECRET=your-secret-key-here
   ```

## Running the Application

### Development Mode
```bash
python main.py
```

### Production Mode
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

The application will be available at `http://localhost:5000`

## Deployment

### For VPS/Cloud Servers

1. Install Python 3.11+ and pip
2. Upload all project files
3. Install dependencies: `pip install -r deployment_requirements.txt`
4. Set environment variables
5. Run with Gunicorn: `gunicorn --bind 0.0.0.0:80 --workers 4 main:app`

### For Heroku

1. Create `Procfile` with: `web: gunicorn main:app`
2. Use `deployment_requirements.txt` as `requirements.txt`
3. Deploy using Heroku CLI or GitHub integration

### For Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r deployment_requirements.txt
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

## Project Structure

```
├── main.py                 # Application entry point
├── app.py                  # Flask application setup
├── routes.py               # URL routes and handlers
├── models.py               # Data models and booking logic
├── data.py                 # Static data definitions
├── deployment_requirements.txt  # Python dependencies
├── templates/              # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── apartments.html
│   ├── flat_details.html
│   ├── booking.html
│   ├── confirmation.html
│   └── my_bookings.html
└── static/                 # CSS and JavaScript
    ├── css/style.css
    └── js/main.js
```

## Data Structure

### Apartments
- **Royal Heights**: 20 flats with luxury amenities
- **Garden View Residences**: 20 flats, family-friendly
- **Metropolitan Suites**: 20 flats in business district

### Flat Types
- **Studio**: $120/night, up to 2 guests
- **1-Bedroom**: $180/night, up to 3 guests
- **2-Bedroom**: $280/night, up to 5 guests
- **Penthouse**: $450/night, up to 6 guests

## Configuration

### Environment Variables
- `SESSION_SECRET`: Secret key for Flask sessions (auto-generated if not set)
- `DATABASE_URL`: Database connection string (optional, not currently used)

### Customization
- Modify `data.py` to change apartment details, pricing, or add more flats
- Update `static/css/style.css` for theme customization
- Edit templates in `templates/` folder for layout changes

## Browser Support

- Chrome, Firefox, Safari, Edge (latest versions)
- Mobile responsive design
- JavaScript required for enhanced features

## License

Open source - feel free to modify and use for your projects.

## Support

For issues or questions, check the code comments or modify the system as needed for your specific requirements.