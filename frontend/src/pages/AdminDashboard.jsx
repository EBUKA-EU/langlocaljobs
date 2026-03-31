import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import {
    fetchAllUsers,
    updateUserRole,
    deleteUser,
    fetchAllJobs,
    deleteJob,
    fetchAllAppliedJobs,
} from "../api/admin";

const ROLES = ["user", "admin"];

function AdminDashboard({ user }) {
    const navigate = useNavigate();
    const qc = useQueryClient();
    const [tab, setTab] = useState("users");
    const [jobPage, setJobPage] = useState(1);

    // Redirect non-admins
    if (!user) {
        return (
            <div className="max-w-2xl mx-auto mt-16 text-center">
                <p className="text-gray-600">Please log in.</p>
            </div>
        );
    }
    if (user.role !== "admin") {
        return (
            <div className="max-w-2xl mx-auto mt-16 text-center">
                <p className="text-red-600 font-semibold">
                    Access denied. Admins only.
                </p>
            </div>
        );
    }

    return (
        <div className="max-w-5xl mx-auto mt-8">
            <h1 className="text-3xl font-extrabold mb-6 text-blue-700">
                Admin Dashboard
            </h1>

            {/* Tabs */}
            <div className="flex gap-2 mb-6">
                <button
                    onClick={() => setTab("users")}
                    className={`px-4 py-2 rounded font-semibold ${tab === "users" ? "bg-blue-600 text-white" : "bg-gray-200 text-gray-700 hover:bg-gray-300"}`}
                >
                    Users
                </button>
                <button
                    onClick={() => setTab("jobs")}
                    className={`px-4 py-2 rounded font-semibold ${tab === "jobs" ? "bg-blue-600 text-white" : "bg-gray-200 text-gray-700 hover:bg-gray-300"}`}
                >
                    Jobs
                </button>
                <button
                    onClick={() => setTab("applied")}
                    className={`px-4 py-2 rounded font-semibold ${tab === "applied" ? "bg-blue-600 text-white" : "bg-gray-200 text-gray-700 hover:bg-gray-300"}`}
                >
                    Applied Jobs
                </button>
            </div>

            {tab === "users" && <UsersTab token={user.token} qc={qc} />}
            {tab === "jobs" && (
                <JobsTab
                    token={user.token}
                    qc={qc}
                    page={jobPage}
                    setPage={setJobPage}
                />
            )}
            {tab === "applied" && <AppliedJobsTab token={user.token} />}
        </div>
    );
}

function UsersTab({ token, qc }) {
    const {
        data: users,
        isLoading,
        error,
    } = useQuery({
        queryKey: ["admin-users", token],
        queryFn: () => fetchAllUsers(token),
        enabled: !!token,
    });

    const roleMutation = useMutation({
        mutationFn: ({ userId, role }) => updateUserRole(token, userId, role),
        onSuccess: () => qc.invalidateQueries({ queryKey: ["admin-users"] }),
    });

    const deleteMutation = useMutation({
        mutationFn: (userId) => deleteUser(token, userId),
        onSuccess: () => qc.invalidateQueries({ queryKey: ["admin-users"] }),
    });

    if (isLoading) return <p>Loading users...</p>;
    if (error) return <p className="text-red-600">Failed to load users.</p>;

    return (
        <div>
            <p className="mb-3 text-gray-600 font-semibold">
                {users?.length ?? 0} registered users
            </p>
            <div className="overflow-x-auto">
                <table className="w-full bg-white rounded shadow text-sm">
                    <thead>
                        <tr className="bg-gray-100 text-left text-gray-700">
                            <th className="px-4 py-2">ID</th>
                            <th className="px-4 py-2">Name</th>
                            <th className="px-4 py-2">Email</th>
                            <th className="px-4 py-2">Role</th>
                            <th className="px-4 py-2">Joined</th>
                            <th className="px-4 py-2">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {(users || []).map((u) => (
                            <tr
                                key={u.id}
                                className="border-t hover:bg-gray-50"
                            >
                                <td className="px-4 py-2 text-gray-500">
                                    {u.id}
                                </td>
                                <td className="px-4 py-2 font-medium">
                                    {u.name || "—"}
                                </td>
                                <td className="px-4 py-2">{u.email}</td>
                                <td className="px-4 py-2">
                                    <select
                                        value={u.role}
                                        onChange={(e) =>
                                            roleMutation.mutate({
                                                userId: u.id,
                                                role: e.target.value,
                                            })
                                        }
                                        className="border rounded px-2 py-1 text-sm"
                                    >
                                        {ROLES.map((r) => (
                                            <option key={r} value={r}>
                                                {r}
                                            </option>
                                        ))}
                                    </select>
                                </td>
                                <td className="px-4 py-2 text-gray-500">
                                    {u.created_at
                                        ? new Date(
                                              u.created_at,
                                          ).toLocaleDateString()
                                        : "—"}
                                </td>
                                <td className="px-4 py-2">
                                    <button
                                        onClick={() => {
                                            if (
                                                window.confirm(
                                                    `Delete user "${u.email}"?`,
                                                )
                                            ) {
                                                deleteMutation.mutate(u.id);
                                            }
                                        }}
                                        className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 text-xs"
                                    >
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

function JobsTab({ token, qc, page, setPage }) {
    const { data, isLoading, error } = useQuery({
        queryKey: ["admin-jobs", token, page],
        queryFn: () => fetchAllJobs(token, page, 20),
        enabled: !!token,
    });

    const deleteMutation = useMutation({
        mutationFn: (jobId) => deleteJob(token, jobId),
        onSuccess: () => qc.invalidateQueries({ queryKey: ["admin-jobs"] }),
    });

    if (isLoading) return <p>Loading jobs...</p>;
    if (error) return <p className="text-red-600">Failed to load jobs.</p>;

    const jobs = data?.jobs || [];
    const totalPages = data?.pages || 1;

    return (
        <div>
            <p className="mb-3 text-gray-600 font-semibold">
                {data?.total ?? 0} total jobs
            </p>
            <div className="overflow-x-auto">
                <table className="w-full bg-white rounded shadow text-sm">
                    <thead>
                        <tr className="bg-gray-100 text-left text-gray-700">
                            <th className="px-4 py-2">ID</th>
                            <th className="px-4 py-2">Title</th>
                            <th className="px-4 py-2">Company</th>
                            <th className="px-4 py-2">Location</th>
                            <th className="px-4 py-2">Posted</th>
                            <th className="px-4 py-2">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {jobs.map((job) => (
                            <tr
                                key={job.id}
                                className="border-t hover:bg-gray-50"
                            >
                                <td className="px-4 py-2 text-gray-500">
                                    {job.id}
                                </td>
                                <td className="px-4 py-2 font-medium">
                                    {job.title}
                                </td>
                                <td className="px-4 py-2">
                                    {job.company || "—"}
                                </td>
                                <td className="px-4 py-2">
                                    {job.location || "—"}
                                </td>
                                <td className="px-4 py-2 text-gray-500">
                                    {job.posted_at
                                        ? new Date(
                                              job.posted_at,
                                          ).toLocaleDateString()
                                        : "—"}
                                </td>
                                <td className="px-4 py-2">
                                    <button
                                        onClick={() => {
                                            if (
                                                window.confirm(
                                                    `Delete job "${job.title}"?`,
                                                )
                                            ) {
                                                deleteMutation.mutate(job.id);
                                            }
                                        }}
                                        className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 text-xs"
                                    >
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Pagination */}
            <div className="flex justify-center mt-4 gap-2">
                <button
                    className="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 disabled:opacity-50"
                    onClick={() => setPage((p) => Math.max(1, p - 1))}
                    disabled={page === 1}
                >
                    Previous
                </button>
                <span className="px-3 py-1 text-gray-700">
                    Page {page} of {totalPages}
                </span>
                <button
                    className="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 disabled:opacity-50"
                    onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                    disabled={page === totalPages}
                >
                    Next
                </button>
            </div>
        </div>
    );
}

function AppliedJobsTab({ token }) {
    const { data, isLoading, error } = useQuery({
        queryKey: ["admin-applied-jobs", token],
        queryFn: () => fetchAllAppliedJobs(token),
        enabled: !!token,
    });

    if (isLoading) return <p>Loading applied jobs...</p>;
    if (error)
        return <p className="text-red-600">Failed to load applied jobs.</p>;

    const rows = data?.applied_jobs || [];

    return (
        <div>
            <p className="mb-3 text-gray-600 font-semibold">
                {data?.total ?? 0} total applications
            </p>
            <div className="overflow-x-auto">
                <table className="w-full bg-white rounded shadow text-sm">
                    <thead>
                        <tr className="bg-gray-100 text-left text-gray-700">
                            <th className="px-4 py-2">User</th>
                            <th className="px-4 py-2">Email</th>
                            <th className="px-4 py-2">Job Title</th>
                            <th className="px-4 py-2">Company</th>
                            <th className="px-4 py-2">Applied At</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows.length === 0 && (
                            <tr>
                                <td
                                    colSpan={5}
                                    className="px-4 py-4 text-center text-gray-500"
                                >
                                    No applications yet.
                                </td>
                            </tr>
                        )}
                        {rows.map((a) => (
                            <tr
                                key={a.id}
                                className="border-t hover:bg-gray-50"
                            >
                                <td className="px-4 py-2 font-medium">
                                    {a.user_name || "—"}
                                </td>
                                <td className="px-4 py-2">{a.user_email}</td>
                                <td className="px-4 py-2">{a.job_title}</td>
                                <td className="px-4 py-2">
                                    {a.job_company || "—"}
                                </td>
                                <td className="px-4 py-2 text-gray-500">
                                    {a.applied_at
                                        ? new Date(
                                              a.applied_at,
                                          ).toLocaleString()
                                        : "—"}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default AdminDashboard;
