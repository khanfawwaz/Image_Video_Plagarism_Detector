import React from 'react'

type Props = {
  metadata: Record<string, any>
  flags: Record<string, any>
}

export const MetadataTable: React.FC<Props> = ({ metadata, flags }) => {
  return (
    <div className="bg-white border rounded">
      <div className="p-4 border-b font-medium">Metadata & Edit Detection</div>
      <div className="p-4 grid md:grid-cols-2 gap-6">
        <div>
          <div className="font-semibold mb-2">Metadata</div>
          <table className="w-full text-sm">
            <tbody>
              {Object.entries(metadata || {}).map(([k, v]) => (
                <tr key={k} className="border-t">
                  <td className="py-2 pr-4 text-gray-600 w-40">{k}</td>
                  <td className="py-2">{String(v)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div>
          <div className="font-semibold mb-2">Edit Detection</div>
          <table className="w-full text-sm">
            <tbody>
              {Object.entries(flags || {}).map(([k, v]) => (
                <tr key={k} className="border-t">
                  <td className="py-2 pr-4 text-gray-600 w-56">{k}</td>
                  <td className="py-2">{Array.isArray(v) ? v.join(', ') : String(v)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}


