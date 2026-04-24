export const UserRole = {
  MEMBER: 'member',
  COACH: 'coach',
} as const

export type UserRole = typeof UserRole[keyof typeof UserRole]

export const Specialization = {
  YOGA: 'Yoga',
  CROSSFIT: 'CrossFit',
  AEROBICS: 'Aerobics',
  STRENGTH_TRAINING: 'Strength Training',
  CARDIO: 'Cardio',
  MEDITATION: 'Meditation',
} as const

export type Specialization = typeof Specialization[keyof typeof Specialization]

export const Emoji = {
  YOGA: '🧘',
  CROSSFIT: '🏋️',
  AEROBICS: '🤸',
  STRENGTH_TRAINING: '💪',
  CARDIO: '🏃',
  MEDITATION: '🪷',
} as const

export type Emoji = typeof Emoji[keyof typeof Emoji]

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
  specialization: Specialization
  emoji: Emoji
  experience: number
  experience_label: string
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
  specialization: Specialization
  emoji: Emoji
  experience: number
  experience_label: string
}

export interface ApiError {
  detail: string
}
