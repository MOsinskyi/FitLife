import type {
  LoginRequest,
  LoginResponse,
  MemberRegisterRequest,
  CoachRegisterRequest,
  User,
  Coach,
  ApiError,
  Gallery,
  Specialization,
  TrainingSession,
  Pass,
} from '../types'

const API_BASE_URL = import.meta.env.VITE_API_URL || '//api.fitlife.space/api/v1'

class ApiClient {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('access_token')
    return {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    }
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const error: ApiError = await response.json()
      throw new Error(error.detail || `HTTP error ${response.status}`)
    }
    return response.json()
  }

  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const formData = new URLSearchParams()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    })

    const data = await this.handleResponse<LoginResponse>(response)
    localStorage.setItem('access_token', data.access_token)
    return data
  }

  async registerMember(data: MemberRegisterRequest): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/members/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })

    return this.handleResponse<User>(response)
  }

  async registerCoach(data: CoachRegisterRequest): Promise<Coach> {
    const response = await fetch(`${API_BASE_URL}/coaches/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })

    return this.handleResponse<Coach>(response)
  }

  async getCurrentUser(): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      headers: this.getAuthHeaders(),
    })

    return this.handleResponse<User>(response)
  }

  async getCoaches(): Promise<Coach[]> {
    const response = await fetch(`${API_BASE_URL}/coaches`, {
      headers: this.getAuthHeaders(),
    })

    return this.handleResponse<Coach[]>(response)
  }

  async getGallery(): Promise<Gallery[]> {
    const response = await fetch(`${API_BASE_URL}/gallery`, {
      headers: this.getAuthHeaders(),
    })

    return this.handleResponse<Gallery[]>(response)
  }

  async getTrainingSessions(): Promise<TrainingSession[]> {
    const response = await fetch(`${API_BASE_URL}/training-sessions`, {
      headers: this.getAuthHeaders(),
    })

    return this.handleResponse<TrainingSession[]>(response)
  }

  async getSpecializations(): Promise<Specialization[]> {
    const response = await fetch(`${API_BASE_URL}/specializations`, {
      headers: this.getAuthHeaders(),
    })

    return this.handleResponse<Specialization[]>(response)
  }

  async getPasses(): Promise<Pass[]> {
    const response = await fetch(`${API_BASE_URL}/passes`, {
      headers: this.getAuthHeaders(),
    })

    return this.handleResponse<Pass[]>(response)
  }

  async bookSession(sessionId: string, memberIds: string[]): Promise<TrainingSession> {
    const response = await fetch(`${API_BASE_URL}/training-sessions/${sessionId}/participants`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(memberIds),
    })

    return this.handleResponse<TrainingSession>(response)
  }

  async cancelSession(sessionId: string, memberId: string): Promise<TrainingSession> {
    const response = await fetch(`${API_BASE_URL}/training-sessions/${sessionId}/participants/${memberId}`, {
      method: 'DELETE',
      headers: this.getAuthHeaders(),
    })

    return this.handleResponse<TrainingSession>(response)
  }

  logout(): void {
    localStorage.removeItem('access_token')
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token')
  }
}

export const apiClient = new ApiClient()
