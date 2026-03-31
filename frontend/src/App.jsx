import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import UserDashboard from "./pages/UserDashboard";
import JobsPage from "./pages/JobsPage";
import JobDetails from "./pages/JobDetails";
import NavBar from "./components/NavBar";
import Footer from "./components/Footer";
import {
    fetchSavedJobs,
    saveJob,
    unsaveJob,
    fetchAppliedJobs,
    markApplied,
} from "./api/jobs";
import AdminDashboard from "./pages/AdminDashboard";

const queryClient = new QueryClient();

function App() {
    const [user, setUser] = useState(null);
    const [appliedJobs, setAppliedJobs] = useState([]);
    const [savedJobs, setSavedJobs] = useState([]);

    const handleLogin = async (userData) => {
        setUser(userData);
        try {
            const [savedData, appliedData] = await Promise.all([
                fetchSavedJobs(userData.token),
                fetchAppliedJobs(userData.token),
            ]);
            setSavedJobs(savedData.saved_jobs || []);
            setAppliedJobs(appliedData.applied_jobs || []);
        } catch {
            setSavedJobs([]);
            setAppliedJobs([]);
        }
    };

    const handleLogout = () => {
        setUser(null);
        setAppliedJobs([]);
        setSavedJobs([]);
    };

    const handleApply = async (job) => {
        if (!user?.token) return;
        try {
            const result = await markApplied(user.token, job.id);
            const appliedAt = result.applied_at || new Date().toISOString();
            setAppliedJobs((prev) =>
                prev.some((j) => j.id === job.id)
                    ? prev
                    : [...prev, { ...job, applied_at: appliedAt }],
            );
        } catch {
            // still update locally even if request fails
            setAppliedJobs((prev) =>
                prev.some((j) => j.id === job.id) ? prev : [...prev, job],
            );
        }
    };

    const handleSave = async (job) => {
        if (!user?.token) return;
        try {
            await saveJob(user.token, job.id);
        } catch {
            // already saved is acceptable
        }
        setSavedJobs((prev) =>
            prev.some((j) => j.id === job.id) ? prev : [...prev, job],
        );
    };

    const handleRemoveSavedJob = async (jobId) => {
        if (!user?.token) return;
        try {
            await unsaveJob(user.token, jobId);
        } catch {
            // proceed with local removal regardless
        }
        setSavedJobs((prev) => prev.filter((j) => j.id !== jobId));
    };

    return (
        <QueryClientProvider client={queryClient}>
            <Router>
                <NavBar user={user} onLogout={handleLogout} />
                <div className="p-4 min-h-[80vh]">
                    <Routes>
                        <Route path="/" element={<Home user={user} />} />
                        <Route
                            path="/jobs"
                            element={<JobsPage user={user} />}
                        />
                        <Route
                            path="/jobs/:jobId"
                            element={
                                <JobDetails
                                    user={user}
                                    onApply={handleApply}
                                    onSave={handleSave}
                                    onUnsave={handleRemoveSavedJob}
                                    appliedJobs={appliedJobs}
                                    savedJobs={savedJobs}
                                />
                            }
                        />
                        <Route
                            path="/login"
                            element={<Login onLogin={handleLogin} />}
                        />
                        <Route path="/register" element={<Register />} />
                        <Route
                            path="/admin"
                            element={<AdminDashboard user={user} />}
                        />
                        <Route
                            path="/dashboard"
                            element={
                                <UserDashboard
                                    user={user}
                                    appliedJobs={appliedJobs}
                                    savedJobs={savedJobs}
                                    onRemoveSavedJob={handleRemoveSavedJob}
                                />
                            }
                        />
                    </Routes>
                </div>
                <Footer />
            </Router>
        </QueryClientProvider>
    );
}

export default App;
