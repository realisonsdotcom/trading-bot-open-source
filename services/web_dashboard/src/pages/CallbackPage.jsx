import { useAuth0 } from '@auth0/auth0-react'
import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

export default function CallbackPage() {
  const { isAuthenticated, isLoading, error } = useAuth0()
  const navigate = useNavigate()

  useEffect(() => {
    if (!isLoading) {
      if (isAuthenticated) {
        // Redirect to dashboard after successful authentication
        navigate('/dashboard')
      } else if (error) {
        // Redirect to auth portal on error
        const authPortalUrl = import.meta.env.VITE_AUTH_PORTAL_URL || 'http://localhost:3000'
        window.location.href = authPortalUrl
      }
    }
  }, [isAuthenticated, isLoading, error, navigate])

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-primary-600 mx-auto mb-4"></div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          {error ? 'Authentication Failed' : 'Completing Sign In'}
        </h2>
        <p className="text-gray-600">
          {error ? error.message : 'Please wait while we complete your authentication...'}
        </p>
      </div>
    </div>
  )
}
