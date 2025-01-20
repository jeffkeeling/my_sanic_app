export interface Agency {
  id: number
  name: string
  phone: string
  address: string
  logo: string
}

export interface User {
  id: number
  name: string
  email: string
  travel_agency_id: number
}

export interface Itinerary {
  id: number
  tour_name: string
  date_start: string
  date_end: string
  user_id: number
}

export interface Trip {
  id: number
  date_start: string
  date_end: string
  location_start: string
  location_end: string
  mode: string
  transporter: string
  itinerary_id: number
}

export interface Lodging {
  id: number
  date_start: string
  date_end: string
  name: string
  address: string
  phone: string
  room_count: number
  itinerary_id: number
}
