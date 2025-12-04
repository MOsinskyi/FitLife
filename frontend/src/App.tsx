import { useState, useEffect } from 'react'
import './App.css'

const API_BASE_URL = 'http://localhost:8000'

interface Member {
  id: string
  name: string
  phone: string
}

interface MemberInput {
  name: string
  phone: string
}

function App() {
  const [members, setMembers] = useState<Member[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [formData, setFormData] = useState<MemberInput>({ name: '', phone: '' })
  const [editingId, setEditingId] = useState<string | null>(null)

  // Fetch all members
  const fetchMembers = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${API_BASE_URL}/members`)
      if (!response.ok) throw new Error('Failed to fetch members')
      const data = await response.json()
      setMembers(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  // Add a new member
  const addMember = async () => {
    if (!formData.name || !formData.phone) {
      setError('Name and phone are required')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${API_BASE_URL}/members`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.msg || 'Failed to add member')
      }
      setFormData({ name: '', phone: '' })
      await fetchMembers()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  // Update a member
  const updateMember = async () => {
    if (!editingId || !formData.name || !formData.phone) {
      setError('Name and phone are required')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${API_BASE_URL}/members/${editingId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.msg || 'Failed to update member')
      }
      setFormData({ name: '', phone: '' })
      setEditingId(null)
      await fetchMembers()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  // Delete a member
  const deleteMember = async (id: string) => {
    if (!confirm('Are you sure you want to delete this member?')) return

    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${API_BASE_URL}/members/${id}`, {
        method: 'DELETE'
      })
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.msg || 'Failed to delete member')
      }
      await fetchMembers()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  // Start editing a member
  const startEdit = (member: Member) => {
    setEditingId(member.id)
    setFormData({ name: member.name, phone: member.phone })
  }

  // Cancel editing
  const cancelEdit = () => {
    setEditingId(null)
    setFormData({ name: '', phone: '' })
  }

  // Load members on component mount
  useEffect(() => {
    fetchMembers()
  }, [])

  return (
    <div className="app-container">
      <h1>FitLife Members Management</h1>

      {error && <div className="error-message">{error}</div>}

      <div className="form-container">
        <h2>{editingId ? 'Edit Member' : 'Add New Member'}</h2>
        <div className="form-group">
          <input
            type="text"
            placeholder="Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          />
          <input
            type="text"
            placeholder="Phone (e.g., +380501234567)"
            value={formData.phone}
            onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
          />
        </div>
        <div className="button-group">
          {editingId ? (
            <>
              <button onClick={updateMember} disabled={loading}>
                Update Member
              </button>
              <button onClick={cancelEdit} disabled={loading} className="cancel-btn">
                Cancel
              </button>
            </>
          ) : (
            <button onClick={addMember} disabled={loading}>
              Add Member
            </button>
          )}
        </div>
      </div>

      <div className="table-container">
        <h2>Members List</h2>
        <button onClick={fetchMembers} disabled={loading} className="refresh-btn">
          Refresh
        </button>
        {loading && <p>Loading...</p>}
        {members.length === 0 && !loading && <p>No members found</p>}
        {members.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Phone</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {members.map((member) => (
                <tr key={member.id}>
                  <td>{member.id}</td>
                  <td>{member.name}</td>
                  <td>{member.phone}</td>
                  <td>
                    <button onClick={() => startEdit(member)} disabled={loading}>
                      Edit
                    </button>
                    <button
                      onClick={() => deleteMember(member.id)}
                      disabled={loading}
                      className="delete-btn"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default App
