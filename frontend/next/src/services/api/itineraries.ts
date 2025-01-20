import { api } from './config'
import { Trip, Lodging } from './types'

export interface ItineraryDetails {
  itinerary: {
    id: number
    tour_name: string
    date_start: string
    date_end: string
  }
  trips: Trip[]
  lodgings: Lodging[]
}

export const itineraryApi = {
  getDetails: (itineraryId: number) =>
    api.get<ItineraryDetails>(`/agencies/itineraries/${itineraryId}/details`),
}
