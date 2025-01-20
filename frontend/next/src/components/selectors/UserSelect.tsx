import { User } from '@/services/api/types'

interface UserSelectProps {
  users: User[]
  value: string
  onChange: (userId: string) => void
  isLoading: boolean
}

export function UserSelect({
  users,
  value,
  onChange,
  isLoading,
}: UserSelectProps) {
  return (
    <div>
      <label className="block text-sm font-medium mb-1">User</label>
      <select
        className="w-full p-2 border rounded"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={isLoading}
      >
        <option value="">Select a user</option>
        {users.map((user) => (
          <option key={user.id} value={user.id}>
            {user.name}
          </option>
        ))}
      </select>
    </div>
  )
}
