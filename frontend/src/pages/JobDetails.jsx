import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchJobById } from "../api/jobs";

function JobDetails({
    user,
    onApply,
    onSave,
    onUnsave,
    appliedJobs = [],
    savedJobs = [],
}) {
    const navigate = useNavigate();
    const { jobId } = useParams();
    const [job, setJob] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [applied, setApplied] = useState(false);
    const [savedJob, setSavedJob] = useState(false);

    useEffect(() => {
        const loadJob = async () => {
            setLoading(true);
            setError("");
            try {
                const jobData = await fetchJobById(user?.token, jobId);
                if (jobData && !jobData.error) {
                    setJob(jobData);
                } else {
                    setJob(null);
                }
            } catch (err) {
                setError("Failed to load job details.");
            }
            setLoading(false);
        };
        loadJob();
    }, [jobId, user]);

    // Sync applied/saved state with props and loaded job
    useEffect(() => {
        if (job) {
            const isApplied = appliedJobs.some((j) => j.id === job.id);
            const isSaved = savedJobs.some((j) => j.id === job.id);
            setApplied(isApplied);
            setSavedJob(isSaved);
        }
    }, [job, appliedJobs, savedJobs]);

    const handleApply = () => {
        setApplied(true);
        if (onApply && job) {
            const appliedAt = new Date().toISOString();
            onApply({ ...job, appliedAt });
        }
    };

    const handleSave = () => {
        setSavedJob(true);
        if (onSave && job) onSave(job);
    };

    const handleUnsave = () => {
        setSavedJob(false);
        if (onUnsave && job) onUnsave(job.id);
    };

    if (loading) return <div className="mt-8 text-center">Loading...</div>;
    if (error)
        return <div className="mt-8 text-center text-red-600">{error}</div>;
    if (!job) return <div className="mt-8 text-center">Job not found.</div>;

    return (
        <div className="max-w-2xl mx-auto mt-8 bg-white rounded shadow p-6">
            <button
                className="mb-4 px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded text-gray-700 font-semibold"
                onClick={() => navigate(-1)}
            >
                &larr; Go Back
            </button>
            <h1 className="text-3xl font-bold mb-2">{job.title}</h1>
            <div className="text-gray-600 mb-2">
                {job.company} &middot; {job.location}
            </div>
            <div className="mb-4">
                {job.description ? (
                    <div
                        className="text-gray-700 text-sm leading-relaxed job-description"
                        dangerouslySetInnerHTML={{ __html: job.description }}
                    />
                ) : (
                    <p className="text-gray-600">No description provided.</p>
                )}
            </div>
            <a
                href={job.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 underline mb-4 block"
            >
                View Original Posting
            </a>
            <div className="mt-6 flex flex-col gap-4">
                <div>
                    <button
                        className="px-4 py-2 rounded font-semibold bg-blue-600 text-white hover:bg-blue-700"
                        onClick={() =>
                            window.open(
                                job.url,
                                "_blank",
                                "noopener,noreferrer",
                            )
                        }
                    >
                        Apply
                    </button>
                </div>
                <div className="mt-4">
                    <span className="font-semibold mr-2">Already Applied?</span>
                    {!applied && (
                        <button
                            className="px-4 py-2 rounded font-semibold bg-green-600 text-white hover:bg-green-700"
                            onClick={handleApply}
                        >
                            Yes
                        </button>
                    )}
                    {applied && (
                        <span className="ml-2 text-green-700 font-semibold">
                            Applied!
                        </span>
                    )}
                </div>
                <div>
                    {savedJob ? (
                        <button
                            className="px-4 py-2 rounded font-semibold bg-yellow-500 text-white hover:bg-yellow-600"
                            onClick={handleUnsave}
                        >
                            Saved &mdash; Remove
                        </button>
                    ) : (
                        <button
                            className="px-4 py-2 rounded font-semibold bg-yellow-400 text-white hover:bg-yellow-500"
                            onClick={handleSave}
                        >
                            Save Job
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
}

export default JobDetails;
