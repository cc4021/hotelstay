from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Optional

@dataclass
class Apartment:
    id: int
    name: str
    description: str
    address: str
    amenities: List[str]

@dataclass
class FlatType:
    id: int
    name: str
    description: str
    max_guests: int
    base_price: float
    features: List[str]

@dataclass
class Flat:
    id: int
    apartment_id: int
    flat_type_id: int
    floor: int
    room_number: str
    is_available: bool = True

@dataclass
class Booking:
    id: int
    flat_id: int
    guest_name: str
    guest_email: str
    guest_phone: str
    check_in: date
    check_out: date
    total_guests: int
    total_price: float
    booking_date: datetime
    status: str = "confirmed"  # confirmed, cancelled
    special_requests: str = ""

class BookingManager:
    def __init__(self):
        self.bookings: List[Booking] = []
        self.next_booking_id = 1
    
    def create_booking(self, flat_id: int, guest_name: str, guest_email: str, 
                      guest_phone: str, check_in: date, check_out: date, 
                      total_guests: int, total_price: float, special_requests: str = "") -> Booking:
        booking = Booking(
            id=self.next_booking_id,
            flat_id=flat_id,
            guest_name=guest_name,
            guest_email=guest_email,
            guest_phone=guest_phone,
            check_in=check_in,
            check_out=check_out,
            total_guests=total_guests,
            total_price=total_price,
            booking_date=datetime.now(),
            special_requests=special_requests
        )
        self.bookings.append(booking)
        self.next_booking_id += 1
        return booking
    
    def get_booking(self, booking_id: int) -> Optional[Booking]:
        return next((b for b in self.bookings if b.id == booking_id), None)
    
    def get_bookings_by_email(self, email: str) -> List[Booking]:
        return [b for b in self.bookings if b.guest_email == email and b.status == "confirmed"]
    
    def is_flat_available(self, flat_id: int, check_in: date, check_out: date) -> bool:
        for booking in self.bookings:
            if (booking.flat_id == flat_id and booking.status == "confirmed" and
                not (check_out <= booking.check_in or check_in >= booking.check_out)):
                return False
        return True
    
    def cancel_booking(self, booking_id: int) -> bool:
        booking = self.get_booking(booking_id)
        if booking:
            booking.status = "cancelled"
            return True
        return False

# Global booking manager instance
booking_manager = BookingManager()
