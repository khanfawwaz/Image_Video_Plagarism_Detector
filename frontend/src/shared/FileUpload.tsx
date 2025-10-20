import React, { useRef, useState } from 'react'

type Props = {
  onSubmit: (file: File) => void
  disabled?: boolean
}

export const FileUpload: React.FC<Props> = ({ onSubmit, disabled }) => {
  const inputRef = useRef<HTMLInputElement | null>(null)
  const [file, setFile] = useState<File | null>(null)
  const [dragOver, setDragOver] = useState(false)

  const handlePick = () => inputRef.current?.click()
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]
    if (f) setFile(f)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setDragOver(false)
    const f = e.dataTransfer.files?.[0]
    if (f) setFile(f)
  }

  return (
    <div className="space-y-4">
      <div
        onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded p-8 text-center ${dragOver ? 'border-blue-400 bg-blue-50' : 'border-gray-300'}`}
      >
        <p className="mb-2">Drag & drop an image or video here</p>
        <p className="text-sm text-gray-600">or</p>
        <button
          className="mt-2 px-4 py-2 bg-gray-900 text-white rounded"
          onClick={handlePick}
          disabled={disabled}
        >
          Choose file
        </button>
        <input ref={inputRef} type="file" className="hidden" onChange={handleChange} accept="image/*,video/*" />
      </div>
      {file && (
        <div className="flex items-center justify-between">
          <div>
            <div className="font-medium">{file.name}</div>
            <div className="text-xs text-gray-600">{Math.round(file.size / 1024)} KB</div>
          </div>
          <button
            className="px-4 py-2 bg-blue-600 text-white rounded"
            onClick={() => onSubmit(file)}
            disabled={disabled}
          >
            Analyze
          </button>
        </div>
      )}
    </div>
  )
}


