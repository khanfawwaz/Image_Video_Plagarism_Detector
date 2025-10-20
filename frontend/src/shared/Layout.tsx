import React from 'react'

export const Layout: React.FC<React.PropsWithChildren> = ({ children }) => {
  return (
    <div className="min-h-screen">
      <header className="border-b bg-white">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="font-semibold">AI Visual Plagiarism Detector</div>
        </div>
      </header>
      <main className="px-4">{children}</main>
    </div>
  )
}


