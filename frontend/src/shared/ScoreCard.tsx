import React from 'react'

export const ScoreCard: React.FC<{ score: number }> = ({ score }) => {
  const color = score >= 75 ? 'bg-red-100 text-red-700' : score >= 40 ? 'bg-yellow-100 text-yellow-700' : 'bg-green-100 text-green-700'
  return (
    <div className={`p-4 rounded ${color}`}>
      <div className="text-sm uppercase">Plagiarism Score</div>
      <div className="text-3xl font-bold">{score}%</div>
    </div>
  )
}


