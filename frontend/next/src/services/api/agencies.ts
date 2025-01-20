import { api } from './config'
import { Agency, User } from './types'

export const agencyApi = {
  getAll: () => api.get<Agency[]>('/agencies'),
  getUsers: (agencyId: number) =>
    api.get<{ users: User[] }>(`/agencies/${agencyId}/users`),
}
