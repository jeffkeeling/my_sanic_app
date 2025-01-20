import { Itinerary } from '@/services/api/types'

interface ItinerarySelectProps {
  itineraries: Itinerary[]
  value: string
  onChange: (itineraryId: string) => void
  isLoading: boolean
}

export function ItinerarySelect({
  itineraries,
  value,
  onChange,
  isLoading,
}: ItinerarySelectProps) {
  return (
    <div>
      <label className="block text-sm font-medium mb-1">Itinerary</label>
      <select
        className="w-full p-2 border rounded"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={isLoading}
      >
        <option value="">Select an itinerary</option>
        {itineraries.map((itinerary) => (
          <option key={itinerary.id} value={itinerary.id}>
            {itinerary.tour_name} ({itinerary.date_start} to{' '}
            {itinerary.date_end})
          </option>
        ))}
      </select>
    </div>
  )
}
