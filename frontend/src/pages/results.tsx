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
    // Show toast notification
    const toast = document.createElement("div");
    toast.className =
      "fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50";
    toast.textContent = "Copied to clipboard!";
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2000);
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return "from-green-500 to-emerald-600";
    if (score >= 60) return "from-blue-500 to-indigo-600";
    if (score >= 40) return "from-yellow-500 to-orange-500";
    return "from-red-500 to-pink-600";
  };

  const getScoreLabel = (score: number) => {
    if (score >= 80) return "Excellent Match";
    if (score >= 60) return "Good Match";
    if (score >= 40) return "Fair Match";
    return "Needs Improvement";
  };

  if (!analysisData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 flex items-center justify-center">
        <div className="text-center bg-white rounded-2xl shadow-xl p-12 max-w-md">
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg
              className="w-8 h-8 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            No Analysis Data
          </h2>
          <p className="text-gray-600 mb-6">
            Please analyze a resume first to see results.
          </p>
          <button
            onClick={() => router.push("/")}
            className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-3 rounded-lg font-semibold hover:shadow-lg transform hover:scale-105 transition-all"
          >
            Start New Analysis
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => router.push("/")}
              className="flex items-center text-gray-600 hover:text-gray-900 transition-colors"
            >
              <svg
                className="w-5 h-5 mr-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M10 19l-7-7m0 0l7-7m-7 7h18"
                />
              </svg>
              Back to Analysis
            </button>
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">TF</span>
              </div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                Talent Forge
              </h1>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        {/* Score Card */}
        <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-8 mb-8 overflow-hidden">
          <div className="flex flex-col md:flex-row items-center md:items-start justify-between">
            <div className="flex-1 mb-6 md:mb-0">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                Match Score
              </h2>
              <p className="text-gray-600">
                {getScoreLabel(analysisData.score)} - Your resume matches{" "}
                {analysisData.score}% of the job requirements
              </p>
            </div>
            <div className="flex items-center space-x-6">
              <div className="text-center">
                <div
                  className={`text-7xl font-bold bg-gradient-to-r ${getScoreColor(
                    analysisData.score
                  )} bg-clip-text text-transparent`}
                >
                  {analysisData.score}
                </div>
                <div className="text-sm text-gray-500 mt-1">out of 100</div>
              </div>
              <div className="w-32">
                <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
                  <div
                    className={`h-full bg-gradient-to-r ${getScoreColor(
                      analysisData.score
                    )} rounded-full transition-all duration-1000`}
                    style={{ width: `${analysisData.score}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Gaps Section */}
          <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-6">
            <div className="flex items-center mb-6">
              <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mr-4">
                <svg
                  className="w-6 h-6 text-red-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                </svg>
              </div>
              <div>
                <h2 className="text-xl font-bold text-gray-900">
                  Skill Gaps
                </h2>
                <p className="text-sm text-gray-500">
                  {analysisData.gaps.length} gaps identified
                </p>
              </div>
            </div>
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {analysisData.gaps.map((gap, idx) => (
                <div
                  key={idx}
                  className="border-l-4 border-red-500 pl-4 py-2 bg-red-50 rounded-r-lg"
                >
                  <h3 className="font-semibold text-gray-900 mb-1">
                    {gap.skill}
                  </h3>
                  <p className="text-sm text-gray-600">{gap.reason}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Evidence Section */}
          <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-6">
            <div className="flex items-center mb-6">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
                <svg
                  className="w-6 h-6 text-blue-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div>
                <h2 className="text-xl font-bold text-gray-900">Evidence</h2>
                <p className="text-sm text-gray-500">
                  {analysisData.evidence.length} matches found
                </p>
              </div>
            </div>
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {analysisData.evidence.map((evidence, idx) => (
                <div
                  key={idx}
                  className="border border-gray-200 rounded-lg p-4 bg-gray-50 hover:bg-gray-100 transition-colors"
                >
                  <div className="mb-2">
                    <span className="text-xs font-semibold text-blue-600 uppercase">
                      Resume
                    </span>
                    <p className="text-sm text-gray-700 mt-1">
                      {evidence.resumeText}
                    </p>
                  </div>
                  <div className="flex items-center my-2">
                    <div className="flex-1 border-t border-gray-300"></div>
                    <svg
                      className="w-4 h-4 text-gray-400 mx-2"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M13 7l5 5m0 0l-5 5m5-5H6"
                      />
                    </svg>
                    <div className="flex-1 border-t border-gray-300"></div>
                  </div>
                  <div>
                    <span className="text-xs font-semibold text-indigo-600 uppercase">
                      Job Description
                    </span>
                    <p className="text-sm text-gray-700 mt-1">
                      {evidence.jdText}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Bullets Section */}
        <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mr-4">
                <svg
                  className="w-6 h-6 text-purple-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                  />
                </svg>
              </div>
              <div>
                <h2 className="text-xl font-bold text-gray-900">
                  Resume Bullets
                </h2>
                <p className="text-sm text-gray-500">
                  {analysisData.bullets.length} bullets extracted
                </p>
              </div>
            </div>
          </div>
          <div className="space-y-3">
            {analysisData.bullets.length > 0 ? (
              analysisData.bullets.map((bullet, idx) => (
                <div
                  key={idx}
                  className="flex items-start justify-between p-4 bg-gradient-to-r from-gray-50 to-white rounded-lg border border-gray-200 hover:shadow-md transition-all"
                >
                  <span className="flex-1 text-gray-700 pr-4">{bullet}</span>
                  <button
                    onClick={() => handleRewrite(bullet)}
                    className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:shadow-lg transform hover:scale-105 transition-all flex items-center whitespace-nowrap"
                  >
                    <svg
                      className="w-4 h-4 mr-2"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                      />
                    </svg>
                    Rewrite
                  </button>
                </div>
              ))
            ) : (
              <div className="text-center py-8 text-gray-500">
                <p>No bullets extracted from resume text.</p>
                <p className="text-sm mt-2">
                  Try formatting your resume with bullet points (• or -)
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Rewrite Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 backdrop-blur-sm">
          <div className="bg-white rounded-2xl max-w-3xl w-full p-8 max-h-[90vh] overflow-y-auto shadow-2xl">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-3xl font-bold text-gray-900">
                Rewrite Bullet
              </h2>
              <button
                onClick={() => {
                  setShowModal(false);
                  setRewriteResult(null);
                  setRewriteError(null);
                }}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>

            {rewriteLoading ? (
              <div className="text-center py-12">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
                <p className="text-gray-600">Rewriting bullet with AI...</p>
              </div>
            ) : rewriteError ? (
              <div className="p-4 bg-red-50 border-l-4 border-red-500 rounded-r-lg">
                <p className="text-red-800">{rewriteError}</p>
              </div>
            ) : rewriteResult ? (
              <div className="space-y-6">
                <div>
                  <h3 className="font-semibold text-gray-700 mb-3 flex items-center">
                    <span className="w-2 h-2 bg-gray-400 rounded-full mr-2"></span>
                    Original
                  </h3>
                  <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                    <p className="text-gray-800">{rewriteResult.original}</p>
                  </div>
                </div>

                <div className="relative">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t border-gray-300"></div>
                  </div>
                  <div className="relative flex justify-center">
                    <span className="bg-white px-4 text-gray-500">
                      <svg
                        className="w-6 h-6"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M13 7l5 5m0 0l-5 5m5-5H6"
                        />
                      </svg>
                    </span>
                  </div>
                </div>

                <div>
                  <h3 className="font-semibold text-gray-700 mb-3 flex items-center">
                    <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                    Revised
                  </h3>
                  <div className="p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg border-2 border-green-200">
                    <p className="text-gray-800 mb-3 font-medium">
                      {rewriteResult.revised}
                    </p>
                    <button
                      onClick={() => copyToClipboard(rewriteResult.revised)}
                      className="text-sm text-green-700 hover:text-green-800 font-medium flex items-center"
                    >
                      <svg
                        className="w-4 h-4 mr-1"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
                        />
                      </svg>
                      Copy to clipboard
                    </button>
                  </div>
                </div>

                <div>
                  <h3 className="font-semibold text-gray-700 mb-3 flex items-center">
                    <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                    Rationale
                  </h3>
                  <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                    <p className="text-gray-700 text-sm leading-relaxed">
                      {rewriteResult.rationale}
                    </p>
                  </div>
                </div>
              </div>
            ) : null}

            <div className="mt-8 flex justify-end">
              <button
                onClick={() => {
                  setShowModal(false);
                  setRewriteResult(null);
                  setRewriteError(null);
                }}
                className="bg-gray-200 text-gray-800 px-6 py-2 rounded-lg font-medium hover:bg-gray-300 transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
