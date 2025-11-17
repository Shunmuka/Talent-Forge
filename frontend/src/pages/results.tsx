import { useState, useEffect } from "react";
import { useRouter } from "next/router";
import { rewrite, RewriteRequest, AnalyzeResponse } from "../lib/api";

export default function ResultsPage() {
  const router = useRouter();
  const [analysisData, setAnalysisData] = useState<AnalyzeResponse | null>(null);
  const [selectedBullet, setSelectedBullet] = useState<string | null>(null);
  const [rewriteResult, setRewriteResult] = useState<{
    original: string;
    revised: string;
    rationale: string;
  } | null>(null);
  const [rewriteLoading, setRewriteLoading] = useState(false);
  const [rewriteError, setRewriteError] = useState<string | null>(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    const dataParam = router.query.data as string;
    if (dataParam) {
      try {
        const parsed = JSON.parse(dataParam) as AnalyzeResponse;
        setAnalysisData(parsed);
      } catch (err) {
        console.error("Error parsing analysis data:", err);
      }
    }
  }, [router.query]);

  const handleRewrite = async (bullet: string) => {
    setSelectedBullet(bullet);
    setRewriteLoading(true);
    setRewriteError(null);
    setShowModal(true);

    try {
      const request: RewriteRequest = {
        original: bullet,
        context: analysisData
          ? `Job Description: ${router.query.jd || ""}`
          : undefined,
      };

      const result = await rewrite(request);
      setRewriteResult(result);
    } catch (err) {
      setRewriteError(err instanceof Error ? err.message : "Rewrite failed");
    } finally {
      setRewriteLoading(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    // Could add a toast notification here
  };

  if (!analysisData) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 mb-4">No analysis data found.</p>
          <button
            onClick={() => router.push("/")}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          >
            Start New Analysis
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-6">
          <button
            onClick={() => router.push("/")}
            className="text-blue-600 hover:text-blue-800 mb-4"
          >
            ← Back to Analysis
          </button>
          <h1 className="text-3xl font-bold text-gray-900">Analysis Results</h1>
        </div>

        {/* Score Card */}
        <div className="bg-white shadow-lg rounded-lg p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            Match Score
          </h2>
          <div className="flex items-center">
            <div className="text-6xl font-bold text-blue-600 mr-4">
              {analysisData.score}
            </div>
            <div className="flex-1">
              <div className="w-full bg-gray-200 rounded-full h-4">
                <div
                  className="bg-blue-600 h-4 rounded-full"
                  style={{ width: `${analysisData.score}%` }}
                ></div>
              </div>
              <p className="text-sm text-gray-600 mt-2">
                Out of 100 - Higher is better
              </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Gaps Section */}
          <div className="bg-white shadow-lg rounded-lg p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
              Skill Gaps ({analysisData.gaps.length})
            </h2>
            <ul className="space-y-3">
              {analysisData.gaps.map((gap, idx) => (
                <li key={idx} className="border-l-4 border-red-500 pl-4">
                  <h3 className="font-medium text-gray-900">{gap.skill}</h3>
                  <p className="text-sm text-gray-600">{gap.reason}</p>
                </li>
              ))}
            </ul>
          </div>

          {/* Evidence Section */}
          <div className="bg-white shadow-lg rounded-lg p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
              Evidence ({analysisData.evidence.length})
            </h2>
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {analysisData.evidence.map((evidence, idx) => (
                <div key={idx} className="border-b pb-4 last:border-0">
                  <p className="text-sm text-gray-700 mb-2">
                    <span className="font-medium">Resume:</span>{" "}
                    {evidence.resumeText}
                  </p>
                  <p className="text-sm text-gray-700">
                    <span className="font-medium">JD:</span> {evidence.jdText}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Bullets Section */}
        <div className="bg-white shadow-lg rounded-lg p-6 mt-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">
            Resume Bullets ({analysisData.bullets.length})
          </h2>
          <ul className="space-y-3">
            {analysisData.bullets.map((bullet, idx) => (
              <li
                key={idx}
                className="flex items-start justify-between p-3 bg-gray-50 rounded-md"
              >
                <span className="flex-1 text-gray-700">{bullet}</span>
                <button
                  onClick={() => handleRewrite(bullet)}
                  className="ml-4 bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  Rewrite
                </button>
              </li>
            ))}
          </ul>
        </div>

        {/* Rewrite Modal */}
        {showModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg max-w-2xl w-full p-6 max-h-[90vh] overflow-y-auto">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold text-gray-900">
                  Rewrite Bullet
                </h2>
                <button
                  onClick={() => {
                    setShowModal(false);
                    setRewriteResult(null);
                    setRewriteError(null);
                  }}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>

              {rewriteLoading ? (
                <div className="text-center py-8">
                  <p className="text-gray-600">Rewriting bullet...</p>
                </div>
              ) : rewriteError ? (
                <div className="p-4 bg-red-50 border border-red-200 rounded-md">
                  <p className="text-red-800">{rewriteError}</p>
                </div>
              ) : rewriteResult ? (
                <div className="space-y-4">
                  <div>
                    <h3 className="font-medium text-gray-700 mb-2">
                      Original
                    </h3>
                    <p className="p-3 bg-gray-50 rounded-md text-gray-800">
                      {rewriteResult.original}
                    </p>
                  </div>

                  <div>
                    <h3 className="font-medium text-gray-700 mb-2">Revised</h3>
                    <div className="p-3 bg-green-50 border border-green-200 rounded-md">
                      <p className="text-gray-800 mb-2">
                        {rewriteResult.revised}
                      </p>
                      <button
                        onClick={() => copyToClipboard(rewriteResult.revised)}
                        className="text-sm text-blue-600 hover:text-blue-800"
                      >
                        Copy to clipboard
                      </button>
                    </div>
                  </div>

                  <div>
                    <h3 className="font-medium text-gray-700 mb-2">
                      Rationale
                    </h3>
                    <p className="p-3 bg-blue-50 rounded-md text-gray-700 text-sm">
                      {rewriteResult.rationale}
                    </p>
                  </div>
                </div>
              ) : null}

              <div className="mt-6 flex justify-end">
                <button
                  onClick={() => {
                    setShowModal(false);
                    setRewriteResult(null);
                    setRewriteError(null);
                  }}
                  className="bg-gray-200 text-gray-800 px-4 py-2 rounded-md hover:bg-gray-300"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
