import { api } from './config'
import { Itinerary } from './types'

export const userApi = {
  getItineraries: (userId: number) =>
    api.get<{ itineraries: Itinerary[] }>(
      `/agencies/users/${userId}/itineraries`
    ),
}
