'use client'

import { useState, useEffect, FormEvent } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Trash2 } from 'lucide-react'

// Using environment variable for API URL
// const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

type Itinerary = {
  tour_name: string
  date_start: string
  date_end: string
  id: string
}

export default function CreateItinerary() {
  const [itineraries, setItineraries] = useState([])
  const [newItinerary, setNewItinerary] = useState({
    tour_name: '',
    date_start: '',
    date_end: '',
  })
  const [error, setError] = useState('')

  const fetchItineraries = async () => {
    try {
      const response = await fetch(`api/itineraries`)
      const data = await response.json()
      console.log('data', data)
      setItineraries(data.data)
    } catch (err) {
      setError('Failed to fetch users')
    }
  }

  useEffect(() => {
    fetchItineraries()
  }, [])

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    try {
      const response = await fetch(`api/itineraries`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newItinerary),
      })

      if (!response.ok) {
        throw new Error('Failed to create user')
      }

      await fetchItineraries()
      setNewItinerary({ tour_name: '', date_start: '', date_end: '' })
      setError('')
    } catch (err) {
      setError('Failed to create user')
    }
  }

  const handleDelete = async (itineraryId: string) => {
    try {
      const response = await fetch(`api/itineraries/${itineraryId}`, {
        method: 'DELETE',
      })

      if (!response.ok) {
        throw new Error('Failed to delete user')
      }

      await fetchItineraries()
    } catch (err) {
      setError('Failed to delete user')
    }
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <Card>
        <CardHeader>
          <CardTitle>Itineraries</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4 mb-6">
            <div className="flex gap-4">
              <Input
                type="text"
                placeholder="Name"
                value={newItinerary.tour_name}
                onChange={(e) =>
                  setNewItinerary({
                    ...newItinerary,
                    tour_name: e.target.value,
                  })
                }
                className="flex-1"
              />
              <Input
                type="date"
                placeholder=""
                value={newItinerary.date_start}
                onChange={(e) =>
                  setNewItinerary({
                    ...newItinerary,
                    date_start: e.target.value,
                  })
                }
                className="flex-1"
              />
              <Input
                type="date"
                placeholder=""
                value={newItinerary.date_end}
                onChange={(e) =>
                  setNewItinerary({
                    ...newItinerary,
                    date_end: e.target.value,
                  })
                }
                className="flex-1"
              />
              <Button type="submit">Add Itinerary</Button>
            </div>
            {error && <p className="text-red-500">{error}</p>}
          </form>

          <div className="space-y-2">
            {itineraries.map((itinerary: Itinerary) => (
              <div
                key={itinerary.id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded"
              >
                <div>
                  <p className="font-medium">{itinerary.tour_name}</p>
                </div>
                <Button
                  variant="destructive"
                  size="icon"
                  onClick={() => handleDelete(itinerary.id)}
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
