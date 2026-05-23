export const UserRole = {
  MEMBER: 'member',
  COACH: 'coach',
  ADMIN: 'admin',
} as const

export type UserRole = typeof UserRole[keyof typeof UserRole]

export interface Specialization {
  id: string
  name: string
  emoji: string
  created_at: string
  updated_at: string
}

export interface User {
  id: string
  first_name: string
  last_name: string
  phone_number: string
  email: string | null
  role: UserRole
  created_at: string
  updated_at: string
}

export interface Member extends User {
  role: 'member'
}

export interface Coach extends User {
  role: 'coach'
  specializations: Specialization[]
  experience: number
  experience_label: string
  image_url: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
}

export interface MemberRegisterRequest {
  first_name: string
  last_name: string
  phone_number: string
  email: string | null
  password: string
}

export interface CoachRegisterRequest extends MemberRegisterRequest {
  specialization_ids: string[]
  experience: number
  experience_label: string
}

export interface ApiError {
  detail: string
}

export interface Gallery {
  id: string
  image_url: string
  title: string
  description: string
  display_order: number
  created_at: string
  updated_at: string
}

export interface Participant {
  joined_at: string
  member: User
}

export interface TrainingSession {
  id: string
  title: string
  description: string
  start_time: string
  end_time: string
  status: string
  max_participants: number
  coach: Coach
  participants: Participant[]
}
