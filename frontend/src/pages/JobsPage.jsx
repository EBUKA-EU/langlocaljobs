import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchJobs } from "../api/jobs";
import { Link } from "react-router-dom";

function JobsPage({ user }) {
    const token = user?.token;
    const [page, setPage] = useState(1);
    const perPage = 10;

    // Filter state (applied on submit)
    const [search, setSearch] = useState("");
    const [location, setLocation] = useState("");
    const [company, setCompany] = useState("");
    const [applied, setApplied] = useState({
        search: "",
        location: "",
        company: "",
    });

    const { data, isLoading, error } = useQuery({
        queryKey: ["jobs", token, page, perPage, applied],
        queryFn: () => fetchJobs(token, page, perPage, applied),
        enabled: !!token,
    });

    const jobs = data?.jobs || [];
    const jobCount = data?.total || 0;
    const totalPages = data?.pages || 1;

    const handleSearch = (e) => {
        e.preventDefault();
        setPage(1);
        setApplied({ search, location, company });
    };

    const handleClear = () => {
        setSearch("");
        setLocation("");
        setCompany("");
        setPage(1);
        setApplied({ search: "", location: "", company: "" });
    };

    const hasFilters = applied.search || applied.location || applied.company;

    return (
        <div className="max-w-2xl mx-auto mt-8">
            <div className="flex items-center justify-between mb-4">
                <h1 className="text-3xl font-bold">All Jobs</h1>
                <span className="text-lg text-gray-700 font-semibold">
                    {hasFilters ? `${jobCount} results` : `${jobCount} jobs`}
                </span>
            </div>

            {/* Search & Filter form */}
            <form
                onSubmit={handleSearch}
                className="bg-white rounded shadow p-4 mb-6 flex flex-col gap-3"
            >
                <div className="flex gap-2">
                    <input
                        type="text"
                        placeholder="Search job title..."
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        className="flex-1 border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
                    />
                </div>
                <div className="flex gap-2">
                    <input
                        type="text"
                        placeholder="Filter by location..."
                        value={location}
                        onChange={(e) => setLocation(e.target.value)}
                        className="flex-1 border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
                    />
                    <input
                        type="text"
                        placeholder="Filter by company..."
                        value={company}
                        onChange={(e) => setCompany(e.target.value)}
                        className="flex-1 border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
                    />
                </div>
                <div className="flex gap-2">
                    <button
                        type="submit"
                        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 font-semibold text-sm"
                    >
                        Search
                    </button>
                    {hasFilters && (
                        <button
                            type="button"
                            onClick={handleClear}
                            className="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300 font-semibold text-sm"
                        >
                            Clear
                        </button>
                    )}
                </div>
            </form>

            {isLoading && <p>Loading jobs...</p>}
            {error && <p className="text-red-600">Failed to load jobs.</p>}
            {!isLoading && jobs.length === 0 && (
                <p className="text-gray-600">
                    No jobs found{hasFilters ? " for your search" : ""}.
                </p>
            )}
            {jobs.length > 0 && (
                <>
                    <ul className="divide-y divide-gray-200">
                        {jobs.map((job) => (
                            <li
                                key={job.id}
                                className="py-3 flex items-center justify-between"
                            >
                                <div>
                                    <div className="font-bold">{job.title}</div>
                                    <div className="text-gray-600 text-sm">
                                        {[job.company, job.location]
                                            .filter(Boolean)
                                            .join(" · ")}
                                    </div>
                                </div>
                                <Link
                                    to={`/jobs/${job.id}`}
                                    className="ml-4 bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 transition text-sm"
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
            )}
        </div>
    );
}

export default JobsPage;
