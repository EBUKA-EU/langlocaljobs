import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchJobs } from "../api/jobs";
import { Link } from "react-router-dom";

function JobsPage({ user }) {
    const token = user?.token;
    const [page, setPage] = useState(1);
    const perPage = 10;
    const { data, isLoading, error } = useQuery({
        queryKey: ["jobs", token, page, perPage],
        queryFn: () => fetchJobs(token, page, perPage),
        enabled: !!token,
    });

    const jobs = data?.jobs || [];
    const jobCount = data?.total || 0;
    const totalPages = data?.pages || 1;

    return (
        <div className="max-w-2xl mx-auto mt-8">
            <div className="flex items-center justify-between mb-4">
                <h1 className="text-3xl font-bold">All Jobs</h1>
                <span className="text-lg text-gray-700 font-semibold">
                    Available jobs: {jobCount}
                </span>
            </div>
            {isLoading && <p>Loading jobs...</p>}
            {error && <p className="text-red-600">Failed to load jobs.</p>}
            {jobs && jobs.length > 0 ? (
                <>
                    <ul className="divide-y divide-gray-200">
                        {jobs.map((job) => (
                            <li
                                key={job.id}
                                className="py-2 flex items-center justify-between"
                            >
                                <div>
                                    <div className="font-bold">{job.title}</div>
                                    <div className="text-gray-600 text-sm">
                                        {job.company}
                                    </div>
                                </div>
                                <Link
                                    to={`/jobs/${job.id}`}
                                    className="ml-4 bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 transition"
                                >
                                    View Details
                                </Link>
                            </li>
                        ))}
                    </ul>
                    <div className="flex justify-center mt-6 space-x-2">
                        <button
                            className="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 disabled:opacity-50"
                            onClick={() => setPage((p) => Math.max(1, p - 1))}
                            disabled={page === 1}
                        >
                            Previous
                        </button>
                        <span className="px-2 py-1">
                            Page {page} of {totalPages}
                        </span>
                        <button
                            className="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 disabled:opacity-50"
                            onClick={() =>
                                setPage((p) => Math.min(totalPages, p + 1))
                            }
                            disabled={page === totalPages}
                        >
                            Next
                        </button>
                    </div>
                </>
            ) : (
                !isLoading && <p>No jobs found.</p>
            )}
        </div>
    );
}

export default JobsPage;
