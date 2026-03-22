import React, { useState } from "react";
import SideBar from "../components/SideBar";
import { Link } from "react-router-dom";

function UserDashboard({
    user,
    appliedJobs = [],
    savedJobs = [],
    onRemoveSavedJob,
}) {
    const [selected, setSelected] = useState("saved");

    // Prefer backend name if available
    const displayName = user?.profile?.name || user?.name || "User";

    return (
        <div className="max-w-4xl mx-auto mt-10 min-h-[60vh]">
            <h1 className="text-3xl font-extrabold mb-8 text-blue-700 text-center">
                Welcome, {displayName}!
            </h1>
            <div className="flex">
                <SideBar selected={selected} onSelect={setSelected} />
                <main className="flex-1 bg-white rounded shadow p-6 ml-0 md:ml-6">
                    {selected === "saved" && (
                        <div>
                            <h2 className="text-xl font-semibold mb-2">
                                Saved Jobs
                            </h2>
                            {savedJobs.length === 0 ? (
                                <p className="text-gray-600">
                                    (No saved jobs yet.)
                                </p>
                            ) : (
                                <ul className="divide-y divide-gray-200">
                                    {savedJobs.map((job) => (
                                        <li
                                            key={job.id}
                                            className="py-2 flex items-center justify-between"
                                        >
                                            <div>
                                                <div className="font-bold">
                                                    {job.title}
                                                </div>
                                                <div className="text-gray-600 text-sm">
                                                    {job.company}
                                                </div>
                                            </div>
                                            <div className="flex gap-2">
                                                <Link
                                                    to={`/jobs/${job.id}`}
                                                    className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 transition"
                                                >
                                                    Apply now
                                                </Link>
                                                <button
                                                    className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 transition"
                                                    onClick={() =>
                                                        onRemoveSavedJob(job.id)
                                                    }
                                                >
                                                    Remove
                                                </button>
                                            </div>
                                        </li>
                                    ))}
                                </ul>
                            )}
                        </div>
                    )}
                    {selected === "applied" && (
                        <div>
                            <h2 className="text-xl font-semibold mb-2">
                                Applied Jobs
                            </h2>
                            {appliedJobs.length === 0 ? (
                                <p className="text-gray-600">
                                    (No applied jobs yet.)
                                </p>
                            ) : (
                                <ul className="divide-y divide-gray-200">
                                    {appliedJobs.map((job) => (
                                        <li
                                            key={job.id}
                                            className="py-2 flex items-center justify-between"
                                        >
                                            <div>
                                                <div className="font-bold">
                                                    {job.title}
                                                </div>
                                                <div className="text-gray-600 text-sm">
                                                    {job.company}
                                                </div>
                                                {job.appliedAt && (
                                                    <div className="text-xs text-gray-400 mt-1">
                                                        Applied:{" "}
                                                        {new Date(
                                                            job.appliedAt,
                                                        ).toLocaleString()}
                                                    </div>
                                                )}
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
                            )}
                        </div>
                    )}
                </main>
            </div>
        </div>
    );
}

export default UserDashboard;
