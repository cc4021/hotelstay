from models import Apartment, FlatType, Flat

# Service Apartments Data
APARTMENTS = [
    Apartment(
        id=1,
        name="Royal Heights",
        description="Luxury service apartment with premium amenities in the heart of the city.",
        address="123 Royal Street, Downtown District",
        amenities=["24/7 Concierge", "Fitness Center", "Swimming Pool", "Spa", "Business Center", "Parking", "WiFi"]
    ),
    Apartment(
        id=2,
        name="Garden View Residences",
        description="Modern apartments with beautiful garden views and family-friendly facilities.",
        address="456 Garden Avenue, Green Valley",
        amenities=["Garden Views", "Children's Play Area", "BBQ Area", "Laundry Service", "Parking", "WiFi", "Pet-Friendly"]
    ),
    Apartment(
        id=3,
        name="Metropolitan Suites",
        description="Contemporary urban living with sophisticated design and premium location.",
        address="789 Metro Boulevard, Business District",
        amenities=["City Views", "Rooftop Terrace", "Conference Room", "Gym", "Restaurant", "Valet Parking", "WiFi"]
    )
]

# Flat Types
FLAT_TYPES = [
    FlatType(
        id=1,
        name="Studio",
        description="Compact and efficient studio apartment perfect for solo travelers or couples.",
        max_guests=2,
        base_price=120.00,
        features=["Queen Bed", "Kitchenette", "Private Bathroom", "Work Desk", "Smart TV", "Air Conditioning"]
    ),
    FlatType(
        id=2,
        name="1 Bedroom",
        description="Spacious one-bedroom apartment with separate living area and full kitchen.",
        max_guests=3,
        base_price=180.00,
        features=["King Bed", "Living Room", "Full Kitchen", "Dining Area", "Private Bathroom", "Balcony", "Smart TV", "Air Conditioning"]
    ),
    FlatType(
        id=3,
        name="2 Bedroom",
        description="Large two-bedroom apartment ideal for families or business travelers.",
        max_guests=5,
        base_price=280.00,
        features=["2 Bedrooms", "2 Bathrooms", "Living Room", "Full Kitchen", "Dining Area", "Balcony", "2 Smart TVs", "Air Conditioning", "Washer/Dryer"]
    ),
    FlatType(
        id=4,
        name="Penthouse Suite",
        description="Luxurious penthouse with panoramic views and premium amenities.",
        max_guests=6,
        base_price=450.00,
        features=["3 Bedrooms", "3 Bathrooms", "Large Living Room", "Gourmet Kitchen", "Private Terrace", "City Views", "Premium Furnishing", "Butler Service"]
    )
]

# Generate 60 flats across 3 apartments
FLATS = []
flat_id = 1

# Royal Heights - 20 flats (floors 1-5, 4 flats per floor)
for floor in range(1, 6):
    for room in range(1, 5):
        room_number = f"{floor}0{room}"
        # Distribute flat types: Studio(5), 1BR(8), 2BR(6), Penthouse(1)
        if flat_id <= 5:
            flat_type_id = 1  # Studio
        elif flat_id <= 13:
            flat_type_id = 2  # 1 Bedroom
        elif flat_id <= 19:
            flat_type_id = 3  # 2 Bedroom
        else:
            flat_type_id = 4  # Penthouse
        
        FLATS.append(Flat(
            id=flat_id,
            apartment_id=1,
            flat_type_id=flat_type_id,
            floor=floor,
            room_number=room_number
        ))
        flat_id += 1

# Garden View Residences - 20 flats (floors 1-5, 4 flats per floor)
for floor in range(1, 6):
    for room in range(1, 5):
        room_number = f"{floor}0{room}"
        # Distribute flat types: Studio(6), 1BR(10), 2BR(4)
        if flat_id <= 26:
            flat_type_id = 1  # Studio
        elif flat_id <= 36:
            flat_type_id = 2  # 1 Bedroom
        else:
            flat_type_id = 3  # 2 Bedroom
        
        FLATS.append(Flat(
            id=flat_id,
            apartment_id=2,
            flat_type_id=flat_type_id,
            floor=floor,
            room_number=room_number
        ))
        flat_id += 1

# Metropolitan Suites - 20 flats (floors 1-5, 4 flats per floor)
for floor in range(1, 6):
    for room in range(1, 5):
        room_number = f"{floor}0{room}"
        # Distribute flat types: Studio(4), 1BR(8), 2BR(6), Penthouse(2)
        if flat_id <= 44:
            flat_type_id = 1  # Studio
        elif flat_id <= 52:
            flat_type_id = 2  # 1 Bedroom
        elif flat_id <= 58:
            flat_type_id = 3  # 2 Bedroom
        else:
            flat_type_id = 4  # Penthouse
        
        FLATS.append(Flat(
            id=flat_id,
            apartment_id=3,
            flat_type_id=flat_type_id,
            floor=floor,
            room_number=room_number
        ))
        flat_id += 1

def get_apartment_by_id(apartment_id: int):
    return next((apt for apt in APARTMENTS if apt.id == apartment_id), None)

def get_flat_type_by_id(flat_type_id: int):
    return next((ft for ft in FLAT_TYPES if ft.id == flat_type_id), None)

def get_flat_by_id(flat_id: int):
    return next((flat for flat in FLATS if flat.id == flat_id), None)

def get_flats_by_apartment(apartment_id: int):
    return [flat for flat in FLATS if flat.apartment_id == apartment_id]

def get_flats_by_type(flat_type_id: int):
    return [flat for flat in FLATS if flat.flat_type_id == flat_type_id]
