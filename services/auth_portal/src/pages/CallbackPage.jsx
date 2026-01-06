import { useAuth0 } from '@auth0/auth0-react'
import { useEffect, useState } from 'react'

export default function CallbackPage() {
  const {
    isAuthenticated,
    isLoading,
    error,
    getAccessTokenSilently,
  } = useAuth0()

  const [status, setStatus] = useState('Processing authentication...')

  useEffect(() => {
    const handleCallback = async () => {
      try {
        if (isLoading) {
          setStatus('Authenticating...')
          return
        }

        if (error) {
          console.error('Auth0 error:', error)
          setStatus(`Error: ${error.message}`)
          return
        }

        if (isAuthenticated) {
          setStatus('Getting access token...')

          // Get access token
          const token = await getAccessTokenSilently()

          // Call auth_gateway_service callback to sync user
          setStatus('Syncing user data...')

          const authGatewayUrl = import.meta.env.VITE_AUTH_GATEWAY_URL || 'http://localhost:8012'
          const response = await fetch(`${authGatewayUrl}/auth/callback`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`,
            },
            credentials: 'include',
          })

          if (!response.ok) {
            throw new Error(`Callback failed: ${response.statusText}`)
          }

          const data = await response.json()
          console.log('User synced:', data)

          setStatus('Redirecting to dashboard...')

          // Redirect to dashboard
          setTimeout(() => {
            const dashboardUrl = import.meta.env.VITE_DASHBOARD_URL || 'http://localhost:8022'
            window.location.href = dashboardUrl
          }, 1000)
        }
      } catch (err) {
        console.error('Callback error:', err)
        setStatus(`Error: ${err.message}`)
      }
    }

    handleCallback()
  }, [isAuthenticated, isLoading, error, getAccessTokenSilently])

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-600 to-primary-800 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-xl p-8 max-w-md text-center">
        {/* Loading Spinner */}
        <div className="mb-6">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-primary-600 mx-auto"></div>
        </div>

        {/* Status Message */}
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          {error ? 'Authentication Failed' : 'Completing Sign In'}
        </h2>
        <p className={`text-lg ${error ? 'text-red-600' : 'text-gray-600'}`}>
          {status}
        </p>

        {error && (
          <button
            onClick={() => window.location.href = '/'}
            className="mt-6 bg-primary-600 text-white py-2 px-6 rounded-lg hover:bg-primary-700 transition-colors"
          >
            Back to Login
          </button>
        )}

        {/* Progress Steps */}
        {!error && (
          <div className="mt-8 space-y-2">
            <div className="flex items-center text-sm text-gray-600">
              <svg className="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span>Authenticated with Auth0</span>
            </div>
            <div className={`flex items-center text-sm ${status.includes('Syncing') ? 'text-primary-600' : 'text-gray-400'}`}>
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span>Syncing user profile</span>
            </div>
            <div className={`flex items-center text-sm ${status.includes('Redirecting') ? 'text-primary-600' : 'text-gray-400'}`}>
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span>Redirecting to dashboard</span>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
