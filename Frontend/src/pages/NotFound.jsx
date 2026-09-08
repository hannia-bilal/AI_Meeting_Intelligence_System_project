import { Link } from 'react-router-dom'
import { Compass } from 'lucide-react'

export default function NotFound() {
  return (
    <div className="min-h-screen bg-paper flex items-center justify-center px-4">
      <div className="text-center max-w-sm">
        <div className="w-12 h-12 rounded-full bg-walnut-50 text-walnut-500 flex items-center justify-center mx-auto mb-4">
          <Compass size={22} />
        </div>
        <h1 className="text-xl font-semibold">Page not found</h1>
        <p className="text-sm text-ink-soft mt-2">
          The page you're looking for doesn't exist or may have moved.
        </p>
        <Link
          to="/dashboard"
          className="inline-block mt-6 text-sm font-medium text-walnut-600 hover:underline"
        >
          Back to dashboard
        </Link>
      </div>
    </div>
  )
}
