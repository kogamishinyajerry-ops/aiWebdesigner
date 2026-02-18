'use client'

import { Navbar } from './navbar'
import { Sidebar } from './sidebar'
import { cn } from '../../lib/utils'

interface AppLayoutProps {
  children: React.ReactNode
  showSidebar?: boolean
  className?: string
}

export function AppLayout({
  children,
  showSidebar = true,
  className,
}: AppLayoutProps) {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <div className="flex">
        {showSidebar && <Sidebar />}
        <main
          className={cn(
            'flex-1 overflow-hidden',
            showSidebar ? 'ml-0' : '',
            className
          )}
        >
          <div className="container mx-auto p-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}
