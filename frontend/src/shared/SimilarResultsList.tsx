import React from 'react'

type Item = { url: string; similarity: number }

export const SimilarResultsList: React.FC<{ items: Item[] }> = ({ items }) => {
  if (!items || items.length === 0) return null
  return (
    <div className="bg-white border rounded">
      <div className="p-4 border-b font-medium">Similar results from the web</div>
      <ul className="divide-y">
        {items.map((it) => (
          <li key={it.url} className="p-4 flex items-center justify-between">
            <a href={it.url} target="_blank" rel="noreferrer" className="text-blue-600 hover:underline break-all">
              {it.url}
            </a>
            <span className="text-sm text-gray-700">Similarity: {it.similarity}%</span>
          </li>
        ))}
      </ul>
    </div>
  )
}


