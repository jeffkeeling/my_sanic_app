import { Agency } from '@/services/api/types'

interface AgencySelectProps {
  agencies: Agency[]
  value: string
  onChange: (agencyId: string) => void
  isLoading: boolean
}

export function AgencySelect({
  agencies,
  value,
  onChange,
  isLoading,
}: AgencySelectProps) {
  return (
    <div>
      <label className="block text-sm font-medium mb-1">Travel Agency</label>
      <select
        className="w-full p-2 border rounded"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={isLoading}
      >
        <option value="">Select an agency</option>
        {agencies.map((agency) => (
          <option key={agency.id} value={agency.id}>
            {agency.name}
          </option>
        ))}
      </select>
    </div>
  )
}
