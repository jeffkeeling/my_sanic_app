import { Lodging } from '@/services/api/types'

interface LodgingsTableProps {
  lodgings: Lodging[]
}

export function LodgingsTable({ lodgings }: LodgingsTableProps) {
  return (
    <div>
      <h3 className="text-lg font-medium mb-2">Lodgings</h3>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Dates
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Name
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Address
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Phone
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Rooms
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {lodgings.map((lodging) => (
              <tr key={lodging.id}>
                <td className="px-6 py-4 whitespace-nowrap">
                  {lodging.date_start} - {lodging.date_end}
                </td>
                <td className="px-6 py-4">{lodging.name}</td>
                <td className="px-6 py-4">{lodging.address}</td>
                <td className="px-6 py-4">{lodging.phone}</td>
                <td className="px-6 py-4">{lodging.room_count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
