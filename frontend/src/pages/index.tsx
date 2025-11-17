import { useState } from "react";
import { useRouter } from "next/router";
import { analyze, analyzeWithFile, AnalyzeRequest } from "../lib/api";

type ResumeSource = "upload" | "paste";

export default function HomePage() {
  const router = useRouter();
  const [resumeSource, setResumeSource] = useState<ResumeSource>("paste");
  const [resumeText, setResumeText] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setResumeFile(file);
      setError(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (!jobDescription.trim()) {
        throw new Error("Job description is required");
      }

      let analyzeRequest: AnalyzeRequest;

      if (resumeSource === "upload" && resumeFile) {
        // Upload file
        const formData = new FormData();
        formData.append("resume_file", resumeFile);
        formData.append("job_description", jobDescription);

        const result = await analyzeWithFile(formData);
        router.push({
          pathname: "/results",
          query: { data: JSON.stringify(result) },
        });
      } else if (resumeSource === "paste" && resumeText.trim()) {
        // Paste text
        analyzeRequest = {
          resumeText: resumeText,
          jobDescription: jobDescription,
        };

        const result = await analyze(analyzeRequest);
        router.push({
          pathname: "/results",
          query: { data: JSON.stringify(result) },
        });
      } else {
        throw new Error(
          resumeSource === "upload"
            ? "Please upload a resume file"
            : "Please paste your resume text"
        );
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Talent Forge
          </h1>
          <p className="text-lg text-gray-600">
            Analyze your resume against job descriptions and get personalized
            improvements
          </p>
        </div>

        <form onSubmit={handleSubmit} className="bg-white shadow-lg rounded-lg p-6">
          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
              <p className="text-red-800">{error}</p>
            </div>
          )}

          {/* Resume Input Section */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Resume
            </label>
            <div className="mb-4">
              <div className="flex space-x-4">
                <label className="flex items-center">
                  <input
                    type="radio"
                    name="resume_source"
                    value="upload"
                    checked={resumeSource === "upload"}
                    onChange={(e) => setResumeSource(e.target.value as ResumeSource)}
                    className="mr-2"
                  />
                  Upload File
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    name="resume_source"
                    value="paste"
                    checked={resumeSource === "paste"}
                    onChange={(e) => setResumeSource(e.target.value as ResumeSource)}
                    className="mr-2"
                  />
                  Paste Text
                </label>
              </div>
            </div>

            {resumeSource === "upload" ? (
              <div>
                <input
                  type="file"
                  accept=".pdf,.docx,.txt"
                  onChange={handleFileChange}
                  className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                  required={resumeSource === "upload"}
                />
                {resumeFile && (
                  <p className="mt-2 text-sm text-gray-600">
                    Selected: {resumeFile.name}
                  </p>
                )}
              </div>
            ) : (
              <textarea
                value={resumeText}
                onChange={(e) => setResumeText(e.target.value)}
                placeholder="Paste your resume text here..."
                rows={10}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                required={resumeSource === "paste"}
              />
            )}
          </div>

          {/* Job Description Section */}
          <div className="mb-6">
            <label
              htmlFor="job_description"
              className="block text-sm font-medium text-gray-700 mb-2"
            >
              Job Description
            </label>
            <textarea
              id="job_description"
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the job description here..."
              rows={10}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              required
            />
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-3 px-4 rounded-md font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? "Analyzing..." : "Analyze Resume"}
          </button>
        </form>
      </div>
    </div>
  );
}
