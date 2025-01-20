import { useEffect, useState, ChangeEvent } from 'react'
import { agencyApi } from '@/services/api/agencies'
import { userApi } from '@/services/api/users'
import { itineraryApi } from '@/services/api/itineraries'
import { AgencySelect } from './selectors/AgencySelect'
import { UserSelect } from './selectors/UserSelect'
import { ItinerarySelect } from './selectors/ItinerarySelect'
import { TripsTable } from './tables/TripsTable'
import { LodgingsTable } from './tables/LodgingsTable'
import type { Agency, User, Itinerary } from '@/services/api/types'
import { ItineraryDetails } from '@/services/api/itineraries'
import axios from 'axios'

export default function ItineraryInterface() {
  // State for selected items
  const [selectedAgency, setSelectedAgency] = useState('')
  const [selectedUser, setSelectedUser] = useState('')
  const [selectedItinerary, setSelectedItinerary] = useState('')

  // State for data
  const [agencies, setAgencies] = useState<Agency[]>([])
  const [users, setUsers] = useState<User[]>([])
  const [itineraries, setItineraries] = useState<Itinerary[]>([])
  const [itineraryDetails, setItineraryDetails] =
    useState<ItineraryDetails | null>(null)

  // State for loading states
  const [loading, setLoading] = useState({
    agencies: false,
    users: false,
    itineraries: false,
    details: false,
  })

  // Fetch agencies on component mount
  useEffect(() => {
    const fetchAgencies = async () => {
      setLoading((prev) => ({ ...prev, agencies: true }))
      try {
        await agencyApi.getAll().then((response) => setAgencies(response.data))
      } catch (error) {
        console.error('Error fetching agencies:', error)
      }
      setLoading((prev) => ({ ...prev, agencies: false }))
    }

    fetchAgencies()
  }, [])

  const fetchUsers = async (agencyId: number) => {
    setLoading((prev) => ({ ...prev, users: true }))
    try {
      await agencyApi
        .getUsers(agencyId)
        .then((response) => setUsers(response.data.users))
    } catch (error) {
      console.error('Error fetching usrs:', error)
    }
    setLoading((prev) => ({ ...prev, users: false }))
  }

  const fetchItineraries = async (userId: number) => {
    setLoading((prev) => ({ ...prev, itineraries: true }))
    try {
      await userApi
        .getItineraries(userId)
        .then((response) => setItineraries(response.data.itineraries))
    } catch (error) {
      console.error('Error fetching usrs:', error)
    }
    setLoading((prev) => ({ ...prev, itineraries: false }))
  }

  const fetchItineraryDetails = async (itineraryId: number) => {
    setLoading((prev) => ({ ...prev, details: true }))
    try {
      await itineraryApi
        .getDetails(itineraryId)
        .then((response) => setItineraryDetails(response.data))
    } catch (error) {
      console.error('Error fetching usrs:', error)
    }
    setLoading((prev) => ({ ...prev, details: false }))
  }

  // Handle selection changes
  const handleAgencyChange = (value: string) => {
    setSelectedAgency(value)
    setSelectedUser('')
    setSelectedItinerary('')
    setItineraryDetails(null)
    fetchUsers(parseInt(value))
  }

  const handleUserChange = (value: string) => {
    setSelectedUser(value)
    setSelectedItinerary('')
    setItineraryDetails(null)
    fetchItineraries(parseInt(value))
  }

  const handleItineraryChange = (value: string) => {
    setSelectedItinerary(value)
    fetchItineraryDetails(parseInt(value))
  }

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Itinerary Dashboard</h1>

      <div className="space-y-4 mb-8">
        <AgencySelect
          agencies={agencies}
          value={selectedAgency}
          onChange={handleAgencyChange}
          isLoading={loading.agencies}
        />

        {selectedAgency && (
          <UserSelect
            users={users}
            value={selectedUser}
            onChange={handleUserChange}
            isLoading={loading.users}
          />
        )}

        {selectedUser && (
          <ItinerarySelect
            itineraries={itineraries}
            value={selectedItinerary}
            onChange={handleItineraryChange}
            isLoading={loading.itineraries}
          />
        )}
      </div>

      {selectedItinerary && itineraryDetails && (
        <div className="space-y-6">
          <h2 className="text-xl font-semibold">
            {itineraryDetails.itinerary.tour_name}
          </h2>

          <TripsTable trips={itineraryDetails.trips} />
          <LodgingsTable lodgings={itineraryDetails.lodgings} />
        </div>
      )}

      {/* Loading indicator */}
      {(loading.agencies ||
        loading.users ||
        loading.itineraries ||
        loading.details) && (
        <div className="fixed bottom-4 right-4 bg-blue-500 text-white px-4 py-2 rounded shadow">
          Loading...
        </div>
      )}
    </div>
  )
}
