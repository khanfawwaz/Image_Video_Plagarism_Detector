import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import './index.css'
import { UploadPage } from './pages/UploadPage'
import { ResultsPage } from './pages/ResultsPage'

const router = createBrowserRouter(
  [
    { path: '/', element: <UploadPage /> },
    { path: '/results', element: <ResultsPage /> },
  ],
  {
    future: {
      v7_startTransition: true,
    },
  },
)

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)


