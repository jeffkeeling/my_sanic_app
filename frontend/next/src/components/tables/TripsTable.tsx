import { Trip } from '@/services/api/types'

interface TripsTableProps {
  trips: Trip[]
}

export function TripsTable({ trips }: TripsTableProps) {
  return (
    <div>
      <h3 className="text-lg font-medium mb-2">Trips</h3>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Date
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                From
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                To
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Mode
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Transporter
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {trips.map((trip) => (
              <tr key={trip.id}>
                <td className="px-6 py-4 whitespace-nowrap">
                  {trip.date_start}
                </td>
                <td className="px-6 py-4">{trip.location_start}</td>
                <td className="px-6 py-4">{trip.location_end}</td>
                <td className="px-6 py-4">{trip.mode}</td>
                <td className="px-6 py-4">{trip.transporter}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
