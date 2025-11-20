import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'EvoForge - Self-Evolving AI Agent Platform',
  description: 'Build agents that evolve themselves through autonomous learning',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50">{children}</body>
    </html>
  )
}
