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

const queryClient = new QueryClient();

function App() {
    const [user, setUser] = useState(null);
    const [appliedJobs, setAppliedJobs] = useState([]);
    const [savedJobs, setSavedJobs] = useState([]);

    const handleLogin = (userData) => {
        setUser(userData);
    };

    const handleLogout = () => {
        setUser(null);
        setAppliedJobs([]);
        setSavedJobs([]);
    };

    const handleApply = (job) => {
        setAppliedJobs((prev) =>
            prev.some((j) => j.id === job.id) ? prev : [...prev, job],
        );
    };

    const handleSave = (job) => {
        setSavedJobs((prev) =>
            prev.some((j) => j.id === job.id) ? prev : [...prev, job],
        );
    };

    const handleRemoveSavedJob = (jobId) => {
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
