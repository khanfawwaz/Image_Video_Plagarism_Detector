import React from 'react'
import { useLocation, Link } from 'react-router-dom'
import { Layout } from '../shared/Layout'
import { ScoreCard } from '../shared/ScoreCard'
import { MetadataTable } from '../shared/MetadataTable'
import { SimilarResultsList } from '../shared/SimilarResultsList'

export const ResultsPage: React.FC = () => {
  const { state } = useLocation() as any
  const report = state?.report

  return (
    <Layout>
      <div className="max-w-4xl mx-auto py-10">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-semibold">Analysis Results</h1>
          <Link to="/" className="text-blue-600 hover:underline">New analysis</Link>
        </div>
        {!report ? (
          <p>No report found. Please upload a file first.</p>
        ) : (
          <div className="space-y-6">
            <ScoreCard score={report.ai_report.plagiarism_score} />
            <MetadataTable metadata={report.ai_report.metadata} flags={report.ai_report.edit_detection} />
            <SimilarResultsList items={report.reverse_search} />
            <div>
              <button className="px-4 py-2 bg-gray-900 text-white rounded">Prove Ownership (soon)</button>
            </div>
          </div>
        )}
      </div>
    </Layout>
  )
}


