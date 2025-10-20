import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { FileUpload } from '../shared/FileUpload'
import { Layout } from '../shared/Layout'
import axios from 'axios'

export const UploadPage: React.FC = () => {
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  const handleSubmit = async (file: File) => {
    setError(null)
    setUploading(true)
    try {
      const form = new FormData()
      form.append('media', file)
      const baseUrl = import.meta.env.VITE_API_BASE_URL
      const url = baseUrl ? `${baseUrl}/analyze` : `/api/analyze`
      const res = await axios.post(url, form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      navigate('/results', { state: res.data })
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Upload failed')
    } finally {
      setUploading(false)
    }
  }

  return (
    <Layout>
      <div className="max-w-2xl mx-auto py-10">
        <h1 className="text-2xl font-semibold mb-6">AI Visual Plagiarism Detector</h1>
        <FileUpload onSubmit={handleSubmit} disabled={uploading} />
        {uploading && <p className="mt-4 text-sm text-gray-600">Analyzing...</p>}
        {error && <p className="mt-4 text-sm text-red-600">{error}</p>}
      </div>
    </Layout>
  )
}


