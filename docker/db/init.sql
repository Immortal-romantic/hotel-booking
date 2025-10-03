CREATE TABLE IF NOT EXISTS room (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    price_per_night DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_room_price ON room (price_per_night);
CREATE INDEX idx_room_created_at ON room (created_at);

CREATE TABLE IF NOT EXISTS booking (
    id SERIAL PRIMARY KEY,
    room_id INTEGER NOT NULL REFERENCES room(id) ON DELETE CASCADE,
    date_start DATE NOT NULL,
    date_end DATE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CHECK (date_end > date_start)
);

CREATE INDEX idx_booking_room_id ON booking (room_id);
CREATE INDEX idx_booking_date_start ON booking (date_start);
